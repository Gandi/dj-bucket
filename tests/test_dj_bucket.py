from io import BytesIO

from django.test import TestCase

from dj_bucket.models import Bucket, BucketItem


class DjBucketTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.text = b"Hello World"
        cls.red_pixel = (
            b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00"
            b"\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\t"
            b"pHYs\x00\x00.#\x00\x00.#\x01x\xa5?v\x00\x00\x00\rIDAT\x08[c"
            b"\xf8\xcf\xc0\xf0\x1f\x00\x05\x00\x01\xff"
            b"\x17Qp\x06\x00\x00\x00\x00IEND\xaeB`\x82"
        )

    def test_upload_text(self):
        file_path = "file.txt"
        storage = Bucket()
        fd = BytesIO(self.text)

        name = storage.save(file_path, fd)
        self.assertEqual(file_path, name)

        fd = storage.open(name)
        self.assertEqual(self.text, fd.read())
        self.assertTrue(storage.exists(file_path))

        model = BucketItem.objects.first()
        self.assertIsNotNone(model)
        self.assertEqual(model.raw, self.text)  # type: ignore
        self.assertEqual(model.mimetype, "text/plain")  # type: ignore
        self.assertEqual(storage.size(name), len(self.text))

        self.assertEqual("/bucket/file.txt", storage.url(name))

    def test_upload_blob(self):
        file_path = "images/red_pixel.png"
        storage = Bucket()
        fd = BytesIO(self.red_pixel)

        name = storage.save(file_path, fd)
        self.assertEqual(file_path, name)

        fd = storage.open(name)
        self.assertEqual(self.red_pixel, fd.read())
        self.assertTrue(storage.exists(file_path))

        model = BucketItem.objects.first()
        self.assertIsNotNone(model)
        self.assertEqual(model.raw, self.red_pixel)  # type: ignore
        self.assertEqual(model.mimetype, "image/png")  # type: ignore
        self.assertEqual(storage.size(name), len(self.red_pixel))

        self.assertEqual("/bucket/images/red_pixel.png", storage.url(name))
