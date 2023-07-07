




from RiceClassifier.components.data_preprocessing import ImageDataProcessor, PickleFileManager, ProcessedData
from RiceClassifier.config.configuration import ConfigurationManager, FilesystemDirectoryCreator, YAMLConfigReader
from RiceClassifier.logger import logger

STAGE_NAME = 'Data Preprocessing Stage'

class DataPreprocessingPipeline:
    def __init__(self):
        pass
    
    def main(self):
        config_reader = YAMLConfigReader()
        dir_creator = FilesystemDirectoryCreator()
        config = ConfigurationManager(config_reader,dir_creator)
        processed_data_config = config.get_processed_data_config()
        image_processor = ImageDataProcessor(processed_data_config)
        pickle_manager = PickleFileManager()
        processed_data = ProcessedData(config=processed_data_config, image_processor=image_processor, pickle_manager=pickle_manager)
        processed_data.get_process_data()
    
# Usage:
if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataPreprocessingPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e