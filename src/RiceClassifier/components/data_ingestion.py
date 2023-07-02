
from abc import ABC, abstractmethod
import os
import urllib.request as request
import zipfile
from RiceClassifier.logger import logger
from RiceClassifier.utils.common import get_size
from RiceClassifier.entity.config_entity import DataIngestionConfig
from pathlib import Path

class FileDownloaderInterface(ABC):
    @abstractmethod
    def download_file(self):
        pass


class ZipExtractorInterface(ABC):
    @abstractmethod
    def extract_zip_file(self):
        pass


class FileDownloader(FileDownloaderInterface):
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            filename, headers = request.urlretrieve(
                url=self.config.source_URL,
                filename=self.config.local_data_file
            )
            logger.info(f"{filename} downloaded! Following info:\n{headers}")
        else:
            logger.info(f"File already exists of size: {get_size(Path(self.config.local_data_file))}")


class ZipExtractor(ZipExtractorInterface):
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def extract_zip_file(self):
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)



class DataIngestion:
    def __init__(self, config: DataIngestionConfig,
                 file_downloader: FileDownloaderInterface,
                 zip_extractor: ZipExtractorInterface):
        self.config = config
        self.file_downloader = file_downloader
        self.zip_extractor = zip_extractor

    def ingest_data(self):
        self.file_downloader.download_file()
        self.zip_extractor.extract_zip_file()
