
 
from abc import ABC, abstractmethod
from RiceClassifier.constants import *
from RiceClassifier.utils.common import read_yaml, create_directories
from RiceClassifier.entity.config_entity import DataIngestionConfig, PrepareBaseModelConfig, PrepareCallbacksConfig
import os

class ConfigReaderInterface(ABC):
    @abstractmethod
    def read_config(self):
        pass


class ConfigDirectoryCreatorInterface(ABC):
    @abstractmethod
    def create_directories(self, paths):
        pass

class YAMLConfigReader(ConfigReaderInterface):
    def __init__(self, config_filepath=CONFIG_FILE_PATH, params_filepath=PARAMS_FILE_PATH):
        self.config_filepath = config_filepath
        self.params_filepath = params_filepath

    def read_config(self):
        return read_yaml(self.config_filepath), read_yaml(self.params_filepath)


class FilesystemDirectoryCreator(ConfigDirectoryCreatorInterface):
    def create_directories(self, paths):
        create_directories(paths)


class ConfigurationManager:
    
    
    def __init__(
        self,
        config_reader: ConfigReaderInterface ,
        dir_creator: ConfigDirectoryCreatorInterface
    ):
        self.config_reader = config_reader
        self.dir_creator = dir_creator
        config, params = self.config_reader.read_config()
        self.config = config
        self.params = params
        self.dir_creator.create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        self.dir_creator.create_directories([config.root_dir])
        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir
        )
        return data_ingestion_config
    
    def get_prepare_base_model_config(self) -> PrepareBaseModelConfig:
        config = self.config.prepare_base_model

        create_directories([config.root_dir])

        prepare_base_model_config = PrepareBaseModelConfig(
            root_dir=Path(config.root_dir),
            base_model_path=Path(config.base_model_path),
            updated_base_model_path=Path(config.updated_base_model_path),
            params_image_size=self.params.IMAGE_SIZE,
            params_learning_rate=self.params.LEARNING_RATE,
            params_include_top=self.params.INCLUDE_TOP,
            params_weights=self.params.WEIGHTS,
            params_classes=self.params.CLASSES
        )

        return prepare_base_model_config
    
    
    
    def get_prepare_callback_config(self) -> PrepareCallbacksConfig:
        config = self.config.prepare_callbacks
        model_ckpt_dir = os.path.dirname(config.checkpoint_model_filepath)
        create_directories([
            Path(model_ckpt_dir),
            Path(config.tensorboard_root_log_dir)
        ])

        prepare_callback_config = PrepareCallbacksConfig(
            root_dir=Path(config.root_dir),
            tensorboard_root_log_dir=Path(config.tensorboard_root_log_dir),
            checkpoint_model_filepath=Path(config.checkpoint_model_filepath)
        )

        return prepare_callback_config
    



