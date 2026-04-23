import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



class Deposit(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
    ]
    
    PAYMENT_METHODS = [
        ('bank_transfer', 'Bank Transfer'),
        ('usdt', 'USDT'),
        ('btc', 'BTC'),
        ('usdc', 'USDC'),
        ('ethereum', 'Ethereum'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deposits')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='btc')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    proof_image = models.ImageField(upload_to='deposit_proofs/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(blank=True, null=True)
    admin_notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.status}"
    
    def approve(self):
        self.status = 'approved'
        self.approved_at = timezone.now()
        self.save()
        # Add money to user's wallet
        wallet, created = Wallet.objects.get_or_create(user=self.user)
        wallet.balance += self.amount
        wallet.save()
        
    def decline(self):
        self.status = 'declined'
        self.save()

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Wallet - ${self.balance}"

@receiver(post_save, sender=User)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)

# class Transaction(models.Model):
#     TRANSACTION_TYPES = (
#         ('deposit', 'Deposit'),
#         ('withdrawal', 'Withdrawal'),
#         ('buy', 'Buy Stock'),
#         ('sell', 'Sell Stock'),
#     )
#     STATUS_CHOICES = (
#         ('pending', 'Pending'),
#         ('completed', 'Completed'),
#         ('failed', 'Failed'),
#         ('cancelled', 'Cancelled'),
#     )
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
#     transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
#     amount = models.DecimalField(max_digits=12, decimal_places=2)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
#     reference_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
#     created_at = models.DateTimeField(auto_now_add=True)
#     completed_at = models.DateTimeField(null=True, blank=True)
#     description = models.TextField(blank=True)

#     def __str__(self):
#         return f"{self.get_transaction_type_display()} - {self.amount} ({self.status})"



# Add to your Transaction model
# class Transaction(models.Model):
#     STATUS_CHOICES = [
#         ('payment_pending', 'Awaiting Payment'),
#         ('pending', 'Pending Approval'),
#         ('completed', 'Completed'),
#         ('failed', 'Failed'),
#         ('cancelled', 'Cancelled'),
#     ]
    
#     PAYMENT_METHODS = [
#         ('bank_transfer (Unavailable)', 'Bank Transfer (Unavailable)'),
#         ('usdt', 'USDT'),
#         ('btc', 'Bitcoin'),
#         ('usdc', 'USDC'),
#         ('ethereum', 'Ethereum'),
#     ]
    
#     # Existing fields...
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
#     transaction_type = models.CharField(max_length=20)  # 'deposit' or 'withdrawal'
#     amount = models.DecimalField(max_digits=12, decimal_places=2)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='payment_pending')
#     payment_method = models.CharField(max_length=40, choices=PAYMENT_METHODS, null=True, blank=True)
#     payment_reference = models.CharField(max_length=100, null=True, blank=True)
#     proof_of_payment = models.FileField(upload_to='proofs/', null=True, blank=True)
#     description = models.TextField(blank=True)
#     reference_id = models.CharField(max_length=20, unique=True, editable=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def save(self, *args, **kwargs):
#         if not self.reference_id:
#             self.reference_id = self.generate_reference_id()
#         super().save(*args, **kwargs)
    
#     def generate_reference_id(self):
#         """Generate a unique UUID-based reference ID"""
#         # Method 1: Full UUID
#         return str(uuid.uuid4()).replace('-', '').upper()[:20]
       

#     def __str__(self):
#         return f"Transaction for {self.amount} ({self.status})"


import uuid
from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('buy_stock', 'Buy Stock'),
        ('sell_stock', 'Sell Stock'),
        ('buy_vehicle_share', 'Buy Vehicle Share'),      # New
        ('buy_vehicle', 'Buy Full Vehicle'),              # New
        ('vehicle_share_dividend', 'Vehicle Share Dividend'),  # Future
        ('vehicle_share_sale', 'Vehicle Share Sale'),     # Future
    ]
    
    STATUS_CHOICES = [
        ('payment_pending', 'Awaiting Payment'),
        ('pending', 'Pending Approval'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_METHODS = [
        ('bank_transfer (Unavailable)', 'Bank Transfer (Unavailable)'),
        ('usdt', 'USDT'),
        ('btc', 'Bitcoin'),
        ('usdc', 'USDC'),
        ('ethereum', 'Ethereum'),
    ]
    
    # Existing fields
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=30, choices=TRANSACTION_TYPES)  # Updated max_length
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='payment_pending')
    payment_method = models.CharField(max_length=40, choices=PAYMENT_METHODS, null=True, blank=True)
    payment_reference = models.CharField(max_length=100, null=True, blank=True)
    proof_of_payment = models.FileField(upload_to='proofs/', null=True, blank=True)
    description = models.TextField(blank=True)
    reference_id = models.CharField(max_length=20, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.reference_id:
            self.reference_id = self.generate_reference_id()
        super().save(*args, **kwargs)
    
    def generate_reference_id(self):
        """Generate a unique UUID-based reference ID"""
        return str(uuid.uuid4()).replace('-', '').upper()[:20]

    def __str__(self):
        return f"{self.get_transaction_type_display()} - ${self.amount} ({self.status})"