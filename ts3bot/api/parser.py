# std
import re

# local
from ts3bot.logger import get_logger

class Parser:
    def __init__(self):
        """Basic query parser."""
        self.logger = get_logger("parser")

    def parse_response(self, msg):
        """Parse response from interactive query and return list."""
        self.logger.debug("Parsing response: (1/2)")
        self.logger.debug(msg)
        msg_list = []
        # Remove leading "/r".
        msg = re.split("\\r", msg)[1]
        msg = re.split("\|", msg)
        for entry in msg:
            entry = re.split(" ", entry)
            entry_dict = {}
            for attr in entry:
                key, val = re.split("=", attr, maxsplit=1)
                entry_dict[key.upper()] = val
            msg_list.append(entry_dict)
        return msg_list

    def parse_notify(self, msg):
        """Parse message from notifier query and return dict."""
        self.logger.debug("Parsing notification: (1/2)")
        self.logger.debug(msg)
        msg_dict = {}
        msg_dict["KIND"], msg = re.split(" ", msg, maxsplit=1)
        msg_dict["CONTENT"] = []
        msg = re.split("\|", msg)
        for entry in msg:
            entry = re.split(" ", entry)
            entry_dict = {}
            for attr in entry:
                key, val = re.split("=", attr, maxsplit=1)
                entry_dict[key.upper()] = val
            msg_dict["CONTENT"].append(entry_dict)
        return msg_dict
