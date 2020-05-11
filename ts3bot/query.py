# std
import re
from socket import gaierror, timeout
from telnetlib import Telnet
import time

# local
from ts3bot.logger import Logger

class AuthError(ConnectionError):
    """Raise when query authentification fails."""  

class Query:
    """
    TeamSpeak Query API.
    - host: str
    - port: str
    - passwd: str
    """
    def __init__(self, host, port, passwd):
        self._host = host
        self._passwd = passwd
        self._port = port
        self._tn = Telnet()
        self.logger = Logger().get_logger("query")
            
    def cl_connect(self):
        """Connect to client query through telnet connection."""
        try:
            self.logger.info(f'Connecting to client query at "{self._host}".')
            self._tn.open(self._host, self._port, timeout=5)
            self._tn.write(f"auth apikey={self._passwd}\n".encode())
            # Check for login status.
            for msg in self.listen():
                if re.search("msg=ok", msg):
                    break
                elif re.search("error", msg):
                    err_msg = f'Query login at "{self._host}" failed.'
                    self.logger.error(err_msg)
                    self.logger.debug(msg)
                    raise AuthError(err_msg, msg)
            self.logger.info(f'Successfully connected to query at "{self._host}"')    
        except ConnectionRefusedError as err:
            err_msg = f'Connection to query at "{self._host}" refused.'
            self.logger.error(err_msg)
            self.logger.debug(err)
            raise ConnectionRefusedError(err_msg, err)
        except gaierror as err:
            err_msg = f'Connection to query at "{self._host}" failed.'
            self.logger.error(err_msg)
            self.logger.debug(err)
            raise ConnectionError(err_msg, err)
        except timeout as err:
            err_msg = f'Connection to query at "{self._host}" timed out.'
            self.logger.error(err_msg)
            self.logger.debug(err)
            raise ConnectionError(err_msg, err)
    
    def sv_connect_tn(self):
        """
        Connect to server query though telnet connection.
        Return session object.
        """
        pass
    
    def sv_connect_ssh(self):
        """
        --- Placeholder ---
        Connect to server query through SSH connection.
        --- Placeholder ----
        """
        pass
    
    def listen(self):
        """Listen on query connection and yield messages."""
        while True:
            try:
                msg = self._tn.read_until("\n".encode()).decode()
                yield(msg)
            except EOFError as err:
                err_msg = f'Connection to query at "{self._host}" closed.'
                self.logger.warning(err_msg)
                raise ConnectionAbortedError(err_msg, err)
                
    def keep_alive(self, freq=180):
        """
        Keep query connection alive by sending whoami requests.
        Run as child process.
        Argument: Frequency in seconds.
        - freq: int 
        """
        while True:
            self.logger.debug("Sending keep alive request.")
            try:
                self._tn.write("whoami\n".encode())
            except OSError as err:
                self.logger.error(f'Keep alive request for query at "{self._host}" failed.')
                self.logger.debug(err)
                # Kill process.
                return False
            time.sleep(freq)