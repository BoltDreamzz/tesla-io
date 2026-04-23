# import uuid
# from django.db import models
# from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.utils import timezone

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
#     phone = models.CharField(max_length=15, blank=True)
#     email_verified = models.BooleanField(default=False)
#     verification_token = models.CharField(max_length=100, blank=True, unique=True)
#     token_created_at = models.DateTimeField(null=True, blank=True)
#     verification_sent_at = models.DateTimeField(null=True, blank=True)

#     def __str__(self):
#         return f"{self.user.username}'s Profile"

#     def generate_verification_token(self):
#         """Generate a unique verification token"""
#         token = uuid.uuid4().hex + uuid.uuid4().hex[:32]
#         self.verification_token = token
#         self.token_created_at = timezone.now()
#         self.save()
#         return token

#     def is_token_expired(self):
#         """Check if verification token is expired (24 hours)"""
#         if self.token_created_at:
#             expiry_time = self.token_created_at + timezone.timedelta(hours=24)
#             return timezone.now() > expiry_time
#         return True

#     def can_resend_verification(self):
#         """Check if user can request another verification email (5 minutes cooldown)"""
#         if self.verification_sent_at:
#             cooldown_time = self.verification_sent_at + timezone.timedelta(minutes=5)
#             return timezone.now() > cooldown_time
#         return True

# # Create Profile automatically when User is created
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         profile = Profile.objects.create(user=instance)
#         # Generate token but don't send email yet (will send after registration)
#         profile.generate_verification_token()

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

import uuid
import random
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import secrets

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True)
    email_verified = models.BooleanField(default=False)
    
    # OTP fields
    verification_otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)
    otp_attempts = models.PositiveSmallIntegerField(default=0)
    
    # Legacy token fields (keep for backward compatibility)
    verification_token = models.CharField(max_length=100, blank=True, null=True)
    token_created_at = models.DateTimeField(null=True, blank=True)
    verification_sent_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def generate_otp(self):
        """Generate a 6-digit OTP"""
        otp = str(random.randint(100000, 999999))
        self.verification_otp = otp
        self.otp_created_at = timezone.now()
        self.otp_attempts = 0
        self.save()
        return otp

    def is_otp_expired(self):
        """Check if OTP is expired (10 minutes)"""
        if self.otp_created_at:
            expiry_time = self.otp_created_at + timezone.timedelta(minutes=10)
            return timezone.now() > expiry_time
        return True

    def can_resend_otp(self):
        """Check if user can request another OTP (2 minutes cooldown)"""
        if self.verification_sent_at:
            cooldown_time = self.verification_sent_at + timezone.timedelta(minutes=2)
            return timezone.now() > cooldown_time
        return True

    def verify_otp(self, otp):
        """Verify OTP and return result"""
        if not self.verification_otp or self.is_otp_expired():
            return False, "OTP has expired. Please request a new one."
        
        if self.otp_attempts >= 5:
            return False, "Too many failed attempts. Please request a new OTP."
        
        if self.verification_otp == otp:
            self.email_verified = True
            self.verification_otp = None
            self.otp_attempts = 0
            self.save()
            return True, "Email verified successfully!"
        
        self.otp_attempts += 1
        self.save()
        remaining = 5 - self.otp_attempts
        return False, f"Invalid OTP. {remaining} attempts remaining."

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()