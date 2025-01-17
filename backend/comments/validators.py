import re
from html import unescape

from django.core.exceptions import ValidationError

ALLOWED_TAGS = ["a", "code", "i", "strong"]
MAX_SIZE_KB = 100  # Max size (In Kilobytes!)

class XHTMLValidator:
    """Checks the comment text for prohibited tags"""

    def __init__(self, allowed_tags=None):
        self.allowed_tags = allowed_tags or ALLOWED_TAGS

    def __call__(self, value):
        if value:
            self.validate_xhtml(value)

    def validate_xhtml(self, value: str):
        allowed_tags_pattern = "|".join(self.allowed_tags)
        tag_pattern = rf"</?({allowed_tags_pattern})[^>]*>"

        if re.search(r"<[^>]*>", value):
            disallowed_tags = re.findall(
                r"<(?!/?(" + "|".join(self.allowed_tags) + r")[^>]*>)([^>]+)>", value
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
        raise ValidationError(
            f"The file size cannot exceed {MAX_SIZE_KB}KB."
        )
