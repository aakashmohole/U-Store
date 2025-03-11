import cloudinary.models
from django.db import models
from authentication.models import Users  # Import Users model

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    seller = models.ForeignKey(Users, on_delete=models.CASCADE)  # Link product to seller
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)  # Linked category
    stock = models.IntegerField(default=0)
    image = cloudinary.models.CloudinaryField('image', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
