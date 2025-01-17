from django.db import models

from comments.validators import XHTMLValidator
from django.utils.translation import gettext as _

class Comment(models.Model):
    home_page = models.URLField(
        _("home page"),
        blank=True,
        null=True
    )
    text = models.TextField(
        _("text"),
        validators=[XHTMLValidator()])
