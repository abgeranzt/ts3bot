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
        """
        Connect to client query through telnet connection.

        Return True if successfull, otherwise False.
        """
        try:
            self.logger.info(f"Connecting to {self._host}:{self._port}.")
            self._tn.open(self._host, self._port, timeout=5)
            self._tn.write(f"auth apikey={self._apikey}\n".encode())
            # Check for login status.
            for msg in self.listen():
                if re.search("msg=ok", msg):
                    break
                elif re.search("error", msg):
                    err_log = f'Query login at "{self._host}" failed.'
                    self.logger.error(err_log)
                    self.logger.debug(msg)
                    raise AuthError(err_log, msg)
            self.logger.info(f'Connected to "{self._host}".')
            return True
        # Connection refused.
        except ConnectionRefusedError as err:
            err_log = f'Connection to "{self._host}" refused.'
            err_msg = err
        # No route to host.
        # TODO: Other causes that use OSError are possible but not known.
        except OSError as err:
            err_log = f'Connection to "{self._host}" failed.'
            err_msg = err
        # TODO: What error is this?
        except gaierror as err:
            err_log = f'Connection to "{self._host}" failed.'
            err_msg = err
        # Connection timed out.
        except timeout as err:
            err_log = f'Connection to "{self._host}" timed out.'
            err_msg = err
        self.logger.error(err_log)
        self.logger.debug(err_msg)
        return False

    def get_msg(self):
        """Read line from query and return as str."""
        try:
            msg = self._tn.read_until("\n".encode()).decode()
            return(msg)
        except EOFError as err:
            err_log = f'Connection to query at "{self._host}" closed.'
            self.logger.warning(err_log)
            raise ConnectionAbortedError(err_log, err)

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
        # Use explicit number because number of output lines depends on command.
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

