from .models import Bid
from django import forms
from django.core.exceptions import ValidationError
from .models import Listing, User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match.")


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "Username"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )


class CreateListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description',
                  'starting_bid', 'image_url', 'category']

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter description'}),
            'starting_bid': forms.NumberInput(attrs={'placeholder': 'Starting bid'}),
            'image_url': forms.URLInput(attrs={'placeholder': 'Optional image URL'}),
            'category': forms.TextInput(attrs={'placeholder': 'Optional category (e.g. Fashion)'}),
        }


# Bid form
class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your bid'
            })
        }
