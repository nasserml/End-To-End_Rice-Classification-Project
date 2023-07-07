import time
from abc import ABC, abstractmethod
from typing import List
import os
import tensorflow as tf

from RiceClassifier.entity.config_entity import PrepareCallbacksConfig

# Callback interface and implementation

class CallbackInterface(ABC):
    @abstractmethod
    def get_callbacks(self):
        pass

class TensorBoardCallback(CallbackInterface):
    def __init__(self, log_dir: str):
        self.log_dir = log_dir

    def get_callbacks(self):
        timestamp = time.strftime("%Y-%m-%d-%H-%M-%S")
        tb_running_log_dir = os.path.join(self.log_dir, f"tb_logs_at_{timestamp}")
        return [tf.keras.callbacks.TensorBoard(log_dir=tb_running_log_dir)]

class ModelCheckpointCallback(CallbackInterface):
    def __init__(self, filepath: str):
        self.filepath = filepath

    def get_callbacks(self):
        return [tf.keras.callbacks.ModelCheckpoint(filepath=self.filepath, save_best_only=True)]

class PrepareCallback:
    def __init__(self, config: PrepareCallbacksConfig):
        self.config = config

    def get_tb_ckpt_callbacks(self):
        tb_callbacks = TensorBoardCallback(self.config.tensorboard_root_log_dir)
        ckpt_callbacks = ModelCheckpointCallback(self.config.checkpoint_model_filepath)
        return tb_callbacks.get_callbacks() + ckpt_callbacks.get_callbacks()
