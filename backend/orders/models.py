from django.db import models
from django.conf import settings
from products.models import Product
from loyalty.models import LoyaltyPoints, LoyaltyTransaction
# Create your models here.

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Canceled', 'Canceled'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.status == "Delivered":
            self.award_loyalty_points()
    
    def award_loyalty_points(self):
        total_price = sum(item.price * item.quantity for item in self.items.all())
        earned_points = total_price * 0.05
        
        loyalty_account, created = LoyaltyPoints.objects.get_or_create(user=self.user)
        loyalty_account.points += earned_points
        loyalty_account.save()
        
        LoyaltyTransaction.objects.create(self.user, points = earned_points, transaction_type="Earned")
        
        
    def __str__(self):
        return f"Order {self.id} - {self.status}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=100, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}" 