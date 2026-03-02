from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('full_name', 'email', 'username')


class PasswordResetForm(forms.Form):
    email = forms.EmailField(max_length=254)

    def clean(self):
        cleaned_data = super().clean()
        email = User.objects.normalize_email(cleaned_data.get('email'))

        if email and not User.objects.filter(email=email).exists():
            raise forms.ValidationError('User with this email address does not exist.')

        return cleaned_data
