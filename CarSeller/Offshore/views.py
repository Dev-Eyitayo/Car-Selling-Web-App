from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse, HttpResponse
from . models import Product, Customer, Cart, Payment
from django.db.models import Count, Q
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json




def home(request):
    return render(request, 'Offshore/home.html')

def about(request):
    return render(request, 'Offshore/about.html')

# def contact(request):
    return render(request, 'Offshore/contact.html')


class BrandView(View):
    def get(self, request, val):
        product = Product.objects.filter(brand=val)
        name = Product.objects.filter(brand=val).values('name').annotate(total=Count('name'))
        return render(request, 'Offshore/brand.html', locals())
    
class BrandNameView(View):
    def get(self, request, val):
        product = Product.objects.filter(name=val)
        name = Product.objects.filter(brand=product[0].brand).values('name')
        return render(request, 'Offshore/brandName.html', locals())
    
class ProductFeatureView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'Offshore/productFeature.html', locals())
    
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'Offshore/registration.html', locals())
    
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account has been created successfully!")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'Offshore/registration.html', locals())

class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'Offshore/profile.html', locals())
    
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            
            reg = Customer(user=user, name=name, mobile=mobile, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Your Profile has been successfully updated!')
        else: 
            messages.success(request, 'invalid Input data!')
        return render(request, 'Offshore/profile.html', locals())
            
def address(request):
    add = Customer.objects.filter(user=request.user)
    
    return render(request, 'Offshore/address.html', locals())

class updateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'Offshore/updateAddress.html', locals())
    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, "Profile has been updated sucessfully!")
        else:
            messages.warning(request, 'Invalid input Data!')
        return redirect(address)    
    
    
@login_required(login_url='/login/')
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect("/cart")

    
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.selling_price
        amount = amount + value
    totalamount = amount + 30
    
    return render(request, 'Offshore/addtocart.html', locals())

@login_required(login_url='/login/')
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.selling_price
            amount = amount + value
        totalamount = amount + 30
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

@login_required(login_url='/login/')
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.selling_price
            amount = amount + value
        totalamount = amount + 30
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)


@login_required(login_url='/login/')
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.selling_price
            amount = amount + value
        totalamount = amount + 30
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)


@login_required(login_url='/login/')
def checkOut(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    famount = 0
    for p in cart_items:
        value = p.quantity * p.product.selling_price
        famount = famount + value
    totalamount = famount + 30 
    
    host = request.get_host()
    
    
    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': totalamount,
        'item_name': 'Order',
        'invoice': uuid.uuid4(),
        'currency': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return': f"http://{host}{reverse('payment-success')}",
        'cancel_url': f"hhtp://{host}{reverse('payment-failed')}"       
    }   
    
    
    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)
    
    context = {
        'paypal': paypal_payment,
        'user': user,
        'add': add,
        'cart_items': cart_items,
        'famount': famount,
        'totalamount': totalamount,
        'host': host,
    }
    
    combined_locals = {**context, **locals()}
    return render(request, 'Offshore/checkout.html', combined_locals)
    # return render(request, 'Offshore/checkout.html', locals())

@csrf_exempt
def paypal_ipn_handler(request):
    # Handle PayPal IPN notification
    if request.method == 'POST':
        # Validate the IPN data (optional but recommended)
        # Process the IPN data and update your models accordingly
        # Example:
        ipn_data = request.POST
        # Process the data and update your models here
        # Example: Update Payment model based on IPN data
        payment_id = ipn_data.get('custom')  # Assuming you pass payment ID as 'custom' field
        payment_status = ipn_data.get('payment_status')
        if payment_id and payment_status == 'Completed':
            # Update Payment model
            payment = Payment.objects.get(id=payment_id)
            payment.paypal_payment_status = payment_status
            payment.save()
            # Update associated OrderPlaced, if needed

    # Return a response to PayPal to acknowledge receipt of the IPN
    return HttpResponse("OK")


@csrf_exempt
def save_payment_info(request):
    if request.method == 'POST':
        # Parse the JSON data from the request body
        data = json.loads(request.body)
        payment_id = data.get('payment_id')
        status = data.get('status')
        amount = data.get('amount')  # Assuming you're sending the amount from the frontend
        
        # Create a Payment object and save all relevant information
        payment = Payment.objects.create(
            user=request.user,
            amount=amount,
            paypalPaymentID=payment_id,
            paypalPaymentStatus=status,
            paid=True  # Mark payment as paid
        )
        payment.save()
        # Return JSON response indicating success
        return JsonResponse({'message': 'Payment information saved successfully.'})
    else:
        # Return JSON response with error message if request method is not POST
        return JsonResponse({'error': 'Invalid request method.'}, status=400)




def logout_view(request):
    logout(request)  # Django's built-in logout function
    return redirect('login')  # Redirect to the login page after logout


def paymentSuccessful(request):
    return render(request, 'Offshore/paymentsuccess.html')


def paymentFailed(request):
    return render(request, 'Offshore/paymentfail.html')




