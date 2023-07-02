
import pytest
import os
from RiceClassifier.logger import logger
from RiceClassifier.utils.common import create_directories

@pytest.fixture
def mock_os_makedirs(mocker):
    return mocker.patch("os.makedirs")

@pytest.fixture
def mock_logger_info(mocker):
    return mocker.patch.object(logger, "info")

def test_create_directories(mock_os_makedirs, mock_logger_info):
    path_to_directories = ["dir1", "dir2", "dir3"]
    create_directories(path_to_directories, verbose=True)

    assert mock_os_makedirs.call_count == len(path_to_directories)
    for path in path_to_directories:
        mock_os_makedirs.assert_any_call(path, exist_ok=True)

    assert mock_logger_info.call_count == len(path_to_directories)
    for path in path_to_directories:
        mock_logger_info.assert_any_call(f"created directory at: {path}")