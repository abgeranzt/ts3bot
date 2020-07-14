# std
import re

# local
from ts3bot.logger import get_logger

class Parser:
    def __init__(self):
        """Basic query parser."""
        self.logger = get_logger("parser")

    def remove_ctrl_chars(self, msg):
        """
        Remove "\r" and "\n" from string.
        - msg: str

        Return str.
        """
        self.logger.debug("Removing control characters.")
        return re.sub("\\n", "", re.sub("\\r", "", msg))

    def parse_response(self, msg):
        """
        Parse response from interactive query.
        - msg: str

        Return list.
        """
        self.logger.debug("Parsing response.")
        msg_list = []
        msg = self.remove_ctrl_chars(msg)
        # Parse message.
        msg = re.split("\|", msg)
        for entry in msg:
            entry = re.split(" ", entry)
            entry_dict = {}
            for attr in entry:
                try:
                    key, val = re.split("=", attr, maxsplit=1)
                # Attribute has no value:
                except ValueError:
                    key = attr
                    val = ""
                entry_dict[key.upper()] = val
            msg_list.append(entry_dict)
        return msg_list

    def parse_notify(self, msg, head):
        """
        Parse message from notifier query.
        - msg: str
        - head: str

        Return dict.
        """
        self.logger.debug("Parsing notification.")
        msg_dict = {}
        msg = self.remove_crtl_chars(msg)
        msg_dict["KIND"], msg = re.split(" ", msg, maxsplit=1)
        # Transform regex pattern into specific head.
        head = re.search(head, msg).group(0)
        # Parse head.
        msg_head, msg = re.split(head, msg)
        msg_dict["HEAD"] = f"{msg_head}{head}"
        # Parse body.
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
