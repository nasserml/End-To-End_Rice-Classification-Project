from RiceClassifier.config.configuration import (ConfigurationManager,YAMLConfigReader,FilesystemDirectoryCreator)
from RiceClassifier.components.data_ingestion import (DataIngestion,FileDownloader,ZipExtractor)
from RiceClassifier.logger import logger


STAGE_NAME = "Data Ingestion stage"

class DataIngestionTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config_reader = YAMLConfigReader()
        dir_creator = FilesystemDirectoryCreator()
        config_manger = ConfigurationManager(config_reader,dir_creator)
        data_ingestion_config = config_manger.get_data_ingestion_config()
        
        download_manger = FileDownloader(data_ingestion_config)
        zip_extractor = ZipExtractor(data_ingestion_config)
        
        download_manger.download_file()
        zip_extractor.extract_zip_file()



if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataIngestionTrainingPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e