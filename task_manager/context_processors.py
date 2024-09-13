from django.conf import settings
from django.http import HttpRequest


def cfg_assets_root(request: HttpRequest) -> dict:

    return {"ASSETS_ROOT": settings.ASSETS_ROOT}
