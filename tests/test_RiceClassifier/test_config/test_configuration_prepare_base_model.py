import pytest
from pathlib import Path
from unittest.mock import MagicMock
from box import ConfigBox
from RiceClassifier.config.configuration import (
    ConfigReaderInterface,
    ConfigDirectoryCreatorInterface,
    ConfigurationManager,
    YAMLConfigReader,
    FilesystemDirectoryCreator,
    PrepareBaseModelConfig,
)


class MockConfigReader(ConfigReaderInterface):
    def read_config(self):
        return (
            ConfigBox({
            'artifacts_root': 'mock_root_dir',
            "prepare_base_model": {
                        "root_dir": "path/to/root_dir",
                        "base_model_path": "path/to/base_model",
                        "updated_base_model_path": "path/to/updated_base_model"
                    }
        }),
            ConfigBox(
                {
                    "IMAGE_SIZE": "image_size",
                    "LEARNING_RATE": "learning_rate",
                    "INCLUDE_TOP": "include_top",
                    "WEIGHTS": "weights",
                    "CLASSES": "classes",
                }
            ),
        )

class MockConfigDirectoryCreator(ConfigDirectoryCreatorInterface):
    def create_directories(self, paths):
        pass


@pytest.fixture
def mock_config_reader():
    return MockConfigReader()


@pytest.fixture
def mock_config_directory_creator():
    return MockConfigDirectoryCreator()


def test_get_prepare_base_model_config(mock_config_reader, mock_config_directory_creator):
    config_manager = ConfigurationManager(mock_config_reader, mock_config_directory_creator)
    prepare_base_model_config = config_manager.get_prepare_base_model_config()

    assert isinstance(prepare_base_model_config, PrepareBaseModelConfig)
    assert prepare_base_model_config.root_dir == Path("path/to/root_dir")
    assert prepare_base_model_config.base_model_path == Path("path/to/base_model")
    assert prepare_base_model_config.updated_base_model_path == Path("path/to/updated_base_model")
    assert prepare_base_model_config.params_image_size == "image_size"
    assert prepare_base_model_config.params_learning_rate == "learning_rate"
    assert prepare_base_model_config.params_include_top == "include_top"
    assert prepare_base_model_config.params_weights == "weights"
    assert prepare_base_model_config.params_classes == "classes"


if __name__ == "__main__":
    pytest.main([__file__])
