#std
import logging.config
import os
import yaml

def get_logger(name):
    """Return configured logger object."""
    if not os.path.exists("logs"):
        os.mkdir("logs")
    with open("config/local/logger.yaml", "r") as cfg:
        logging.config.dictConfig(yaml.safe_load(cfg))
    logger = logging.getLogger(name)
    return logger
