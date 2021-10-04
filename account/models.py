from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from store.models import Store
from django.db.models import Q


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    avatar = models.TextField(
        max_length=2000,  default='/media/default.png', null=True)
    role = models.TextField(
        max_length=2000,  default='staff', null=True)
    digit_token = models.TextField(
        max_length=2000,  default='staff', null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']
    store = models.ForeignKey(Store, related_name='staffs',
                              null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'auth_user'
        constraints = [
            models.UniqueConstraint(
                fields=['role', 'store'],
                condition=Q(role="Owner"),
                name='unique'
            )
        ]
