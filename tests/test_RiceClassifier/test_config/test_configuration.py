from unittest import mock
from box import ConfigBox
import pytest
from RiceClassifier.config.configuration import ConfigReaderInterface, ConfigurationManager, YAMLConfigReader,ConfigDirectoryCreatorInterface
from RiceClassifier.config.configuration import FilesystemDirectoryCreator
from RiceClassifier.entity.config_entity import DataIngestionConfig
from pathlib import Path
from unittest.mock import MagicMock

@pytest.fixture
def mock_read_yaml():
    with mock.patch("RiceClassifier.config.configuration.read_yaml") as mock_read_yaml:
        mock_read_yaml.side_effect = [
            {"config": "mock_config"},
            {"params": "mock_params"},
        ]
        yield mock_read_yaml


def test_yaml_config_reader(mock_read_yaml):
    config_reader = YAMLConfigReader()
    config, params = config_reader.read_config()
    assert config == {"config": "mock_config"}
    assert params == {"params": "mock_params"}


def test_yaml_config_reader_with_custom_paths(mock_read_yaml):
    config_filepath = "custom_config_path.yaml"
    params_filepath = "custom_params_path.yaml"
    config_reader = YAMLConfigReader(config_filepath, params_filepath)
    config, params = config_reader.read_config()
    assert config == {"config": "mock_config"}
    assert params == {"params": "mock_params"}


def test_yaml_config_reader_config_filepath(mock_read_yaml):
    config_filepath = "custom_config_path.yaml"
    params_filepath = "custom_params_path.yaml"
    config_reader = YAMLConfigReader(config_filepath, params_filepath)
    assert config_reader.config_filepath == "custom_config_path.yaml"


def test_yaml_config_reader_params_filepath(mock_read_yaml):
    config_filepath = "custom_config_path.yaml"
    params_filepath = "custom_params_path.yaml"
    config_reader = YAMLConfigReader(config_filepath, params_filepath)
    assert config_reader.params_filepath == "custom_params_path.yaml"

class MockDirectoryCreator:
    def create_directories(self, paths):
        pass

def test_filesystem_directory_creator(monkeypatch):
    mock_directory_creator = MockDirectoryCreator()
    paths = ["path1", "path2", "path3"]
    filesystem_creator = FilesystemDirectoryCreator()

    mock_create_directories = mock.Mock()
    monkeypatch.setattr(filesystem_creator, "create_directories", mock_create_directories)

    filesystem_creator.create_directories(paths)

    mock_create_directories.assert_called_once()
    mock_create_directories.assert_called_once_with(paths)


class MockConfigReaderInterface:
    def read_config(self):
        config = ConfigBox({
            'artifacts_root': 'mock_root_dir',
            'data_ingestion': {
                'root_dir': 'mock_data_root_dir',
                'source_URL': 'mock_source_URL',
                'local_data_file': 'mock_local_data_file',
                'unzip_dir': 'mock_unzip_dir'
            }
        })
        params = {}  # Mock parameters if needed
        return config, params


class MockConfigDirectoryCreatorInterface:
    def create_directories(self, paths):
        pass  # Mock directory creation


def test_get_data_ingestion_config():
    # Create an instance of ConfigurationManager with mocked dependencies
    config_reader = MockConfigReaderInterface()
    dir_creator = MockConfigDirectoryCreatorInterface()
    config_manager = ConfigurationManager(config_reader, dir_creator)

    # Call the method under test
    data_ingestion_config = config_manager.get_data_ingestion_config()

    # Assert the expected values
    assert isinstance(data_ingestion_config, DataIngestionConfig)
    assert data_ingestion_config.root_dir == 'mock_data_root_dir'
    assert data_ingestion_config.source_URL == 'mock_source_URL'
    assert data_ingestion_config.local_data_file == 'mock_local_data_file'
    assert data_ingestion_config.unzip_dir == 'mock_unzip_dir'



