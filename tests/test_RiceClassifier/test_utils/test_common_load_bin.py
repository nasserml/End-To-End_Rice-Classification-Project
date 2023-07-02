import pytest
from pathlib import Path
from unittest import mock
from RiceClassifier.logger import logger
from RiceClassifier.utils.common import load_bin

@pytest.fixture
def mock_logger_info(mocker):
    return mocker.patch.object(logger, "info")

def test_load_bin(mock_logger_info):
    # Define test data
    data = {"key1": "value1", "key2": "value2"}
    path = Path("test.bin")

    # Create a mock for the joblib.load function
    mock_joblib_load = mock.Mock()
    mock_joblib_load.return_value = data
    with mock.patch("RiceClassifier.utils.common.joblib.load", mock_joblib_load):
        # Call the load_bin function
        result = load_bin(path)

    # Assert that the joblib.load method was called with the correct path
    mock_joblib_load.assert_called_once_with(path)

    # Assert that the logger.info method was called with the correct message
    mock_logger_info.assert_called_once_with(f"binary file loaded from: {path}")

    # Assert the result
    assert result == data
