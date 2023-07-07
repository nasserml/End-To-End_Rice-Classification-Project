import os
import urllib.request as request
from zipfile import ZipFile
import tensorflow as tf
from RiceClassifier.entity.config_entity import PrepareBaseModelConfig 

from pathlib import Path

import tensorflow as tf
import tensorflow_hub as hub
from tensorflow import keras

class BaseModelLoader:
    
    def __init__(self, config: PrepareBaseModelConfig):
        self.config = config
        
    def load_base_model(self, config: PrepareBaseModelConfig):
        
        mobile_net = 'https://tfhub.dev/google/tf2-preview/mobilenet_v2/feature_vector/4' # MobileNetv2 link
        mobile_net = hub.KerasLayer(
            mobile_net, input_shape=(224,224,3), trainable=False) # Removing the last layer

        num_label = 5 # number of labels

        self.model = keras.Sequential([
            mobile_net,
            #keras.layers.Dense(num_label)
        ])
        
        return self.model
    """ return tf.keras.applications.mobilenet_v2.MobileNetV2(
            input_shape=config.params_image_size,
            weights=config.params_weights,
            include_top=config.params_include_top
        ) """
        
    def save_base_model(self, model: tf.keras.Model):
        model.save(self.config.base_model_path)


class FullModelPreparer:
    def __init__(self, config: PrepareBaseModelConfig):
        self.config = config

    def prepare_full_model(self, base_model, classes, freeze_all, freeze_till, learning_rate):
        if freeze_all:
            for layer in base_model.layers:
                layer.trainable = False
        elif (freeze_till is not None) and (freeze_till > 0):
            for layer in base_model.layers[:-freeze_till]:
                layer.trainable = False

        flatten_in = tf.keras.layers.Flatten()(base_model.output)
        prediction = tf.keras.layers.Dense(
            units=classes,
            activation="softmax"
        )(base_model.output)

        full_model = tf.keras.models.Model(
            inputs=base_model.input,
            outputs=prediction
        )

        full_model.compile(
            optimizer="adam",
            loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            metrics=["acc"]
        )

        full_model.summary()
        return full_model


class BaseModelUpdater:
    def __init__(self, config: PrepareBaseModelConfig):
        self.config = config

    def save_updated_base_model(self, model: tf.keras.Model):
        model.save(self.config.updated_base_model_path)
    
    