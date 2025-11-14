from django.contrib.auth import forms
from .models import User


class CustomUserCreationForm(forms.UserCreationForm):

    class Meta:
        model = User
        fields = ('full_name', 'email', 'username')
