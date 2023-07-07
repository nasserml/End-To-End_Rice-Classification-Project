
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Tuple
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
import pickle
from RiceClassifier.config.configuration import ConfigurationManager

from RiceClassifier.entity.config_entity import ProcessedDataConfig
from RiceClassifier.utils.common import create_directories

class ImageProcessor(ABC):
    @abstractmethod
    def read_images(self):
        pass

    @abstractmethod
    def resize_images(self, image_paths, label_mapping):
        pass

    @abstractmethod
    def scale_data(self, X, y):
        pass

class PickleManager(ABC):
    @abstractmethod
    def save_pickle(self, data: Any, pickle_path: str):
        pass

    @abstractmethod
    def load_pickle(self, pickle_path: str) -> Any:
        pass

class ProcessedData:
    def __init__(self, config: ProcessedDataConfig, image_processor: ImageProcessor, pickle_manager: PickleManager):
        self.config = config
        self.image_processor = image_processor
        self.pickle_manager = pickle_manager
    
    def get_process_data(self):
        df_images, df_labels = self.image_processor.read_images()
        X, y = self.image_processor.resize_images(df_images, df_labels)
        X, y = self.image_processor.scale_data(X, y)
        train_data, valid_data, test_data = self.split_data(X, y)

        self.create_directories()
        self.pickle_manager.save_pickle(train_data, self.config.processed_train_data_pickle_file)
        self.pickle_manager.save_pickle(valid_data, self.config.processed_valid_data_pickle_file)
        self.pickle_manager.save_pickle(test_data, self.config.processed_test_data_pickle_file)
    
    def split_data(self, X, y):
        X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.4, random_state=42)
        X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)
        return (X_train, y_train), (X_val, y_val), (X_test, y_test)
    
    def create_directories(self):
        create_directories([Path(self.config.train_dir)]) 
        create_directories([Path(self.config.valid_dir)]) 
        create_directories([Path(self.config.test_dir)]) 

class ImageDataProcessor(ImageProcessor):
    def __init__(self, config: ProcessedDataConfig):
        self.config = config
    
    def read_images(self):
        data_dir = Path(self.config.data_dir)
        image_paths = {
            'arborio': list(data_dir.glob('Arborio/*'))[:100],
            'basmati': list(data_dir.glob('Basmati/*'))[:100],
            'ipsala': list(data_dir.glob('Ipsala/*'))[:100],
            'jasmine': list(data_dir.glob('Jasmine/*'))[:100],
            'karacadag': list(data_dir.glob('Karacadag/*'))[:100]
        }
        label_mapping = {
            'arborio': 0,
            'basmati': 1,
            'ipsala': 2,
            'jasmine': 3,
            'karacadag': 4
        }
        return image_paths, label_mapping
    
    def resize_images(self, image_paths, label_mapping):
        X, y = [], []
        for label, paths in image_paths.items():
            for path in paths:
                img = cv2.imread(str(path))
                resized_img = cv2.resize(img, (224, 224))
                X.append(resized_img)
                y.append(label_mapping[label])
        return np.array(X), np.array(y)
    
    def scale_data(self, X, y):
        X_scaled = X / 255
        return X_scaled, y

class PickleFileManager(PickleManager):
    def save_pickle(self, data: Any, pickle_path: str):
        with open(pickle_path, "wb") as file:
            pickle.dump(data, file)
    
    def load_pickle(self, pickle_path: str) -> Any:
        with open(pickle_path, "rb") as file:
            data = pickle.load(file)
        return data
