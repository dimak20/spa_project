import re
from html import unescape

from django.core.exceptions import ValidationError

ALLOWED_TAGS = ["a", "code", "i", "strong"]
MAX_SIZE_KB = 100  # Max size (In Kilobytes!)


def xhtml_validator(value):
    """Checks the comment text for prohibited tags."""
    allowed_tags_pattern = "|".join(ALLOWED_TAGS)
    tag_pattern = rf"</?({allowed_tags_pattern})[^>]*>"

    if re.search(r"<[^>]*>", value):
        disallowed_tags = re.findall(
            r"<(?!/?(" + "|".join(ALLOWED_TAGS) + r")[^>]*>)([^>]+)>", value
        )
        if disallowed_tags:
            raise ValidationError(
                f"Not allowed tags: {', '.join(set(tag[1] for tag in disallowed_tags))}"
            )

    try:
        value_unescaped = unescape(value)
    except Exception as e:
        raise ValidationError(f"Error in XHTML markup: {e}")


def validate_file_size(value):
    """Checks the size of the downloaded file."""
    if value.size > MAX_SIZE_KB * 1024:
        raise ValidationError(f"The file size cannot exceed {MAX_SIZE_KB}KB.")
