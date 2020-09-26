import inspect
import logging
import os
from datetime import date


def custom_logger(log_level=logging.INFO):

    # Gets the name of the class / method from where this method is called
    logger_name = inspect.stack()[1][3]
    logger = logging.getLogger(logger_name)
    # By default, log all messages
    logger.setLevel(logging.INFO)
    log_file_path = os.path.join(os.path.abspath(__file__ + '/../../'), 'Logs', f'Logs_{date.today()}.log')
    file_handler = logging.FileHandler(log_file_path, mode='a')
    file_handler.setLevel(log_level)

    formatter = logging.Formatter('%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)',
                                  datefmt='%m/%d/%Y %I:%M:%S %p')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger
