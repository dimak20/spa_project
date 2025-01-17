from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

from accounts.utils import user_image_profile_file_path
from accounts.validators import username_validator


class User(AbstractUser):
    username = models.CharField(
        _("username"),
        max_length=50,
        unique=True,
        validators=[username_validator]
    )
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(
        _("first name"),
        max_length=150,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        _("last name"),
        max_length=150,
        blank=True,
        null=True
    )
    bio = models.TextField(_("bio"), max_length=1000, null=True, blank=True)
    data_joined = models.DateTimeField(auto_now_add=True)
    profile_image = models.ImageField(
        upload_to=user_image_profile_file_path,
        null=True,
        blank=True
    )
    USERNAME_FIELD = "username"
