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

    def report_error(self, status):
        """
        Print error information to log.
        status: str
        """
        for key in status["body"]:
            self.logger.debug(f'{key}: {status["body"][key]}')
        try:
            self.logger.warn(self._errors[status["body"]["id"]]["def"])
        except KeyError:
            self.logger.critical("Unknown error ID! See debug messages.")


    def move_client(self, query, cid, clid):
        """
        Move client to specified channel.
        query: Client_Query
        cid: int
        clid: int

        Return True if successfull.
        Otherwise return false.
        """
        self.logger.info(f'Moving client "{clid}" to channel "{cid}".')
        status = self.parser.parse_message(
            query.send_cmd(f"clientmove cid={cid} clid={clid}"))
        if status["body"]["id"] == 0:
            return True
        else:
            self.logger.warn("Moving client failed!")
            self.report_error(status)
            return False

    def send_message(self, query, msg, targetmode, clid=0):
        """
        Send message according to targetmode.
        query: Client_Query
        msg: str
        targetmode: int
        clid: int

        Return True if successfull,
        Otherwise return false.
        """
        targets = {
            1: f'client "{clid}"',
            2: "current channel",
            3: "server"}
        self.logger.info(f'Sending message to {targets[targetmode]}.')
        self.logger.debug(f'Msg: "{msg}"')
        status = self.parser.parse_message(
            query.send_cmd(f"sendtextmessage targetmode={targetmode} " \
                           f"target={clid} msg={msg}"))
        if status["body"]["id"] == 0:
            return True
        else:
            self.logger.warn("Sending private text message failed!")
            self.report_error(status)
            return False


