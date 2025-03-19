from django.db import models
from authentication.models import Users
from django.conf import settings

# Create your models here.

class LoyaltyPoints(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="loyalty_points")
    points = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.name} - {self.points} points"
    
class LoyaltyTransaction(models.Model):
    TRANSACTION_TYPES = [
        ("Earned", "Earned"),
        ("Redeemed", "Redeemed"),
        ("Expired", "Expired"),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="loyalty_transactions")
    points = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.name} - {self.transaction_type} {self.points} points"
