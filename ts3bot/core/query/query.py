# std
import logging.config
import re
from socket import gaierror, timeout
from telnetlib import Telnet

class Query:
    """Interface for TeamSpeak client query.
    
    Attributes:
        host: query host
        port (int): query port
        apikey (str): query api key
        logger (dict): logger configuration
    """
    def __init__(self, host, port, apikey, logging_config):
        self.HOST = host
        self.PORT = port
        self._APIKEY = apikey
        self._tn = Telnet()

        # Configure logging.
        logging.config.dictConfig(logging_config)
        self._logger = logging.getLogger("listener")

    # --- Basic Methods ---

    def connect(self):
        """Connect to query through telnet.
        
        Returns:
            status (int): status code

        Status codes:
            0: OK
            1: connection error
            3: auth error
        """
        self._logger.info(f"Connecting to query at {self.HOST}" \
                          f":{self.PORT}")
        try:
            # Open connection and authenticate.
            self._tn.open(self.HOST, self.PORT, timeout=5)
            self.write(f"auth apikey={self._APIKEY}")
            # Check for auth success.
            for line in self.read_all():
                if re.search("msg=ok", line[1]):
                    self._logger.info("Query connection OK.")
                    return 0
                elif re.search("error", line[1]):
                    self._logger.error("Query authentification failed!")
                    self._logger.debug(line[1])
                    return 3
        except ConnectionRefusedError:
            self._logger.error("Connection refused!")
        except gaierror:
            self._logger.error("Connection failed!")
        except OSError:
            self._logger.error("No route to host!")
        except timeout:
            self._logger.error("Connection timed out!")
        return 1

    def read_line(self, timeout=None):
        """Read line from query.

        Args:
            timeout (int): timeout in seconds

        Returns:
            status (int): status code
            line (str): line of query output

        Status codes:
            0: OK
            1: connection error
            2: read timeout
        """
        try:
            line = self._tn.read_until("\n".encode(), timeout=timeout)
            line = line.decode()
            if not re.search(r"\w", line):
               return 2, "" 
            return 0, line
        except EOFError:
            return 1, ""

    def read_all(self, timeout=None):
        """Read lines from query.

        Yield values returned by self.read_line()

        Args:
            timeout (int): timeout in seconds

        Yields:
            status (int): status code
            line (str): line of query output
        """
        while True:
            yield(self.read_line(timeout))

    def write(self, line):
        """Write line to query.

        Args:
            line (str): line to write
        """
        self._tn.write(f"{line}\n".encode())

    # --- Wrapper Methods ---

    def send(self, line, response_len):
        """Write line to query and return answer.

        Wrapper for self.write() and self.read_line().

        Args:
            line (str): line to write
            response_len (1): expected amount of lines returned by query

        Returns:
            status (int): status code
            response_lines (str[]): list containing query output lines

        Status codes:
            0: OK
            1: connection error
            2: query returned error
        """
        response_lines = []
        self.write(line)
        for _ in range(response_len):
            status, response = self.read_line(timeout=2)
            if status == 0:
                response_lines.append(response)
            elif status == 1:
                return 1, []
            else:
                return 2, response_lines
        return 0, response_lines

    def keep_alive(self):
        """Keep query connection alive.

        Send "whoami" through self.send().

        Returns:
            status (int): status code
            response (str): query output line

        Status codes:
            0: OK
            1: connection error
            2: query returned error
        """
        status, response = self.send("whoami", 1)
        return status, response[0]

    def notify_register(self, event, schandlerid=1):
        """Register for query event notifications.

        Send request through self.send().
        Check whether request was successfull.

        Args:
            event (str): event
            schandlerid (int): schandlerid (defaults to 1)

        Returns:
            status (int): status code
            response (str): query output line

        Status codes:
            0: OK
            1: connection error
            2: query returned error
        """
        status, response = self.send(f"clientnotifyregister " \
                                     f"schandlerid={schandlerid} " \
                                     f"event={event}", 1)
        return status, response[0]

    def notify_unregister(self):
        """Unregister from all event notifications.

        Send request through self.send().
        Check whether request was successfull.

        Returns:
            status (int): status code
            response (str): query output line

        Status codes:
            0: OK
            1: connection error
            2: query returned error
        """
        status, response = self.send("clientnotifyunregister", 1)
        return status, response[0]
