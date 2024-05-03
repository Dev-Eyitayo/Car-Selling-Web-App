
from django.contrib import admin
from django.urls import path, include
from Offshore import views
app_name = 'Offshore'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("Offshore.urls")),
    path('', include('paypal.standard.ipn.urls')),
    path('payment-success/', views.paymentSuccessful, name='payment-success'),
    path('payment-failed/', views.paymentFailed, name='payment-failed'),
    
]
