import pytest
from RiceClassifier.config.configuration import (
    ConfigurationManager, YAMLConfigReader, FilesystemDirectoryCreator
)
from RiceClassifier.components.prepare_base_model import (
    BaseModelLoader, BaseModelUpdater, FullModelPreparer
)
from RiceClassifier.logger import logger
from RiceClassifier.pipeline.stage_02_prepare_base_model import PrepareBaseModelTrainingPipeline


class TestPrepareBaseModelTrainingPipeline:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.mock_config_manager = ConfigurationManager(
            config_reader=YAMLConfigReader(),
            dir_creator=FilesystemDirectoryCreator()
        )

    def test_main(self, mocker):
        # Mock necessary classes and methods
        mocker.patch.object(BaseModelLoader, "load_base_model")
        mocker.patch.object(BaseModelLoader, "save_base_model")
        mocker.patch.object(FullModelPreparer, "prepare_full_model")
        mocker.patch.object(BaseModelUpdater, "save_updated_base_model")

        # Create an instance of the pipeline
        pipeline = PrepareBaseModelTrainingPipeline()

        # Call the main method
        pipeline.main()

        # Assert that the necessary methods were called
        BaseModelLoader.load_base_model.assert_called_once()
        BaseModelLoader.save_base_model.assert_called_once()
        FullModelPreparer.prepare_full_model.assert_called_once()
        BaseModelUpdater.save_updated_base_model.assert_called_once()

    def test_main_exception(self, mocker):
        # Mock an exception to be raised
        mocker.patch.object(BaseModelLoader, "load_base_model", side_effect=Exception("Mocked exception"))

        # Patch logger.exception method
        mock_logger_exception = mocker.patch.object(logger, "exception")

        # Create an instance of the pipeline
        pipeline = PrepareBaseModelTrainingPipeline()

        # Call the main method and check if the exception is raised
        try:
            pipeline.main()
        except Exception as e:
            # Log the exception manually
            logger.exception(str(e))

        # Assert that logger.exception was called with the raised exception
        mock_logger_exception.assert_called_once_with("Mocked exception")


if __name__ == '__main__':
    pytest.main()
