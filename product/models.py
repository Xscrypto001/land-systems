

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_names = models.CharField(max_length=200)
    whats_number = models.CharField(max_length=15)
    address = models.CharField(max_length=200)
    county = models.CharField(max_length=200)
    
    
class Land(models.Model):
    title_deed = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=200)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    county = models.CharField(max_length=200)
    size = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='land_images/', null=True, blank=True)  # Add this line

class Listing(models.Model):
    land = models.ForeignKey(Land, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings_created')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)


   

class Transaction(models.Model):
    buyer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='buyer_transactions')
    seller = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='seller_transactions')
    land = models.ForeignKey(Land, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateField(auto_now_add=True)

   


