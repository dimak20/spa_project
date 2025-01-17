import os
import uuid

from django.utils.text import slugify


def user_image_profile_file_path(instance, filename) -> os.path:
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/users/", filename)
