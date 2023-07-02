import pytest
import json
from RiceClassifier.logger import logger
from RiceClassifier.utils.common import save_json
from pathlib import Path


@pytest.fixture
def json_data(tmp_path):
    data = {
        "key1": "value1",
        "key2": "value2"
    }
    file_path = tmp_path / "data.json"
    return data, file_path


def test_save_json(json_data, mocker):
    data, file_path = json_data

    mock_open = mocker.patch("builtins.open", mocker.mock_open())
    mock_json_dump = mocker.patch("json.dump")
    mock_logger_info = mocker.patch.object(logger, "info")

    save_json(file_path, data)

    mock_open.assert_called_once_with(file_path, "w")
    mock_json_dump.assert_called_once_with(data, mock_open.return_value.__enter__.return_value, indent=4)
    mock_logger_info.assert_called_once_with(f"json file saved at: {file_path}")


def test_save_json_invalid_file_path(json_data):
    data, file_path = json_data

    # Modify file_path to an invalid path
    file_path = Path("non_existent_path/data.json")

    with pytest.raises(FileNotFoundError):
        save_json(file_path, data)
