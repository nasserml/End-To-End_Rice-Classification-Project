import pytest
from dataclasses import dataclass
from pathlib import Path
from RiceClassifier.entity.config_entity import (
    PathConfig,
    DataIngestionConfig,
    PrepareBaseModelConfig,
    PrepareCallbacksConfig,
    TrainingConfig,
    EvaluationConfig,
)


@pytest.fixture
def root_dir():
    return Path("/path/to/root")


@pytest.fixture
def data_ingestion_config(root_dir):
    return DataIngestionConfig(
        root_dir=root_dir,
        source_URL="https://example.com",
        local_data_file=Path("data.csv"),
        unzip_dir=Path("unzip"),
    )


@pytest.fixture
def base_model_config(root_dir):
    return PrepareBaseModelConfig(
        root_dir=root_dir,
        base_model_path=Path("base_model.h5"),
        updated_base_model_path=Path("updated_model.h5"),
        params_image_size=[224, 224],
        params_learning_rate=0.001,
        params_include_top=True,
        params_weights="imagenet",
        params_classes=1000,
    )


@pytest.fixture
def callbacks_config(root_dir):
    return PrepareCallbacksConfig(
        root_dir=root_dir,
        tensorboard_root_log_dir=Path("logs"),
        checkpoint_model_filepath=Path("checkpoint.h5"),
    )


@pytest.fixture
def training_config(root_dir):
    return TrainingConfig(
        root_dir=root_dir,
        trained_model_path=Path("trained_model.h5"),
        updated_base_model_path=Path("updated_model.h5"),
        training_data=Path("train_data"),
        params_epochs=10,
        params_batch_size=32,
        params_is_augmentation=True,
        params_image_size=[224, 224],
    )


@pytest.fixture
def evaluation_config(root_dir):
    return EvaluationConfig(
        root_dir=root_dir,
        path_of_model=Path("model.h5"),
        training_data=Path("train_data"),
        all_params={"param1": 1, "param2": 2},
        params_image_size=[224, 224],
        params_batch_size=32,
    )


def test_data_ingestion_config(data_ingestion_config, root_dir):
    assert isinstance(data_ingestion_config, DataIngestionConfig)
    assert isinstance(data_ingestion_config, PathConfig)
    assert data_ingestion_config.root_dir == root_dir
    assert data_ingestion_config.source_URL == "https://example.com"
    assert data_ingestion_config.local_data_file == Path("data.csv")
    assert data_ingestion_config.unzip_dir == Path("unzip")


def test_base_model_config(base_model_config, root_dir):
    assert isinstance(base_model_config, PrepareBaseModelConfig)
    assert isinstance(base_model_config, PathConfig)
    assert base_model_config.root_dir == root_dir
    assert base_model_config.base_model_path == Path("base_model.h5")
    assert base_model_config.updated_base_model_path == Path("updated_model.h5")
    assert base_model_config.params_image_size == [224, 224]
    assert base_model_config.params_learning_rate == 0.001
    assert base_model_config.params_include_top is True
    assert base_model_config.params_weights == "imagenet"
    assert base_model_config.params_classes == 1000


def test_callbacks_config(callbacks_config, root_dir):
    assert isinstance(callbacks_config, PrepareCallbacksConfig)
    assert isinstance(callbacks_config, PathConfig)
    assert callbacks_config.root_dir == root_dir
    assert callbacks_config.tensorboard_root_log_dir == Path("logs")
    assert callbacks_config.checkpoint_model_filepath == Path("checkpoint.h5")


def test_training_config(training_config, root_dir):
    assert isinstance(training_config, TrainingConfig)
    assert isinstance(training_config, PathConfig)
    assert training_config.root_dir == root_dir
    assert training_config.trained_model_path == Path("trained_model.h5")
    assert training_config.updated_base_model_path == Path("updated_model.h5")
    assert training_config.training_data == Path("train_data")
    assert training_config.params_epochs == 10
    assert training_config.params_batch_size == 32
    assert training_config.params_is_augmentation is True
    assert training_config.params_image_size == [224, 224]


def test_evaluation_config(evaluation_config):
    assert isinstance(evaluation_config, EvaluationConfig)
    assert isinstance(evaluation_config, PathConfig)
    assert evaluation_config.path_of_model == Path("model.h5")
    assert evaluation_config.training_data == Path("train_data")
    assert evaluation_config.all_params == {"param1": 1, "param2": 2}
    assert evaluation_config.params_image_size == [224, 224]
    assert evaluation_config.params_batch_size == 32
