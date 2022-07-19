import logging
import logging.handlers
from os import path, makedirs

LOG_FILE = 'kibana_extract.log'
LEVEL = 'DEBUG'
LOG_DIR = 'logs'

if not path.exists(LOG_DIR):
    makedirs(LOG_DIR)


def logger(name=None):
    formatter = logging.Formatter('%(asctime)s  [%(name)s]  [%(levelname)s]  %(message)s', datefmt='%Y-%m-%d %H:%M:%S%z')
    logger = logging.getLogger(name)
    logger.setLevel(LEVEL)

    file_handler = logging.FileHandler(f'{LOG_DIR}/{LOG_FILE}')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
