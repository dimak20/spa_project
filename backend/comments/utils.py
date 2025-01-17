import os
import uuid

from PIL import Image
from django.core.exceptions import ValidationError
from django.utils.text import slugify

MAX_IMAGE_WIDTH = 320
MAX_IMAGE_HEIGHT = 240


def comment_image_file_path(instance, filename: str) -> os.path:
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/comments/images", filename)


def comment_text_file_path(instance, filename: str) -> os.path:
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/comments/files", filename)


def resize_image(image):
    image_path = image.path
    try:
        image = Image.open(image_path)

        if image.width > MAX_IMAGE_WIDTH or image.height > MAX_IMAGE_HEIGHT:
            output_size = (MAX_IMAGE_WIDTH, MAX_IMAGE_HEIGHT)
            image.thumbnail(output_size)
            image.save(image_path)
    except Exception as e:
        raise ValidationError(f"Failed to process the image: {e}")
