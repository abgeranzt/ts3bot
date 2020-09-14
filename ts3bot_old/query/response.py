# std
import os
import yaml

class Error:
    """Error Response object."""
    def __init__(self, error_id, error_msg):
        self.reponse_type = "error"
        self.error_id = error_id
        self.error_msg = error_msg
        self.error_def = self._load_error_def()

    def _load_error_def(self):
        """Load error definition and return it as string."""
        cfg_path = os.path.join("config", "default", "errors.yaml")
        with open(cfg_path, "r") as cfg_file:
            cfg = yaml.safe_load(cfg_file)
        return cfg[self.error_id]["def"]

class Event:
    """Event Response object."""
    def __init__(self, event_type, body, schandlerid):
        self.reponse_type = "event"
        self.event_type = event_type
        self.body = body
        self.schandlerid = schandlerid

class Response:
    """Reponse object."""
    def __init__(self, body, error):
        self.reponse_type = "response"
        self.body = body
        self.error = error
