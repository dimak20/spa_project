import re
from django.core.exceptions import ValidationError
from html import unescape

ALLOWED_TAGS = ["a", "code", "i", "strong"]


class XHTMLValidator:
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
