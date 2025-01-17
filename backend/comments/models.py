from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import CASCADE
from django.utils.translation import gettext as _

from comments.utils import comment_image_file_path, comment_text_file_path, resize_image
from comments.validators import xhtml_validator, validate_file_size


class Comment(models.Model):
    home_page = models.URLField(
        _("home page"),
        blank=True,
        null=True
    )
    text = models.TextField(
        _("text"),
        validators=[xhtml_validator])
    user = models.ForeignKey(
        get_user_model(),
        on_delete=CASCADE,
        related_name="comments"
    )
    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _("updated at"),
        auto_now=True
    )
    attached_image = models.ImageField(
        _("attached image"),
        upload_to=comment_image_file_path,
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    "jpg", "gif", "png"
                ]
            )
        ],
        blank=True,
        null=True
    )
    attached_file = models.FileField(
        _("attached file"),
        upload_to=comment_text_file_path,
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    "txt"
                ]
            ),
            validate_file_size
        ],
        blank=True,
        null=True
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="replies",
        blank=True,
        null=True,
        verbose_name=_("parent comment")
    )

    def __str__(self):
        return f"Comment by {self.user} on {self.created_at}"

    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.attached_image:
            resize_image(self.attached_image)
