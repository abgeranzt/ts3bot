#std
import logging.config
import os
import yaml

class Logger:
    """Return configured logger object."""
    def get_logger(self, name):
        if not os.path.exists("logs"):
            os.mkdir("logs")
        with open("config/logger.yaml", "r") as cfg:
            logging.config.dictConfig(yaml.safe_load(cfg))
        logger = logging.getLogger(name)
        return logger
