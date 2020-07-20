# std
import re
from socket import gaierror, timeout
from telnetlib import Telnet
import time

# local
from ts3bot.logger import get_logger
from ts3bot.misc import AuthError

class Client_Query:
    """
    Basic API for TeamSpeak client query.
    - host: int
    - port: int
    - apikey: str
    """
    def __init__(self,
                 host,
                 port,
                 apikey):
        self.logger = get_logger("client_query")
        self._host = host
        self._port = port
        self._apikey = apikey
        self._tn = Telnet()

    def connect(self):
        """Connect to client query through telnet connection."""
        try:
            self.logger.info(f"Connecting to {self._host}:{self._port}.")
            self._tn.open(self._host, self._port, timeout=5)
            self._tn.write(f"auth apikey={self._apikey}\n".encode())
            # Check for login status.
            for msg in self.listen():
                if re.search("msg=ok", msg):
                    break
                elif re.search("error", msg):
                    err_msg = f'Query login at "{self._host}" failed.'
                    self.logger.error(err_msg)
                    self.logger.debug(msg)
                    raise AuthError(err_msg, msg)
            self.logger.info(f'Connected to "{self._host}".')
        except ConnectionRefusedError as err:
            err_msg = f'Connection to "{self._host}" refused.'
            self.logger.error(err_msg)
            self.logger.debug(err)
            raise ConnectionRefusedError(err_msg, err)
        except gaierror as err:
            err_msg = f'Connection to "{self._host}" failed.'
            self.logger.error(err_msg)
            self.logger.debug(err)
            raise ConnectionError(err_msg, err)
        except timeout as err:
            err_msg = f'Connection to "{self._host}" timed out.'
            self.logger.error(err_msg)
            self.logger.debug(err)
            raise ConnectionError(err_msg, err)

    def get_msg(self):
        """Read line from query and return as str."""
        try:
            msg = self._tn.read_until("\n".encode()).decode()
            return(msg)
        except EOFError as err:
            err_msg = f'Connection to query at "{self._host}" closed.'
            self.logger.warning(err_msg)
            raise ConnectionAbortedError(err_msg, err)

    def listen(self):
        """Listen on query connection and yield messages."""
        while True:
            yield(self.get_msg())

    def send_msg(self, msg, freq=5, max_retry=3):
        """
        Encode and send message string to query.
        - msg: str
        - freq: int
        - max_retry: int
        """
        retry = 0
        while True:
            try:
                self.logger.debug(f'(1/2) Sending message to "{self._host}".')
                self.logger.debug(f'(2/2) Message body: "{msg}"')
                self._tn.write(f"{msg}\n".encode())
                break
            except OSError as err:
                self.logger.error(f'Sending message to query at "{self._host}" failed.')
                self.logger.debug(err)
                if retry > max_retry:
                    self.logger.critical(
                        f'Sending message to query at "{self._host}" ' \
                        f"failed after {retry + 1} attempts.")
                    self.logger.error('Aborting message.')
                    raise ConnectionError("Failed to send message.")
                self.logger.debug(f"Attempting to resend message in {freq} seconds.")
                time.sleep(freq)
                freq *= 2
                retry += 1
                continue

    def send_cmd(self, msg, freq=5, max_retry=3, lines=1):
        """
        Wrapper for get_msg() and send_msg().
        - msg: str
        - freq: int
        - max_retry: int

        Return message and status.
        """
        self.send_msg(msg, freq, max_retry)
        if lines == 1:
            return self.get_msg()
        elif lines == 2:
            return self.get_msg(), self.get_msg()

    def keep_alive(self, freq=180):
        """
        Query current schandlerid to keep connection alive.
        Run as child process.
        Argument: Frequency in seconds.
        - freq: int
        """
        while True:
            self.logger.debug("Sending keep alive request.")
            try:
                self.send_cmd("currentschandlerid")
            except ConnectionError as err:
                self.logger.error(f'Keep alive request for query at "{self._host}" failed.')
                self.logger.debug(err)
                # Kill process.
                return False
            time.sleep(freq)

