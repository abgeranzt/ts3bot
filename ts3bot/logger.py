import logging.config
import os
import yaml

class Logger:
    """Configure logging from config file."""
    def __init__(self, name):
        if not os.path.exists("logs"):
            os.mkdir("logs")
            
        with open(os.path.join("config", "logger.yaml"),
                  "r") as cfg:
            logging.config.dictConfig(yaml.safe_load(cfg))
            
        self.logger = logging.getLogger(name)
