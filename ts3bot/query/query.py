# std
import re
# TODO Import of exceptions necessary?
#from socket import gaierror, timeout
from telnetlib import Telnet

# local
from ts3bot.errors import AuthError

class Query:
    """
    Interface for TeamSpeak client query.
    - cfg: dict
    """
    def __init__(self, cfg, logger):
        self._HOST = cfg["host"]
        self._PORT = cfg["port"]
        self._APIKEY = cfg["apikey"]
        self._logger = logger
        self._telnet = Telnet()

    def connect(self):
        """
        Connect to query using telnet.
        Return bool depending on success.
        """
        log_d = self._logger.debug
        log_e = self._logger.error
        log_i = self._logger.info

        log_i(f"Connecting to query at {self._HOST}:{self._PORT}")
        try:
            # Connect and login.
            self._telnet.open(self._HOST, self._PORT, timeout=5)
            self.write(f"auth apikey={self._APIKEY}")
            # Check for login success.
            for line in self._read_all():
                if re.search("msg=ok", line):
                    log_i("Connection established.")
                    return True
                elif re.search("error", line):
                    log_e("Query login failed.")
                    log_d(line)
                    raise AuthError(line)
        except ConnectionRefusedError:
            log_e("Connection refused.")
        except gaierror:
            log_e("Connection failed.")
        except OSError:
            log_e("No route to host.")
        except timeout:
            log_e("Connection timed out.")
        return false

    def read_line(self, timeout=None):
        """
        Read line from query and return it as str.
        """
        try:
            line = self._telnet.read_until("\n".encode(), timeout=timeout)
            return line.decode()
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
        self._telnet.write(f"{line}\n".encode())
