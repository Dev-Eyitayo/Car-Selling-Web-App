class Checkout(View):
    def get(self, request):
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