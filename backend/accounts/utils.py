import os
import uuid

from PIL import Image
from django.utils.text import slugify
from rest_framework.exceptions import ValidationError

MAX_PROFILE_IMAGE_WIDTH = 100
MAX_PROFILE_IMAGE_HEIGHT = 100


def user_image_profile_file_path(instance, filename) -> os.path:
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.id)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/users/", filename)


def resize_profile_image(image):
    image_path = image.path
    try:
        image = Image.open(image_path)

        if image.width > MAX_PROFILE_IMAGE_WIDTH or image.height > MAX_PROFILE_IMAGE_HEIGHT:
            output_size = (MAX_PROFILE_IMAGE_WIDTH, MAX_PROFILE_IMAGE_HEIGHT)
            image.thumbnail(output_size)
            image.save(image_path)
    except Exception as e:
        raise ValidationError(f"Failed to process the image: {e}")
