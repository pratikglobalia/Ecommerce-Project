from django.db import models

# Create your models here.
class ContactModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    message = models.TextField()
    
    def __str__(self):
        return self.name
    
    
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200, unique=True)
    password = models.CharField(max_length=100)
    password2 = models.CharField(max_length=100)
    mobile_number = models.IntegerField()
    address = models.CharField(max_length=400)
    postcode = models.IntegerField(null=True)
    area = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    
    def __str__(self):
        return self.email


gender_choices = (('mens','mens'),('womens','womens'),('kids','kids'))
class ProductModel(models.Model):
    category = models.CharField(max_length=10, choices=gender_choices)
    upload = models.ImageField(upload_to='images/', default='')
    product_name = models.CharField(max_length=200)
    product_price = models.IntegerField()
    product_disc = models.TextField(max_length=500)
    
    
class CartModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return str(self.user)