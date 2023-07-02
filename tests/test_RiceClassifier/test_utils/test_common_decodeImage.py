import base64
import pytest
from RiceClassifier.utils.common import decodeImage


def test_decodeImage(mocker):
    # Define test data
    imgstring = "SGVsbG8gV29ybGQh"  # Base64 encoded string
    fileName = "test_image.png"

    mock_open = mocker.mock_open()
    mocker.patch("RiceClassifier.utils.common.open", mock_open)

    # Call the decodeImage function
    decodeImage(imgstring, fileName)

    # Assert that the open and write methods were called with the correct arguments
    mock_open.assert_called_once_with(fileName, 'wb')
    mock_file = mock_open()
    mock_file.write.assert_called_once_with(base64.b64decode(imgstring))
