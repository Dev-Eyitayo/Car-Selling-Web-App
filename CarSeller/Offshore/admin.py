from django.contrib import admin
from . models import Product, Customer

# @admin.register(Product)
# class ProductModelAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'brand', 'product_image']

admin.site.register(Product)

admin.site.register(Customer)
