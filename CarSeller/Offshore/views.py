from django.shortcuts import render
from django.views import View
from . models import Product
from django.db.models import Count
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages

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
        return render(request, 'Offshore/profile.html', locals())
             
            
    
    