"""Test utils."""
import os

from django.core.files.storage import default_storage
from django.core.files.uploadedfile import SimpleUploadedFile


def wipe_directory_recursive(directory):
    """Wipe the passed directory recursively."""
    dirs, files = default_storage.listdir(directory)
    for filename in files:
        default_storage.delete(os.path.join(directory, filename))
    for dirname in dirs:
        wipe_directory_recursive(os.path.join(directory, dirname))
    if directory:
        default_storage.delete(directory)


def add_binary_data(file_path, *, key, content_type, **kwargs):
    """Return the binary data."""
    with open(file_path, "rb") as fyle:
        file_name = fyle.name
        content = fyle.read()
    return {
        key: SimpleUploadedFile(file_name, content, content_type=content_type),
        **kwargs,
    }


def add_image_data(image_path, *, key="image", content_type="image/jpeg", **kwargs):
    """Return the image data."""
    return add_binary_data(
        file_path=image_path, key=key, content_type=content_type, **kwargs
    )
