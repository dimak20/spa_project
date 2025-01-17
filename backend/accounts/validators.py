import re

from django.core.exceptions import ValidationError


def username_validator(value: str) -> None | ValidationError:
    if not re.match(r"^[a-zA-Z0-9_]+$", value):
        raise ValidationError(
            "Username can only contain letters, numbers, and underscores."
        )

    return None
