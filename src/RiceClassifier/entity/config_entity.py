from dataclasses import dataclass
from pathlib import Path

from abc import ABC, abstractmethod


@dataclass(frozen=True)
class PathConfig(ABC):
    root_dir: Path


@dataclass(frozen=True)
class DataIngestionConfig(PathConfig):
    source_URL: str
    local_data_file: Path
    unzip_dir: Path


@dataclass(frozen=True)
class PrepareBaseModelConfig(PathConfig):
    base_model_path: Path
    updated_base_model_path: Path
    params_image_size: list
    params_learning_rate: float
    params_include_top: bool
    params_weights: str
    params_classes: int


@dataclass(frozen=True)
class PrepareCallbacksConfig(PathConfig):
    tensorboard_root_log_dir: Path
    checkpoint_model_filepath: Path



@dataclass(frozen=True)
class ProcessedDataConfig(PathConfig):
    data_dir:Path
    train_dir: Path
    processed_train_data_pickle_file: Path
    valid_dir: Path
    processed_valid_data_pickle_file: Path
    test_dir: Path
    processed_test_data_pickle_file: Path
    params_image_fixed_size: tuple
    

@dataclass(frozen=True)
class TrainingConfig(PathConfig):
    trained_model_path: Path
    updated_base_model_path: Path
    training_data: Path
    params_epochs: int
    params_batch_size: int
    params_is_augmentation: bool
    params_image_size: list


@dataclass(frozen=True)
class EvaluationConfig(PathConfig):
    path_of_model: Path
    training_data: Path
    all_params: dict
    params_image_size: list
    params_batch_size: int
