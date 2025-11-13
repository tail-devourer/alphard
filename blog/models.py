from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name = None
    last_name = None
    full_name = models.CharField(_("full name"), max_length=150, blank=True)
    avatar = models.ImageField(default="default.png")
    email = models.EmailField(_("email address"), unique=True)

    def get_full_name(self):
        return self.full_name.strip()

    def get_short_name(self):
        return self.full_name.strip()
