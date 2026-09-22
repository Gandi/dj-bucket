from django.urls import re_path

from .settings import BUCKET_PATH
from .views import dj_bucket

urlpatterns = [
    re_path(
        f"^{BUCKET_PATH}/(?P<name>.+)/?$",
        dj_bucket,
        name="dj_bucket",
    )
]
