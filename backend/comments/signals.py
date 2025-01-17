import os

from django.db.models.signals import pre_delete
from django.dispatch import receiver

from comments.models import Comment


@receiver(pre_delete, sender=Comment)
def delete_attached_image(sender, instance: Comment, **kwargs):
    """Deletes the image/txt file, if it exists, before deleting the object."""
    if instance.attached_image:
        if os.path.isfile(instance.attached_image.path):
            os.remove(instance.attached_image.path)
    if instance.attached_file:
        if os.path.isfile(instance.attached_file.path):
            os.remove(instance.attached_file.path)
