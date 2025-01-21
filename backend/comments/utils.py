import json
import os
import uuid

import requests
from PIL import Image
from django.conf import settings
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.utils.text import slugify

MAX_IMAGE_WIDTH = 320
MAX_IMAGE_HEIGHT = 240


def comment_image_file_path(instance, filename: str) -> os.path:
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.id)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/comments/images", filename)


def comment_text_file_path(instance, filename: str) -> os.path:
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.id)}-{uuid.uuid4()}{extension}"

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


def verify_recaptcha(token):
    url = "https://www.google.com/recaptcha/api/siteverify"
    payload = {
        "secret": settings.RECAPTCHA_SECRET_KEY,
        "response": token,
    }
    response = requests.post(url, data=payload)
    return response.json()


def submit_comment(request):
    if request.method == "POST":
        data = json.loads(request.body)
        recaptcha_token = data.get("recaptcha")

        result = verify_recaptcha(recaptcha_token)
        if not result.get("success"):
            return JsonResponse({"error": "Invalid reCAPTCHA"}, status=400)

        return JsonResponse({"message": "Comment submitted successfully"})


def generate_key(request, *args, **kwargs):
    return "comment_list"
