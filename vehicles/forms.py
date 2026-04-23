from django import forms
from .models import VehiclePurchase

class SharePurchaseForm(forms.Form):
    shares = forms.IntegerField(
        min_value=1,
        label="Number of Shares",
        widget=forms.NumberInput(attrs={
            'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500',
            'id': 'shares-input'
        })
    )
    
    def __init__(self, *args, **kwargs):
        self.vehicle = kwargs.pop('vehicle', None)
        super().__init__(*args, **kwargs)
    
    def clean_shares(self):
        shares = self.cleaned_data['shares']
        if self.vehicle and shares > self.vehicle.available_shares:
            raise forms.ValidationError(f"Only {self.vehicle.available_shares} shares available.")
        return shares

class VehiclePurchaseForm(forms.ModelForm):
    class Meta:
        model = VehiclePurchase
        fields = ['delivery_address', 'contact_phone']
        widgets = {
            'delivery_address': forms.Textarea(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': 3,
                'placeholder': 'Enter your full delivery address'
            }),
            'contact_phone': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': '+1 234 567 8900'
            }),
        }