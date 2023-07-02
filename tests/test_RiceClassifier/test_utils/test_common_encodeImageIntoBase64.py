import base64
import pytest
from RiceClassifier.utils.common import encodeImageIntoBase64


def test_encodeImageIntoBase64(tmpdir):
    # Create a temporary file with some content
    image_path = tmpdir.join("test_image.png")
    image_path.write(b"Hello, World!")

    # Call the encodeImageIntoBase64 function
    result = encodeImageIntoBase64(str(image_path))

    # Convert the result from bytes to string
    result = result.decode()

    # Assert that the result is a base64 encoded string
    assert isinstance(result, str)
    assert isinstance(base64.b64decode(result.encode()), bytes)

    # Assert that the decoded content matches the original content
    assert base64.b64decode(result.encode()) == b"Hello, World!"
