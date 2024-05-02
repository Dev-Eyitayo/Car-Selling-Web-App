from django.contrib import admin
from . models import Product, Customer, Cart, Payment, OrderPlaced

# @admin.register(Product)
# class ProductModelAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'brand', 'product_image']

admin.site.register(Product)

admin.site.register(Customer)

admin.site.register(Cart)

admin.site.register(Payment)

admin.site.register(OrderPlaced)