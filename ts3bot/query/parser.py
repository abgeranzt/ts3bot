# std
import re

# local
from ts3bot.query.response import Error, Event, Response

class Parser:
    def __init__(self):
        """Parser for query format."""
        pass

    # --- Public Methods ---

    @classmethod
    def parse_event(cls, line):
        """
        Parse event from query.
        Return Event response object.
        """
        line = cls._rm_crtl_chars(line)
        event_type, schandlerid, line = re.split(" ", line, maxsplit=2)
        body = cls._parse_body(line)
        schandlerid = int(re.split("=", schandlerid)[1])
        return Event(event_type, body, schandlerid)

    @classmethod
    def parse_response(cls, line, error):
        """
        Parse response from query.
        Return response object.
        """
        line = cls._rm_ctrl_chars(line)
        body = cls._parse_body(line)
        error = cls.parse_error(error)
        return Response(body, error)

    @classmethod
    def parse_error(cls, line):
        """
        Parse error id response.
        Return response object.
        """
        line = cls._rm_ctrl_chars(line)
        line = re.sub("error ", "", line)
        body = cls._parse_content(line)
        error_id = int(body["id"])
        error_msg = body["msg"]
        return Error(error_id, error_msg)

    # --- Private Methods ---

    @staticmethod
    def _split_rows(line):
        """Split string at "|" and return splits in list."""
        return re.split("\|", line)

    @staticmethod
    def _parse_content(line):
        """Parse keys and values and return them in dict."""
        content = {}
        for row in re.split(" ", line):
            try:
                key, val = re.split("=", row, maxsplit=1)
                # Convert number strings to int.
                if re.search("^\d+$", val):
                    val = int(val)
                elif re.search("^\d+,", val):
                    vals = []
                    for nr in re.split(",", val):
                        vals.append(int(nr))
                    val = vals
            # If key has no value:
            except ValueError:
                key = row
                val = ""
            content[key.lower()] = val
        return content

    @classmethod
    def _parse_body(cls, line):
        """Parse line body and return its attributes in list."""
        body = []
        for row in cls._splitrows(line):
            body.append(cls._parse_content(row))
        return body

    @staticmethod
    def _rm_ctrl_chars(line):
        """Remove and "\n" and "\r" from string and return it."""
        return re.sub("\\n|\\r", "", line)

