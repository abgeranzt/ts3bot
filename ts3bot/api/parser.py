# std
import re

# local
from ts3bot.logger import get_logger

class Parser:
    def __int__(self):
        """Basic query parser."""
        self.logger = get_logger("parser")

    def parse_response(self, msg):
        """Parse response from interactive query and return dict."""
        msg_dict = {}
        msg_split = re.split(" ", msg)
        for msg_part in msg_split:
            key, val = re.split("=", msg_part, maxsplit=1)
            msg_dict[key.upper()] = val
        return msg_dict

    def parse_notify(self, msg):
        """Parse message from notifier query and return dict."""
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