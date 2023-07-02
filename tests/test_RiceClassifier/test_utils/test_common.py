import pytest
from box.exceptions import BoxValueError
from box import ConfigBox
from pathlib import Path
from RiceClassifier.utils.common import read_yaml


@pytest.fixture
def valid_yaml_file(tmp_path):
    yaml_content = """
    key1: value1
    key2: value2
    """
    file_path = tmp_path / "config.yaml"
    with open(file_path, "w") as f:
        f.write(yaml_content)
    return file_path


@pytest.fixture
def empty_yaml_file(tmp_path):
    file_path = tmp_path / "empty.yaml"
    with open(file_path, "w") as f:
        pass
    return file_path


def test_read_yaml_valid_file(valid_yaml_file):
    config = read_yaml(valid_yaml_file)
    assert isinstance(config, ConfigBox)
    assert config.key1 == "value1"
    assert config.key2 == "value2"


def test_read_yaml_empty_file(empty_yaml_file):
    with pytest.raises(ValueError) as exc_info:
        read_yaml(empty_yaml_file)
    assert str(exc_info.value) == "yaml file is empty"


def test_read_yaml_nonexistent_file():
    non_existent_file = Path("non_existent.yaml")
    with pytest.raises(FileNotFoundError):
        read_yaml(non_existent_file)


