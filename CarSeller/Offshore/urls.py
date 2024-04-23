from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.home, name="home"),
    path('brand/<slug:val>', views.BrandView.as_view(), name="brand"),
    path('product-feature/<int:pk>', views.ProductFeatureView.as_view(), name="product-feature"),
    path('brand-name/<val>', views.BrandNameView.as_view(), name="brand-name"),
    path('about/', views.about, name="about"),
    
    # user authentication
    path('create account/', views.CustomerRegistrationView.as_view(), name="register"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)