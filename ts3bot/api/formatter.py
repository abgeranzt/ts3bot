# std
import re

# local
from ts3bot.logger import get_logger

class Formatter:
    def __init__(self):
        """Query message formatter."""
        self.logger = get_logger("formatter")

    def rep_whitespace(self, msg):
        """
        Replace whitespace with control characters.
        msg: str

        Return str.
        """
        return re.sub(" ", "\\s", re.sub("\n", "\\n"))
