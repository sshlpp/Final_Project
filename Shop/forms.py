from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Product, SwapedUser, Purchase
import requests

class RegistForm(UserCreationForm):
    seller = forms.BooleanField(
        required=False,
        label="Я хочу продавать вещи",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )
    class Meta:
        model = SwapedUser
        fields = ["username", "email", "password1", "password2", "seller"]
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "formWidget",
                "placeholder": "Enter username"
            }),
            "email": forms.EmailInput(attrs={
                "class": "formWidget",
                "placeholder": "Enter email"
            }),
            "password1": forms.PasswordInput(attrs={
                "class": "formWidget",
                "placeholder": "Enter password"
            }),
            "password2": forms.PasswordInput(attrs={
                "class": "formWidget",
                "placeholder": "Confirm your password"
            }),
        }


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["image", "name", "brand", "size", "category", "description", "price"]
        widgets = {
            "image": forms.ClearableFileInput(attrs={"class": "add-product-form-widget"}),
            "name": forms.TextInput(attrs={"class": "add-product-form-widget"}),
            "brand": forms.TextInput(attrs={"class": "add-product-form-widget"}),
            "size": forms.TextInput(attrs={"class": "add-product-form-widget"}),
            "category": forms.TextInput(attrs={"class": "add-product-form-widget"}),
            "description": forms.Textarea(attrs={"class": "add-product-form-widget"}),
        }

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['customer_first_name', 'customer_last_name', 'delivery_address']

    def clean_delivery_address(self):
        address = self.cleaned_data['delivery_address']
        api_key = ""
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
        response = requests.get(url)
        data = response.json()
        # if not data.get("results"):
        #     raise forms.ValidationError("Address not found, try again.")
        if not data.get("results"):
            error = data.get("error_message", "Address not found, try again.")
            raise forms.ValidationError(error)
        return address
    
class SearchForm(forms.Form):
    search = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={
        'placeholder': 'Search...'
    }))
