from RiceClassifier.config.configuration import (ConfigurationManager,YAMLConfigReader,FilesystemDirectoryCreator)
from RiceClassifier.components.prepare_base_model import BaseModelLoader, BaseModelUpdater, FullModelPreparer
from RiceClassifier.logger import logger


STAGE_NAME = "Prepare base model"

class PrepareBaseModelTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config_reader = YAMLConfigReader()
        dir_creator = FilesystemDirectoryCreator()
        config_manager = ConfigurationManager(config_reader,dir_creator)
        prepare_base_model_config = config_manager.get_prepare_base_model_config()

        base_model_loader = BaseModelLoader(prepare_base_model_config)
        base_model = base_model_loader.load_base_model(prepare_base_model_config)
        base_model_loader.save_base_model(base_model)

        full_model_preparer = FullModelPreparer(prepare_base_model_config)
        full_model = full_model_preparer.prepare_full_model(
            base_model=base_model,
            classes=prepare_base_model_config.params_classes,
            freeze_all=True,
            freeze_till=None,
            learning_rate=prepare_base_model_config.params_learning_rate
        )

        base_model_updater = BaseModelUpdater(prepare_base_model_config)
        base_model_updater.save_updated_base_model(full_model)





if __name__ == '__main__':
    try:
        logger.info(f"*******************")
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = PrepareBaseModelTrainingPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e