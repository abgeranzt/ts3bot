# std
import yaml

# local
from ts3bot.logger import get_logger
from ts3bot.api.parser import Parser

class Server_Action:
    def __init__(self):
        """Interact with server and clients."""
        self.logger = get_logger("server_action")
        self.parser = Parser()
        # TODO: Query config, currently hardcoded.
        self._freq = 5
        self._max_retry = 5
        with open("config/errors.yaml", "r") as errors:
            self._errors = yaml.safe_load(errors)

    def move_client(self, query, cid, clid):
        """
        Move client to specified channel.
        query: Client_Query
        cid: str
        clid: str

        Return True if successfull,
        Otherwise return false.
        """
        self.logger.info(f'Moving client "{clid}" to channel "{cid}".')
        status = self.parser.parse_message(
            query.send_cmd(f"clientmove cid={cid} clid={clid}"))
        if status["body"]["id"] == 0:
            return True
        else:
            self.logger.warn("Moving client failed!")
            for key in status["body"]:
                self.logger.debug(f'{key}: {status["body"][key]}')
            try:
                self.logger.warn(self._errors[status["body"]["id"]]["def"])
            except KeyError:
                self.logger.critical("Unknown error ID! See debug messages.")
            return False
