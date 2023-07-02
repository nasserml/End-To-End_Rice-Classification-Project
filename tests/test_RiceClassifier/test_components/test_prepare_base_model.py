import pytest
from unittest.mock import MagicMock
import tensorflow as tf
from RiceClassifier.entity.config_entity import PrepareBaseModelConfig
from RiceClassifier.components.prepare_base_model import (
    BaseModelLoader,
    FullModelPreparer,
    BaseModelUpdater
)

@pytest.fixture
def prepare_base_model_config():
    return PrepareBaseModelConfig(
        root_dir="/path/to/root_dir",
        params_image_size=(224, 224, 3),
        params_weights="imagenet",
        params_include_top=False,
        params_learning_rate=0.001,
        params_classes=10,
        base_model_path="/path/to/base_model.h5",
        updated_base_model_path="/path/to/updated_base_model.h5"
    )



def test_base_model_loader(prepare_base_model_config):
    base_model_loader = BaseModelLoader(prepare_base_model_config)
    base_model = base_model_loader.load_base_model(prepare_base_model_config)

    assert isinstance(base_model, tf.keras.Model)


def test_full_model_preparer(prepare_base_model_config):
    full_model_preparer = FullModelPreparer(prepare_base_model_config)
    base_model = tf.keras.applications.mobilenet_v2.MobileNetV2()
    classes = 10
    freeze_all = False
    freeze_till = None
    learning_rate = 0.001
    full_model = full_model_preparer.prepare_full_model(base_model, classes, freeze_all, freeze_till, learning_rate)

    assert isinstance(full_model, tf.keras.Model)


def test_base_model_updater(prepare_base_model_config):
    base_model_updater = BaseModelUpdater(prepare_base_model_config)
    model = tf.keras.applications.mobilenet_v2.MobileNetV2()
    base_model_updater.save_updated_base_model(model)

    # Check if the updated base model file exists
    assert tf.keras.models.load_model(prepare_base_model_config.updated_base_model_path)


if __name__ == "__main__":
    pytest.main([__file__])
