from django.urls import re_path

from .views import dj_bucket
from .settings import BUCKET_PATH

urlpatterns = [
    re_path(
        "/".join([BUCKET_PATH, "(?P<name>.+)/?$"]),
        dj_bucket,
        name="dj_bucket",
    )
]
