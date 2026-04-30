from django import forms
from .models import Stock

from django import forms

class BuyStockForm(forms.Form):
    quantity = forms.IntegerField(
    min_value=4,
    initial=4,
    widget=forms.NumberInput(attrs={
        "id": "quantity-input",
        "min": "4",
        "class": "input imput-bordered w-full max-w-xs"
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