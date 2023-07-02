
import os
import sys
import logging

class Logger:
    def __init__(self, logger_name, log_filepath, logging_str):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)
        
        self.log_filepath = log_filepath
        self.logging_str = logging_str
        
        self._configure_handlers()

    def _configure_handlers(self):
        os.makedirs(os.path.dirname(self.log_filepath), exist_ok=True)

        file_handler = logging.FileHandler(self.log_filepath)
        file_handler.setLevel(logging.INFO)

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(self.logging_str)
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)

    def get_logger(self):
        return self.logger


logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"
log_dir = "logs"
log_filepath = os.path.join(log_dir, "running_logs.log")
    
logger = Logger("RiceClassifierLogger", log_filepath, logging_str).get_logger()
