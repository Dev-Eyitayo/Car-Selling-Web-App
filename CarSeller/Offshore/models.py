from django.db import models
from django.contrib.auth.models import User
CATEGORY_CHOICES = (
    ('AU','Audi'),
    ('MD', 'Mercedes'),
    ('BMW', 'BMW'),
    ('LB', 'Lamborghini'),
    ('MB', 'Maybach'),
    ('BT', 'Bentley'),
)
STATE_CHOICES = (
    ('Abia', 'Abia'),
    ('Adamawa', 'Adamawa'),
    ('Akwa Ibom', 'Akwa Ibom'),
    ('Anambra', 'Anambra'),
    ('Bauchi', 'Bauchi'),
    ('Bayelsa', 'Bayelsa'),
    ('Benue', 'Benue'),
    ('Borno', 'Borno'),
    ('Cross River', 'Cross River'),
    ('Delta', 'Delta'),
    ('Ebonyi', 'Ebonyi'),
    ('Edo', 'Edo'),
    ('Ekiti', 'Ekiti'),
    ('Enugu', 'Enugu'),
    ('Gombe', 'Gombe'),
    ('Imo', 'Imo'),
    ('Jigawa', 'Jigawa'),
    ('Kaduna', 'Kaduna'),
    ('Kano', 'Kano'),
    ('Katsina', 'Katsina'),
    ('Kebbi', 'Kebbi'),
    ('Kogi', 'Kogi'),
    ('Kwara', 'Kwara'),
    ('Lagos', 'Lagos'),
    ('Nasarawa', 'Nasarawa'),
    ('Niger', 'Niger'),
    ('Ogun', 'Ogun'),
    ('Ondo', 'Ondo'),
    ('Osun', 'Osun'),
    ('Oyo', 'Oyo'),
    ('Plateau', 'Plateau'),
    ('Rivers', 'Rivers'),
    ('Sokoto', 'Sokoto'),
    ('Taraba', 'Taraba'),
    ('Yobe', 'Yobe'),
    ('Zamfara', 'Zamfara'),
    ('Abuja', 'Abuja'),
)


class Product(models.Model):
    name = models.CharField(max_length=100)
    selling_price = models.FloatField()
    features = models.TextField()
    brand = models.CharField(choices=CATEGORY_CHOICES, max_length=200)
    product_image = models.ImageField(upload_to='product')
    
    
    def __str__(self):
        return self.name
    
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    mobile = models.IntegerField(default=8)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=100)
    
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    @property
    def total_cost(self):
        return self.quantity * self.product.selling_price


STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packaged', 'Packaged'),
    ('On the way', 'On the way'),
    ('Delivered', 'Delivered'),
    ('Canceled', 'Canceled'),
    ('Pending', 'Pending'),
)


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    paypalOrderId = models.CharField(max_length=100, blank=True, null=True)
    paypalPaymentStatus = models.CharField(max_length=100, blank=True, null=True)
    paypalPaymentID = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=False)
    
    
class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    
    @property
    def total_cost(self):
        return self.quantity * self.product.selling_price