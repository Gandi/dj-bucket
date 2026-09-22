import mimetypes
from datetime import datetime
from io import BytesIO, StringIO
from urllib.parse import urljoin

from django.core.files import File
from django.core.files.storage import Storage
from django.db import models
from django.utils.deconstruct import deconstructible
from django.utils.encoding import filepath_to_uri
from django.utils.timezone import now

from .settings import BUCKET_PATH


class BucketItem(models.Model):
    raw = models.BinaryField()
    path = models.CharField(max_length=255, unique=True)
    mimetype = models.CharField(max_length=64)
    accessed_at = models.DateTimeField()
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()


@deconstructible(path="gcs.infrastructure.dj_bucket.models.Bucket")
class Bucket(Storage):
    def _open(self, name: str, mode: str) -> StringIO | BytesIO:
        # Figure out if mode should be handled
        if mode.startswith("w"):
            if "b" in mode:
                return BytesIO()
            return StringIO()
        elif mode.startswith("r"):
            item = BucketItem.objects.filter(path=name).first()
            if not item:
                raise FileNotFoundError(f"No such file: {name}")
            if "b" in mode:
                return BytesIO(item.raw)
        return StringIO(item.raw.decode("utf-8"))

    def _save(self, name: str, content: File) -> str:
        raw = content.read()
        content_type, _ = mimetypes.guess_type(name)
        current_dt = now()
        _, created = BucketItem.objects.update_or_create(
            path=name,
            defaults={
                "path": name,
                "raw": raw,
                "mimetype": content_type,
                "accessed_at": current_dt,
                "created_at": current_dt,
                "modified_at": current_dt,
            },
        )
        if not created:
            raise ValueError(f"Could not save upload '{name}' ({content_type})")
        return name

    def delete(self, name: str) -> None:
        """
        Delete the specified file from the storage system.
        """
        BucketItem.objects.filter(path=name).delete()

    @property
    def base_url(self) -> str:
        return f"/{BUCKET_PATH}"

    def exists(self, name: str) -> bool:
        """
        Return True if a file referenced by the given name already exists in the
        storage system, or False if the name is available for a new file.
        """
        return bool(BucketItem.objects.filter(path=name).count())

    def size(self, name: str) -> int:
        """
        Return the total size, in bytes, of the file specified by name.
        """
        item = (
            BucketItem.objects.annotate(
                raw_length=models.Func("raw", function="OCTET_LENGTH")
            )
            .values("raw_length")
            .first()
        )
        if item:
            return item["raw_length"]
        raise FileNotFoundError(f"No such file: {name}")

    def url(self, name: str) -> str:
        """
        Return an absolute URL where the file's contents can be accessed
        directly by a web browser.
        """
        item = BucketItem.objects.filter(path=name).first()
        if item:
            url = filepath_to_uri(item.path)
            return urljoin(self.base_url, url)
        raise FileNotFoundError(f"No such file: {name}")

    def get_accessed_time(self, name: str) -> datetime:
        """
        Return the last accessed time (as a datetime) of the file specified by
        name. The datetime will be timezone-aware if USE_TZ=True.
        """
        item = BucketItem.objects.filter(path=name).first()
        if item:
            return item.accessed_at
        raise FileNotFoundError(f"No such file: {name}")

    def get_created_time(self, name: str) -> datetime:
        """
        Return the creation time (as a datetime) of the file specified by name.
        The datetime will be timezone-aware if USE_TZ=True.
        """
        item = BucketItem.objects.filter(path=name).first()
        if item:
            return item.created_at
        raise FileNotFoundError(f"No such file: {name}")

    def get_modified_time(self, name: str) -> datetime:
        """
        Return the last modified time (as a datetime) of the file specified by
        name. The datetime will be timezone-aware if USE_TZ=True.
        """
        item = BucketItem.objects.filter(path=name).first()
        if item:
            return item.modified_at
        raise FileNotFoundError(f"No such file: {name}")
