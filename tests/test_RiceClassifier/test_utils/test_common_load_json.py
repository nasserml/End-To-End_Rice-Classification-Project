import json
from pathlib import Path
from box import ConfigBox
from RiceClassifier.logger import logger
from pytest_mock import mocker

from RiceClassifier.utils.common import load_json

def test_load_json(mocker):
    # Define test data
    data = {"key1": "value1", "key2": "value2"}
    json_data = json.dumps(data)
    path = Path("test.json")

    # Create a mock for the logger
    mock_logger_info = mocker.patch.object(logger, "info")

    # Create a mock for the open function and configure it to return the test data
    mocker.patch("builtins.open", mocker.mock_open(read_data=json_data))

    # Call the load_json function
    result = load_json(path)

    # Assert that the logger.info method was called with the correct message
    # Assert that the logger.info method was called with the correct message
    mock_logger_info.assert_called_once_with(f"json file loaded succesfully from: {path}")


    # Assert that the result is an instance of ConfigBox
    assert isinstance(result, ConfigBox)

    # Assert that the result has the same content as the test data
    assert result.key1 == "value1"
    assert result.key2 == "value2"
