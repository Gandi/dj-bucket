# dj-bucket

Store blobs into a database table.

## Setup

In your configuration add the dj-bucket app to the installed apps:

```python
INSTALLED_APPS: = [
    "dj_bucket",
]

# Bucket base path no starting and no ending slash
BUCKET_PATH="bucket"
```

Then make sure a database backend is setup, for testing you can use the SQLite:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

Add the bucket URL to your `urls.py`:

```python
from dj_bucket.urls import urlpatterns as dj_bucket_urls

urlpatterns = [
    path("", include(dj_bucket_urls)),
    ...
]
```

Run the Django database migrations to create the table that will store the
blobs.

## Wagtail

With wagtail you need to declare the storage in the `STORAGES` variable:

```python
STORAGES = {
    "default": {
        "BACKEND": "dj_bucket.models.Bucket",
    }
}
```
