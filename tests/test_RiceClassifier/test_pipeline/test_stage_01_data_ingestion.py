import pytest
from unittest.mock import MagicMock
from RiceClassifier.config.configuration import ConfigurationManager, YAMLConfigReader, FilesystemDirectoryCreator
from RiceClassifier.components.data_ingestion import  FileDownloader, ZipExtractor
from RiceClassifier.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline


@pytest.fixture
def mock_config_manager():
    return MagicMock(spec=ConfigurationManager)


@pytest.fixture
def mock_data_ingestion_config():
    return MagicMock()


@pytest.fixture
def mock_file_downloader():
    return MagicMock(spec=FileDownloader)


@pytest.fixture
def mock_zip_extractor():
    return MagicMock(spec=ZipExtractor)


class DataIngestionTrainingPipeline:
    def __init__(self):
        self.config_manager = None
        self.file_downloader = None
        self.zip_extractor = None

    def main(self):
        data_ingestion_config = self.config_manager.get_data_ingestion_config()
        self.file_downloader.download_file(data_ingestion_config.file_url)
        self.zip_extractor.extract_zip_file(data_ingestion_config.zip_file_path)


def test_data_ingestion_pipeline(mock_config_manager, mock_data_ingestion_config, mock_file_downloader,
                                mock_zip_extractor):
    mock_config_manager.get_data_ingestion_config.return_value = mock_data_ingestion_config

    pipeline = DataIngestionTrainingPipeline()
    pipeline.config_manager = mock_config_manager
    pipeline.file_downloader = mock_file_downloader
    pipeline.zip_extractor = mock_zip_extractor

    pipeline.main()

    mock_config_manager.get_data_ingestion_config.assert_called_once()
    mock_file_downloader.download_file.assert_called_once()
    mock_zip_extractor.extract_zip_file.assert_called_once()


if __name__ == "__main__":
    mock_config_manager = MagicMock(spec=ConfigurationManager)
    mock_data_ingestion_config = MagicMock()
    mock_file_downloader = MagicMock(spec=FileDownloader)
    mock_zip_extractor = MagicMock(spec=ZipExtractor)

    test_data_ingestion_pipeline(mock_config_manager, mock_data_ingestion_config, mock_file_downloader,
                                mock_zip_extractor)
