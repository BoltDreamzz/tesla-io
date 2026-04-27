from django import forms
from .models import Transaction

from django import forms
from .models import Deposit

from django import forms
from .models import Transaction

class DepositForm(forms.Form):
    PAYMENT_CHOICES = [
        # ('bank_transfer', 'Bank Transfer'),
        ('usdt', 'USDT (ERC-20)'),
        ('btc', 'Bitcoin'),
        ('usdc', 'USDC'),
        ('ethereum', 'Ethereum'),
    ]
    
    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=10,
        widget=forms.NumberInput(attrs={
            'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent',
            'placeholder': 'Enter amount (minimum $500)'
        })
    )
    payment_method = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent text-white'
        })
    )

class PaymentConfirmationForm(forms.Form):
    # payment_reference = forms.CharField(
    #     max_length=100,
    #     required=True,
    #     widget=forms.TextInput(attrs={
    #         'class': 'w-full p-3 bg-gray-800 border border-gray-700 rounded-lg',
    #         'placeholder': 'Enter transaction reference/hash',
    #         'readonly': 'readonly',  # Make it readonly by default
    #     }),
    #     help_text="This reference is automatically generated for tracking purposes"
    # )
    
    proof_of_payment = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={
            'class': 'w-full p-3 bg-gray-800 border border-gray-700 rounded-lg',
            'accept': 'image/*,.pdf',
            'required': 'required'
        }),
        help_text="Upload a screenshot or receipt of your payment"
    )
    
    def clean_payment_reference(self):
        reference = self.cleaned_data.get('payment_reference')
        if not reference:
            raise forms.ValidationError('Payment reference is required')
        return reference

class WithdrawForm(forms.Form):
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0.01, widget=forms.NumberInput(attrs={'class': 'w-full border border-gray-300  px-3 py-2', 'placeholder': '0.00'}))
    bank_details = forms.CharField(widget=forms.Textarea(attrs={'class': 'w-full border border-gray-300 rounded px-3 py-2', 'rows': 3, 'placeholder': 'Enter your bank account details'}))