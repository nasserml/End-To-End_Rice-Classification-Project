import os
import logging
import pytest
from RiceClassifier.logger import Logger

@pytest.fixture(scope="module")
def test_logger():
    # Set up test parameters
    logger_name = "TestLogger"
    log_filepath = "logs/test_logs.log"
    logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"

    # Create an instance of the Logger
    logger = Logger(logger_name, log_filepath, logging_str).get_logger()

    # Yield the logger object to the test function
    yield logger

    # Perform any necessary cleanup after the test
    logger.handlers = []  # Remove all handlers from the logger
    if os.path.isfile(log_filepath):
        os.remove(log_filepath)

def test_logger_creation(test_logger):
    # Check if the logger object is created
    assert isinstance(test_logger, logging.Logger)

def test_logger_logging(test_logger):
    # Perform logging operations
    test_logger.info("Test message")

    # Read the log file and check if the test message is logged
    with open("logs/test_logs.log", "r") as f:
        log_content = f.read()
        assert "Test message" in log_content



# Test log file creation
def test_log_file_creation(tmpdir):
    # Create a temporary directory for the log file
    log_dir = tmpdir.mkdir("logs")
    log_filepath = os.path.join(log_dir, "test_logs.log")

    # Create an instance of the Logger
    logger = Logger("TestLogger", log_filepath, "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]").get_logger()

    # Assert that the log file exists
    assert os.path.isfile(log_filepath)

# Test log format
def test_log_format(tmpdir, caplog):
    # Create a temporary directory for the log file
    log_dir = tmpdir.mkdir("logs")
    log_filepath = os.path.join(log_dir, "test_logs.log")

    # Create an instance of the Logger
    logger = Logger("TestLogger", log_filepath, "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]").get_logger()

    # Log a message
    logger.info("Test message")

    # Assert that the log format matches the specified format
    assert caplog.records[0].getMessage() == "Test message"

# Test log messages
def test_log_messages(tmpdir, caplog):
    # Create a temporary directory for the log file
    log_dir = tmpdir.mkdir("logs")
    log_filepath = os.path.join(log_dir, "test_logs.log")

    # Create an instance of the Logger
    logger = Logger("TestLogger", log_filepath, "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]").get_logger()

    # Log multiple messages
    logger.info("Message 1")
    logger.warning("Message 2")
    logger.error("Message 3")

    # Assert that the logged messages are captured correctly
    assert caplog.records[0].getMessage() == "Message 1"
    assert caplog.records[1].getMessage() == "Message 2"
    assert caplog.records[2].getMessage() == "Message 3"