import os
from pathlib import Path
from unittest import mock
from RiceClassifier.logger import logger
from RiceClassifier.utils.common import get_size

def test_get_size():
    # Define test data
    path = Path("test_file.txt")
    file_size = 2048  # 2 KB

    # Create a mock for the os.path.getsize function
    mock_getsize = mock.Mock()
    mock_getsize.return_value = file_size
    with mock.patch("RiceClassifier.utils.common.os.path.getsize", mock_getsize):
        # Call the get_size function
        result = get_size(path)

    # Assert that the os.path.getsize method was called with the correct path
    mock_getsize.assert_called_once_with(path)

    # Calculate the expected size string
    expected_result = f"~ {file_size // 1024} KB"  # Updated format without decimal part

    # Assert the result
    assert result == expected_result
