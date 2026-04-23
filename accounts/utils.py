from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
import random

def send_verification_otp(user, request):
    """Send OTP via email"""
    profile = user.profile
    otp = profile.generate_otp()
    
    # Email subject and content
    subject = f'Your TeslaInvest Verification Code: {otp}'
    
    context = {
        'user': user,
        'otp': otp,
        'expiry_minutes': 10,
        'site_name': 'TeslaInvest',
        'support_email': settings.DEFAULT_FROM_EMAIL,
    }
    
    html_message = render_to_string('accounts/email/verification_otp_email.html', context)
    plain_message = strip_tags(html_message)
    
    # Send email
    try:
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=html_message,
            fail_silently=False,
        )
        profile.verification_sent_at = timezone.now()
        profile.save()
        return True, "OTP sent successfully!"
    except Exception as e:
        return False, str(e)

def send_verification_sms(user, phone_number, otp):
    """Send OTP via SMS (placeholder for SMS gateway integration)"""
    # You can integrate with SMS providers like Twilio, MessageBird, etc.
    # This is a placeholder function
    pass