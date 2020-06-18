# std
import yaml

# local
from ts3bot.api.parser import Parser
from ts3bot.logger import get_logger

class Server_Status:
    def __init__(self):
        """Query information about server and clients."""
        self.logger = get_logger("server_status")
        self.parser = Parser()

        # TODO: Query config, currently hardcoded
        self._freq = 5
        self._max_retry = 5

    def list_current_clients(self, query):
        """
        List all clients currently on the server.
        - query: Client_Query
        
        Return dicts in list:
        clients[{id: ID, ...}, ...]
        """
        clients = [] 
        self.logger.info("Querying for current clients.")
        msg, status = query.send_cmd("clientlist -uid -groups",
                                     self._freq,
                                     self._max_retry)
        return self.parser.parse_response(msg)
