from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('full_name', 'email', 'username')


class PasswordResetForm(forms.Form):
    email = forms.EmailField(max_length=254)

    def clean(self):
        User = get_user_model()

        cleaned_data = super().clean()
        email = cleaned_data.get("email")

        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("User with this email address does not exist.")

        return cleaned_data


class PasswordResetConfirmForm(forms.Form):
    password1 = forms.CharField(
        help_text=password_validation.password_validators_help_text_html()
    )
    password2 = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn’t match.")

        return cleaned_data
