from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm, MyPasswordResetForm


urlpatterns = [
    path("", views.home, name="home"),
    path('brand/<slug:val>', views.BrandView.as_view(), name="brand"),
    path('product-feature/<int:pk>', views.ProductFeatureView.as_view(), name="product-feature"),
    path('brand-name/<val>', views.BrandNameView.as_view(), name="brand-name"),
    path('about/', views.about, name="about"),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.ProfileView.as_view(), name='address'),
    # user authentication
    path('create account/', views.CustomerRegistrationView.as_view(), name="register"),
    path('login/', auth_view.LoginView.as_view(template_name='Offshore/login.html', authentication_form=LoginForm), name="login"),
    path("password-reset/", auth_view.PasswordResetView.as_view(template_name='Offshore/password_reset.html', form_class=MyPasswordResetForm), name="password_reset")
    
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)