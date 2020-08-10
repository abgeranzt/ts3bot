# std
import os
import time
import yaml

# local
from ts3bot.errors import AuthError, QueryTimeout
from ts3bot.logger import get_logger
from ts3bot.query.interface import Interface as iface
from ts3bot.query.query import Query
from ts3bot.threads.job import Job

# TODO: Implement error codes upon thread termination.
# Always returns false at the moment.

class Listener:
    def __init__(self, queue):
        self._cfg = self._load_cfg()
        self._logger = get_logger("listener")
        self._query = Query(self._cfg["query"], self._logger)
        self._queue = queue

    # --- Public Methods ---

    def listen(self):
        """
        Listen query and create jobs.
        Return False if interrupted.
        """
        # Establish connection.
        self._logger.info("INIT (1/2): Connecting to query.")
        if not self._connect():
            return False
        # Register for notifications.
        self._logger.info("INIT (2/2): Registering for event notifications.")
        if not self._register():
            return False
        # Listen.
        self._logger.info("Init complete. Listening.")
        while True:
            try:
                line = self._query.read_line(120)
                self._logger.debug("Found line. Creating Job.")
                job = Job("query_event", line, "listener", "worker")
                self._queue.put(job)
            except QueryTimeout:
                iface.keep_alive(self._query)

    # --- Private Methods ---

    def _connect(self):
        """Establish connection."""
        try:
            # Attempt to connect 3 times.
            for attempt in range(2):
                if self._query.connect():
                   return True
                time.sleep(5)
                self._logger.info("Retrying connection.")
            self._logger.critical("Connection to query failed!")
            return False
        except AuthError:
            return False

    def _register(self):
        """Register for notifications."""
        for event in self._cfg["events"]:
            self._logger.info(f'Registering for event "{event}".')
            response = iface.notify_register(self._query, event, self._cfg["schandlerid"])
            # Response is bool if successfull.
            if response == True:
                continue
            else:
                self._logger.critical(f'Registration for event "{event}" failed!')
                self._logger.error(response.error_def)
                return False
        return True

    @staticmethod
    def _load_cfg():
        """Load config and return it as dict."""
        cfg_path = os.path.join("config", "local", "listener.yaml")
        with open(cfg_path, "r") as cfg_file:
            cfg = yaml.safe_load(cfg_file)
        return cfg
