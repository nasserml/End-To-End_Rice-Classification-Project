import os
import json
from pathlib import Path
from unittest import mock
import joblib
from box import ConfigBox
from pytest_mock import mocker

from RiceClassifier.logger import logger
from RiceClassifier.utils.common import save_bin


def test_save_bin(mocker):
    # Define test data
    data = {"key1": "value1", "key2": "value2"}
    path = Path("test.bin")

    # Create a mock for the logger
    mock_logger_info = mocker.patch.object(logger, "info")

    # Create a mock for the joblib.dump function
    mock_joblib_dump = mocker.patch.object(joblib, "dump")

    # Call the save_bin function
    save_bin(data, path)

    # Assert that the joblib.dump function was called with the correct arguments
    mock_joblib_dump.assert_called_once_with(value=data, filename=path)

    # Assert that the logger.info method was called with the correct message
    mock_logger_info.assert_called_once_with(f"binary file saved at: {path}")
