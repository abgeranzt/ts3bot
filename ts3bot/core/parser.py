# std
import re

class Parser:
    def __init__(self):
        """Parser for query output."""
        pass
    
    # --- Public Interface Methods ---

    def parse_event(self, line):
        """Parse query event notification.

        Split line into name and rows with attributes.

        Args:
            line (str): raw query output

        Returns:
            event (dict): name, schandlerid, list of rows with attributes
        """
        event = {}
        line = re.sub(r"\n|\r", "", line)
        event["NAME"], schandlerid, line = (re.split(" ", line, maxsplit=2))
        event["SCHANDLERID"] = int(re.search(r"\d+", schandlerid).group())
        event["ROWS"] = []
        for row in re.split(r"\|", line):
            attributes = {}
            for attribute in re.split(r" ", row):
                m = re.search(r"(^\S+)=(\S+$)", attribute)
                key = m.group(1)
                val = m.group(2)
                # Convert number strings to int:
                if re.search(r"^\d+$", val):
                    val = int(val)
                # Multiple numbers:
                elif re.search(r"^\d+,", val):
                    val = [int(i) for i in re.split(r",", val)]
                attributes[key] = val
            event["ROWS"].append(attributes)
        return event

    def parse_error(self, line):
        """Parse query error message.

        Split line into ID and description string.

        Args:
            line (str): raw query output

        Returns:
            error (dict): "ID", "DESC"
        """
        line = re.sub(r"\n|\r|error ", "", line)
        m = re.search(r"id=(\d+) msg=(.+$)", line)
        return {"ID": int(m.group(1)),
                "DESC": m.group(2)}

    def parse_response(self, line):
        """Parse query response message.

        Split line into rows with attributes.

        Args:
            line (str): raw query output

        Returns:
            response (dict[]): list with dicts
        """
        line = re.sub(r"\n|\r", "", line)
        response = []
        for row in re.split(r"\|", line):
            attributes = {}
            for attribute in re.split(r" ", row):
                m = re.search(r"(^\S+)=(\S+$)", attribute)
                key = m.group(1)
                val = m.group(2)
                # Convert number strings to int:
                if re.search(r"^\d+$", val):
                    val = int(val)
                # Multiple numbers:
                elif re.search(r"^\d+,", val):
                    val = [int(i) for i in re.split(r",", val)]
                attributes[key] = val
            response.append(attributes)
        return response