# std
import time
import yaml

# local
from ts3bot.api.client_query import Client_Query
from ts3bot.api.parser import Parser
from ts3bot.logger import get_logger
from ts3bot.server_action import Server_Action
from ts3bot.server_status import Server_Status

class Listener:
    def __init__(self):
        """Listen on query connection and act upon notification."""
        self.logger = get_logger("listener")
        self.parser = Parser()
        self.server_action = Server_Action()
        self.server_status = Server_Status()
        try:
            with open("config/listener.yaml", "r") as cfg:
                self._cfg = yaml.safe_load(cfg)
        # TODO Improve this.
        except FileNotFoundError:
            self.logger.critical("No config file detected!")
            raise FileNotFoundError
        self.query = Client_Query(self._cfg["host"],
                                  self._cfg["port"],
                                  self._cfg["apikey"])

    def start(self):
        freq = self._cfg["freq"]
        retry = 0
        while True:
            try:
                self.query.connect()
                for msg in self.query.listen():
                    # TODO Implement this
                    pass
                except ConnectionAbortedError:
                    self.logger.info("Connection closed. Reconnecting.")
                    continue
                except ConnectionError
                    self.logger.info(f"Connection failed. Attempting to reconnect in {freq} seconds.")
                    time.sleep(freq)
                    # TODO Improve this.
                    if retry > 3:
                        freq = 60
                    elif retry > 10:
                        freq = 600
                    elif retry > 20:
                        freq = 3600
                    retry += 1
                    continue

