from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, Group


class CustomUser(AbstractUser):
    first_name = None
    last_name = None
    full_name = models.CharField(_('full name'), max_length=150, blank=True)
    avatar = models.ImageField(_('avatar'), default='default.jpg')
    email = models.EmailField(_('email address'), unique=True)
    email_verified_at = models.DateTimeField(_('email verified at'), blank=True, null=True)

    def get_full_name(self):
        return self.full_name.strip()

    def get_short_name(self):
        return self.full_name.strip()


class CustomGroup(Group):

    class Meta:
        proxy = True
        verbose_name = _('group')
        verbose_name_plural = _('groups')
