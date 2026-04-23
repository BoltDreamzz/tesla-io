# from django.shortcuts import redirect
# from django.urls import reverse, resolve
# from django.contrib import messages

# class EmailVerificationMiddleware:
#     """
#     Middleware to restrict access to unverified users
#     """
    
#     # URLs that are always accessible
#     ALLOWED_URLS = [
#         'landing',
#         'login',
#         'signup',
#         'logout',
#         'verify_email',
#         'verify_otp',
#         'resend_verification',
#         'resend_verification_public',
#         'verification_pending',
#         'password_reset',
#         'password_reset_done',
#         'password_reset_confirm',
#         'password_reset_complete',
#     ]
    
#     def __init__(self, get_response):
#         self.get_response = get_response
    
#     def __call__(self, request):
#         if request.user.is_authenticated:
#             profile = request.user.profile
#             current_url = resolve(request.path_info).url_name
            
#             # Check if user is verified and trying to access restricted area
#             if not profile.email_verified:
#                 # Allow access to verification-related URLs
#                 messages.warning(
#                         request,
#                         'Please verify your email !.'
#                     )
#                 return redirect('verify_otp')
                    
        
#         response = self.get_response(request)
#         return response