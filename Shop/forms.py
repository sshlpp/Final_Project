from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Product, SwapedUser

class RegistForm(UserCreationForm):
    seller = forms.BooleanField(
        required=False,
        label="Я хочу продавать вещи",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )
    class Meta:
        model = SwapedUser
        fields = ["username", "password1", "password2", "seller"]
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "reg-form",
                "placeholder": "Enter username"
            }),
            "password1": forms.PasswordInput(attrs={
                "class": "form-control",
                "placeholder": "Enter password"
            }),
            "password2": forms.PasswordInput(attrs={
                "class": "form-control",
                "placeholder": "Confirm your password"
            }),
        }


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["image", "name", "brand", "size", "product_type", "description", "price"]
        widgets = {
            "image": forms.ClearableFileInput(attrs={"class": "add-product-form-widget"}),
            "name": forms.TextInput(attrs={"class": "add-product-form-widget"}),
            "brand": forms.TextInput(attrs={"class": "add-product-form-widget"}),
            "size": forms.TextInput(attrs={"class": "add-product-form-widget"}),
            "product_type": forms.TextInput(attrs={"class": "add-product-form-widget"}),
            "description": forms.Textarea(attrs={"class": "add-product-form-widget"}),
        }