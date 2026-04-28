# from django.urls import path
# from django.contrib.auth import views as auth_views
# from . import views

# urlpatterns = [
#     path('signup/', views.signup, name='signup'),
#     path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
#     path('logout/', auth_views.LogoutView.as_view(), name='logout'),
#     path('profile/', views.profile, name='profile'),
#     path('password-change/', auth_views.PasswordChangeView.as_view(
#         template_name='accounts/password_change.html', 
#         success_url='/accounts/profile/'
#     ), name='password_change'),
    
#     # Verification URLs
#     path('verify/<str:token>/', views.verify_email, name='verify_email'),
#     path('verification-pending/', views.verification_pending, name='verification_pending'),
#     path('resend-verification/', views.resend_verification, name='resend_verification'),
#     path('resend-verification-public/', views.resend_verification_public, name='resend_verification_public'),
#     # apps/accounts/urls.py
# path('resend-verification-ajax/', views.resend_verification_ajax, name='resend_verification_ajax'),
# ]


from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
     path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/password_change.html', 
        success_url='/accounts/profile/'
    ), name='password_change'),
    
    # OTP Verification URLs
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    path('verification-pending/', views.verification_pending, name='verification_pending'),
    
    # Legacy URLs (keep for backward compatibility)
    path('verify/<str:token>/', views.verify_email, name='verify_email'),
    path('resend-verification/', views.resend_verification, name='resend_verification'),
    path('resend-verification-public/', views.resend_verification_public, name='resend_verification_public'),
]