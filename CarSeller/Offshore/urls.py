from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm, MyPasswordResetForm, MyPasswordChangeForm, MySetPasswordForm


urlpatterns = [
    path("", views.home, name="home"),
    path('brand/<slug:val>', views.BrandView.as_view(), name="brand"),
    path('product-feature/<int:pk>', views.ProductFeatureView.as_view(), name="product-feature"),
    path('brand-name/<val>', views.BrandNameView.as_view(), name="brand-name"),
    path('about/', views.about, name="about"),
    path('accounts/profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('updateAddress/<int:pk>', views.updateAddress.as_view(), name='updateAddress'),
    
    # Cart 
    path("add-to-cart/", views.add_to_cart, name = "add-to-cart"),
    path('cart/', views.show_cart, name="showcart"),
    path('checkout/', views.checkOut, name="checkout"),
    
    path('pluscart/', views.plus_cart,),
    path('minuscart/', views.minus_cart,),
    path('removecart/', views.remove_cart,),
    
    path('paypal-ipn/', views.paypal_ipn_handler, name='paypal-ipn'),
    path('save-payment-info/', views.save_payment_info, name='save_payment_info'),
    
    # user authentication
    path('create account/', views.CustomerRegistrationView.as_view(), name="register"),
    path('login/', auth_view.LoginView.as_view(template_name='Offshore/login.html', authentication_form=LoginForm), name="login"),
    path("password-change/", auth_view.PasswordChangeView.as_view(template_name='Offshore/passwordchange.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone'), name="passwordchange"),
    
    path("passwordchangedone/", auth_view.PasswordChangeDoneView.as_view(template_name="Offshore/passwordchangedone.html"), name = 'passwordchangedone'),
    
    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),
    
    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='Offshore/password_reset.html', form_class=MyPasswordResetForm), name="password_reset"),
    
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='Offshore/password_reset_done.html'), name="password_reset_done"),
    
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='Offshore/password_reset_confirm.html', form_class=MySetPasswordForm), name="password_reset_confirm"),
    
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='Offshore/password_reset_complete.html'), name="password_reset_complete"),
    
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)