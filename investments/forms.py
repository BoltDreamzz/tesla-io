from django import forms
from .models import Stock

from django import forms

class BuyStockForm(forms.Form):
    quantity = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=4.00,
        initial=4.00,  # ✅ pre-populates the input
        widget=forms.NumberInput(attrs={
            'class': 'w-full border border-gray-300 px-3 py-2',
            'step': '1',          # prevents weird decimals
            'min': '4',           # HTML validation
        })
    )

    def __init__(self, *args, **kwargs):
        self.stock = kwargs.pop('stock', None)
        super().__init__(*args, **kwargs)

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity < 4:
            raise forms.ValidationError("Quantity must be at least 4 shares.")
        if quantity % 1 != 0:
            raise forms.ValidationError("Quantity must be a whole number of shares.")
        return quantity