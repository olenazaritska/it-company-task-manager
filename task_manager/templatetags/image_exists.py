import os
from django import template

register = template.Library()


@register.filter
def image_exists(username: str) -> bool:
    image_path = f"static/assets/img/{username}.jpg"
    return os.path.exists(image_path)
