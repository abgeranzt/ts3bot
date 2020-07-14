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

    def parse_line(self, line):
        """
        Parse single message (body) line from query.
        - msg: str
        - ctrl_chars: bool

        Return dict.
        """
        self.logger.debug("Parsing message line.")
        line = self.remove_ctrl_chars(line)
        line_dict = {}
        line = re.split(" ", line)
        for attr in line:
            try:
                key, val = re.split("=", attr, maxsplit=1)
            except ValueError:
                key, val = attr,""
            # Convert string numbers to int.
            if re.search("^\d+$", val):
                val = int(val)
            elif re.search("^\d+,", val):
                val_list = []
                for number in re.split(",", val):
                    val_list.append(int(number))
                val = val_list
            line_dict[key.lower()] = val
        return line_dict

    def parse_lines(self, msg):
        """
        Parse items seperated by "|".
         - msg: str

        Return dict(s in list).
        """
        self.logger.debug("Parsing lines.")
        msg_items = []
        msg = re.split("\|", msg)
        for line in msg:
            msg_items.append(self.parse_line(line))
        if len(msg_items) == 1:
            msg_items = msg_items[0]
        return msg_items

    def parse_message(self, msg, head=None):
        """
        Parse message from notifier query.
        - msg: str
        - head: str

        Return dict.
        """
        self.logger.debug("Parsing notification.")
        msg_dict = {}
        msg = self.remove_ctrl_chars(msg)
        msg_dict["kind"], msg = re.split(" ", msg, maxsplit=1)
        if head != None:
            # Transform regex pattern into specific head.
            head = re.search(head, msg).group(0)
            # TODO: Parse head.
            msg_head, msg = re.split(head, msg)
            msg_dict["head"] = f'{msg_head}{re.sub(" ", "", head)}'
        # Parse body.
        msg_dict["body"] = self.parse_lines(msg)
        return msg_dict
