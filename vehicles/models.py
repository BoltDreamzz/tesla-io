import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Vehicle(models.Model):
    MODEL_CHOICES = (
        ('model_3', 'Model 3'),
        ('model_y', 'Model Y'),
        ('model_s', 'Model S'),
        ('model_x', 'Model X'),
        ('cybertruck', 'Cybertruck'),
        ('roadster', 'Roadster'),
    )
    
    CONDITION_CHOICES = (
        ('new', 'New'),
        ('used', 'Used'),
        ('certified', 'Certified Pre-Owned'),
    )
    
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('reserved', 'Reserved'),
    )
    
    # Basic Information
    name = models.CharField(max_length=200)
    model = models.CharField(max_length=20, choices=MODEL_CHOICES)
    year = models.PositiveIntegerField()
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='new')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    
    # Pricing
    price = models.DecimalField(max_digits=12, decimal_places=2, help_text="Full vehicle price")
    share_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price per share")
    total_shares = models.PositiveIntegerField(default=100)
    available_shares = models.PositiveIntegerField(default=100)
    
    # Specifications
    mileage = models.PositiveIntegerField(null=True, blank=True, help_text="Mileage for used vehicles")
    color = models.CharField(max_length=50, default='White')
    interior_color = models.CharField(max_length=50, blank=True)
    battery_range = models.PositiveIntegerField(help_text="Range in miles")
    acceleration = models.DecimalField(max_digits=4, decimal_places=1, help_text="0-60 mph in seconds")
    
    # Features
    features = models.TextField(help_text="Comma-separated features", blank=True)
    autopilot = models.BooleanField(default=True)
    premium_audio = models.BooleanField(default=True)
    
    # Media
    image = models.ImageField(upload_to='vehicles/', null=True, blank=True)
    
    # Location
    location = models.CharField(max_length=200, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.year} {self.get_model_display()} - ${self.price}"
    
    @property
    def remaining_value(self):
        """Calculate remaining value based on available shares"""
        return self.available_shares * self.share_price
    
    @property
    def sold_percentage(self):
        """Calculate percentage of shares sold"""
        if self.total_shares > 0:
            sold = self.total_shares - self.available_shares
            return (sold / self.total_shares) * 100
        return 0

class VehicleSharePurchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicle_shares')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='share_purchases')
    shares_purchased = models.PositiveIntegerField()
    price_per_share = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_reference = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.vehicle.name} - {self.shares_purchased} shares"

class VehiclePurchase(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicle_purchases')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='purchases')
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2)
    delivery_address = models.TextField()
    contact_phone = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_reference = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.vehicle.name} - ${self.purchase_price}"