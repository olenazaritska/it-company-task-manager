import os
from django import template
from django.conf import settings

register = template.Library()


@register.filter
def image_exists(username):
    image_path = f"static/assets/img/{username}.jpg"
    return os.path.exists(image_path)
