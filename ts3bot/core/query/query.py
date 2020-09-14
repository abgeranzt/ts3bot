# std
import re
from socket import gaierror, timeout
from telnetlib import Telnet

# local
from .errors import AuthError, QueryTimeout

class Query:
    """
    Interface for TeamSpeak client query.
    
    - host: int
    - port: int
    - apikey: str
    - logger: logger object
    """
    def __init__(self, host, port, apikey, logger=None):
        self.HOST = host
        self.PORT = port
        self._APIKEY = apikey
        self._logger = logger
        self._tn = Telnet()

    def connect(self):
        """
        Connect to query through telnet.
        Return exit status:
        0: OK
        1: Connection error
        2: Authentification error
        """
        self._logger.info(
            f"Connecting to query at {self.HOST}:{self.PORT}"
        )
        try:
            # Open connection and authenticate.
            self._tn.open(self.HOST, self.PORT, timeout=5)
            self.write(f"auth apikey={self._APIKEY}")
            # Check for auth success.
            for line in self.read_all():
                if re.search("msg=ok", line):
                    self._logger.info("Query connection OK.")
                    return 0
                elif re.search("error", line):
                    self._logger.error("Query authentification failed!")
                    self._logger.debug(line)
                    return 2
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
        """
        Read line from query and return it as str.
        """
        try:
            line = self._tn.read_until("\n".encode(), timeout=timeout)
            line = line.decode()
            if not re.search(r"\w", line):
                raise QueryTimeout
            return line
        except EOFError:
            raise ConnectionAbortedError

    def read_all(self, timeout=None):
        """
        Yield lines from query as str.
        """
        while True:
            yield(self.read_line(timeout))

    def write(self, line):
        """
        Write line to query.
        """
        self._tn.write(f"{line}\n".encode())
