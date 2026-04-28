from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django.shortcuts import redirect

# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2'}))

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2')

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs['class'] = 'w-full border border-gray-300 rounded px-3 py-2'

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from captcha.fields import ReCaptchaField
# from captcha.widgets import ReCaptchaV2Checkbox
from .models import Profile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, 
        required=True, 
        widget=forms.EmailInput(attrs={
            'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'your@email.com'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if hasattr(field.widget, 'attrs'):
                field.widget.attrs['class'] = 'w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
            # return redirect('login')
        return email

class OTPVerificationForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        min_length=6,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full text-center text-2xl tracking-widest border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': '000000',
            'autocomplete': 'off',
            'maxlength': '6'
        })
    )

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone',)
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2'}),
        }

class ResendVerificationForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full border border-gray-300 rounded px-3 py-2',
            'placeholder': 'Enter your email'
        })
    )


# forms.py

class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Email"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Password"
    }))