from io import BytesIO
from pathlib import Path

from django.http import (
    FileResponse,
    Http404,
    HttpRequest,
)

from .models import BucketItem


def dj_bucket(request: HttpRequest, name: str) -> FileResponse:
    item = BucketItem.objects.filter(path=name).first()
    if item:
        return FileResponse(BytesIO(item.raw), filename=Path(name).name)
    raise Http404
