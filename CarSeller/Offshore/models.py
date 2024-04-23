from django.db import models

CATEGORY_CHOICES = (
    ('FD','Ford'),
    ('MD', 'Mercedez'),
    ('FR', 'Ferrari'),
    ('LB', 'Lamborghini'),
    ('MB', 'Maybach'),
    ('BG', 'Buggati'),
)


class Product(models.Model):
    name = models.CharField(max_length=100)
    selling_price = models.FloatField()
    features = models.TextField()
    brand = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='product')
    
    
    def __str__(self):
        return self.name