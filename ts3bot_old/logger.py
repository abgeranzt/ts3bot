#std
import logging.config
import os
import yaml

def get_logger(name):
    """
    Load logging config from file and return logger object.
    Create new directory for logs if necessary.
    """
    if not os.path.exists("logs"):
        os.mkdir("logs")
    cfg_path = os.path.join("config", "local", "logger.yaml")
    with open(cfg_path, "r") as cfg_file:
        cfg = yaml.safe_load(cfg_file)
        logging.config.dictConfig(cfg)
    return logging.getLogger(name)
