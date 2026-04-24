from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import json

from .forms import SignUpForm, ProfileForm, OTPVerificationForm
from .models import Profile
from .utils import send_verification_otp
# def signup(request):
#     """Registration with OTP verification"""
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             email = form.clean_email()
#             if email.exists:
#                 return redirect('login')
#             user = form.save()
            
#             # Log the user in
#             login(request, user)
            
#             # Send OTP
#             success, message = send_verification_otp(user, request)
            
#             if success:
#                 messages.success(
#                     request, 
#                     'Account created! finish up.'
#                 )
#                 return redirect('verify_otp')
#             else:
#                 messages.error(request, f'Failed to send verification code: {message}')
#                 return redirect('verify_otp')
#     else:
#         form = SignUpForm()
#     return render(request, 'accounts/signup.html', {'form': form})


from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.contrib.auth.models import User

def custom_login(request):
    """Custom login view with email validation and proper error handling"""
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        
        # Get the username/email from the form
        username_or_email = request.POST.get('username')
        
        # Check if the input is an email
        if username_or_email and '@' in username_or_email:
            # Try to find user by email
            try:
                user = User.objects.get(email=username_or_email)
                username = user.username
                # Update the form data with username
                request.POST = request.POST.copy()
                request.POST['username'] = username
                # Recreate form with updated username
                form = AuthenticationForm(request, data=request.POST)
            except User.DoesNotExist:
                # Email doesn't exist, redirect to signup
                messages.warning(request, 'This email is not registered. Please create an account first.')
                return redirect('signup')
        
        # Check if user exists (if input was username or we found email user)
        if username_or_email:
            # Check if user exists (using username)
            user_exists = User.objects.filter(username=username_or_email).exists()
            if not user_exists and '@' not in username_or_email:
                messages.warning(request, 'This username does not exist. Please check your username or sign up.')
                return redirect('signup')
        
        # Try to authenticate
        if form.is_valid():
            # Get the authenticated user
            user = form.get_user()
            login(request, user)
            
            # Check if user wants to be remembered
            if not request.POST.get('remember'):
                request.session.set_expiry(0)  # Session expires when browser closes
            
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')  # Change to your home page URL name
        else:
            # Authentication failed (wrong password)
            messages.error(request, 'Invalid username or password. Please try again.')
            return render(request, 'accounts/login.html', {'form': form})
    
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})


# def signup(request):
#     """Registration with OTP verification"""
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
        
#         # Check for duplicate email before full validation
#         email = request.POST.get('email')
#         if email and User.objects.filter(email=email).exists():
#             messages.info(request, 'This email is already registered. Please login instead.')
#             return redirect('login')
        
#         if form.is_valid():
#             user = form.save()
#             request.session['pending_user_id'] = user.id
#             # login(request, user)
#             success, message = send_verification_otp(user, request)
            
#             if success:
#                 messages.success(request, 'Account created! Please verify your email to finish up.')
#                 return redirect('verify_otp')
#             else:
#                 messages.error(request, f'Failed to send verification code: {message}')
#                 return redirect('verify_otp')
#     else:
#         form = SignUpForm()
#     return render(request, 'accounts/signup.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        email = request.POST.get('email')
        if email and User.objects.filter(email=email).exists():
            messages.info(request, 'This email is already registered. Please login instead.')
            return redirect('login')

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            request.session['pending_user_id'] = user.id

            success, message = send_verification_otp(user, request)

            messages.success(request, 'Account created! Verify OTP to activate.')
            return redirect('verify_otp')
    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})


# @login_required
# def verify_otp(request):
#     """OTP verification page"""
#     profile = request.user.profile
    
#     # If already verified, redirect to dashboard
#     if profile.email_verified:
#         messages.success(request, 'Your email is already verified!')
#         return redirect('dashboard')
    
#     if request.method == 'POST':
#         form = OTPVerificationForm(request.POST)
#         if form.is_valid():
#             otp = form.cleaned_data['otp']
#             success, message = profile.verify_otp(otp)
            
#             if success:
#                 messages.success(request, message)
#                 return redirect('dashboard')
#             else:
#                 messages.error(request, message)
#                 return redirect('verify_otp')
#     else:
#         form = OTPVerificationForm()
    
#     return render(request, 'accounts/verify_otp.html', {'form': form})


@login_required
def resend_otp(request):
    """Resend OTP"""
    profile = request.user.profile
    
    if profile.email_verified:
        messages.info(request, 'Your email is already verified.')
        return redirect('dashboard')
    
    # Check cooldown (2 minutes)
    if not profile.can_resend_otp():
        # Calculate remaining time
        remaining_seconds = (profile.verification_sent_at + timezone.timedelta(minutes=2) - timezone.now()).total_seconds()
        minutes = int(remaining_seconds // 60)
        seconds = int(remaining_seconds % 60)
        messages.error(
            request, 
            f'Please wait {minutes}:{seconds:02d} before requesting another code.'
        )
        return redirect('verify_otp')
    
    # Send new OTP
    success, message = send_verification_otp(request.user, request)
    
    if success:
        messages.success(request, 'A new code has been sent to your email.')
    else:
        messages.error(request, f'Failed to send code: {message}')
    
    return redirect('verification_pending')

@login_required
def profile(request):
    """User profile view"""
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'accounts/profile.html', {'form': form})

@login_required
def verification_pending(request):
    """Show pending verification page with OTP form"""
    profile = request.user.profile
    
    # If already verified, redirect to dashboard
    if profile.email_verified:
        messages.success(request, 'Your email is already verified!')
        return redirect('dashboard')
    
    # Check if user can resend
    can_resend = profile.can_resend_otp()
    next_resend_time = None
    
    if not can_resend and profile.verification_sent_at:
        next_resend_time = profile.verification_sent_at + timezone.timedelta(minutes=2)
    
    context = {
        'can_resend': can_resend,
        'next_resend_time': next_resend_time,
    }
    return render(request, 'accounts/verification_pending.html', context)

@login_required
def verify_otp(request):
    """Verify OTP and redirect back to pending page with result"""
    profile = request.user.profile
    
    if request.method == 'POST':
        otp = request.POST.get('otp', '')
        success, message = profile.verify_otp(otp)
        
        if success:
            messages.success(request, message)
            # Clear OTP expiry from localStorage (will be handled by JS on next page)
            return redirect('dashboard')
        else:
            messages.error(request, message)
    
    return redirect('verify_otp')
@login_required
def resend_verification(request):
    """Resend verification email (legacy)"""
    profile = request.user.profile
    
    if profile.email_verified:
        messages.info(request, 'Your email is already verified.')
        return redirect('dashboard')
    
    if not profile.can_resend_otp():
        messages.error(request, 'Please wait 2 minutes before requesting another code.')
        # return redirect('verification_pending')
    
    success, message = send_verification_otp(request.user, request)
    
    if success:
        messages.success(request, 'A new verification code has been sent to your email.')
    else:
        messages.error(request, f'Failed to send code: {message}')
    
    return redirect('verify_otp')

def resend_verification_public(request):
    """Allow non-logged in users to request verification (placeholder)"""
    messages.info(request, 'Please login to request a new verification code.')
    return redirect('login')

def verify_email(request, token):
    """Legacy email verification (redirect to OTP)"""
    messages.info(request, 'Please use OTP verification instead.')
    return redirect('verify_otp')