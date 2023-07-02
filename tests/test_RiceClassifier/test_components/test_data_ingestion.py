import pytest
from unittest.mock import MagicMock
from RiceClassifier.entity.config_entity import DataIngestionConfig
from RiceClassifier.components.data_ingestion import FileDownloader, ZipExtractor, DataIngestion


@pytest.fixture
def mock_file_downloader():
    return MagicMock()


@pytest.fixture
def mock_zip_extractor():
    return MagicMock()


@pytest.fixture
def data_ingestion_config():
    return DataIngestionConfig(
        source_URL="http://example.com/data.zip",
        local_data_file="/path/to/data.zip",
        unzip_dir="/path/to/unzip",
        root_dir="/path/to/root"  # Add the root_dir argument here
    )


def test_data_ingestion(mock_file_downloader, mock_zip_extractor, data_ingestion_config):
    data_ingestion = DataIngestion(data_ingestion_config, mock_file_downloader, mock_zip_extractor)
    data_ingestion.ingest_data()

    mock_file_downloader.download_file.assert_called_once()
    mock_zip_extractor.extract_zip_file.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__])
