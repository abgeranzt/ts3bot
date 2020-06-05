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
        """Parse message from listener query and return dict."""
        msg_dict = {}
        msg_split = re.split(" ", msg)
        msg_dict["KIND"] = msg_split[0]
        for msg_part in msg_split[1:]:
            key, val = re.split("=", msg_part, maxsplit=1)
            msg_dict[key.upper()] = val
        return msg_dict
