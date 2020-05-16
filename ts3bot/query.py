# std
import re
from socket import gaierror, timeout
from telnetlib import Telnet
import time

# local
from ts3bot.logger import get_logger

class AuthError(ConnectionError):
    """Raise when query authentification fails."""  

class Query:
    """
    Basic API for TeamSpeak Queries.
    - host: str
    - port: str
    - passwd: str
    """
    def __init__(self, host, port, passwd):
        self._host = host
        self._passwd = passwd
        self._port = port
        self._tn = Telnet()
        self.logger = get_logger("query")
            
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
    
    def send(self, msg, freq=5, max_retry=3):
        """
        Encode and send message string to query.
        - msg: str
        - freq: int        
        """
        retry = 0
        while true:
            try:
                self.logger.debug(f'(1/2) Sending message to query at "{self._host}".')
                self.logger.debug(f'(2/2) Message body: "{msg}"')
                self._tn.write(f"{msg}\n".encode(), timeout)
                break
            except OSError as err:
                self.logger.error(f'Sending message to query at "{self._host}" failed.')
                self.logger.debug(err)
                if retry > max_retry:
                    self.logger.critical(f'Sending message to query at "{self._host}" failed after {retry + 1} attempts.')
                    self.logger.error('Aborting message.')
                    raise ConnectionError("Failed to send message.")
                self.logger.debug(f"Attempting to resend message in {freq} seconds.")
                time.sleep(freq)
                freq *= 2
                retry += 1
                continue
                
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
                self._tn.write("currentschandlerid\n".encode())
            except OSError as err:
                self.logger.error(f'Keep alive request for query at "{self._host}" failed.')
                self.logger.debug(err)
                # Kill process.
                return False
            time.sleep(freq)