# std
import yaml

# local
from ts3bot.logger import get_logger

class Server_Action:
    def __init__(self):
        """Interact with server and clients."""
        self.logger = get_logger("server_action")
        # TODO: Query config, currently hardcoded.
        # TODO: Handle status messages.
        self._freq = 5
        self._max_retry = 5

    def move_client(self, query, cid, clid):
        """
        Move client to specified channel.
        query: Client_Query
        cid: str
        clid: str

        Return True if successfull,
        Otherwise raise error.
        """
        self.logger.info(f'Moving client "{clid}" to channel "{cid}".')
        status = query.send_cmd(f"clientmove cid={cid} clid={clid}")
        self.logger.info(f'Successfully moved client "{clid}" to channel "{cid}".')
        return True
        # TODO: Handle insufficient permissions.
