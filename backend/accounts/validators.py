import re

from django.core.exceptions import ValidationError

MAX_AVATAR_SIZE_KB = 200


def username_validator(value: str) -> None | ValidationError:
    if not re.match(r"^[a-zA-Z0-9_]+$", value):
        raise ValidationError(
            "Username can only contain letters, numbers, and underscores."
        )

    return None


def validate_avatar_size(value) -> None | ValidationError:
    if value.size > MAX_AVATAR_SIZE_KB * 1024:
        raise ValidationError(
            f"The image cannot exceed {MAX_AVATAR_SIZE_KB}KB."
        )

    return None
