#std
import logging.config
import time

class Listener:
    """Listener for TeamSpeak client query.

    Attributes:
        events (str[]): events to listen for
        query (query): query interface
        queue (queue): queue for interpreter
        logging_config (dict): logger configuration 
    """
    def __init__(self, events, query, queue, logging_config):
        self.EVENTS = events
        self._query = query
        self.queue = queue

        # Configure logging.
        logging.config.dictConfig(logging_config)
        self._logger = logging.getLogger("listener")

    def listen(self):
        """Listen on query and queue output for processing.
        
        1. Establish query connection.
        2. Register for events.
        3. Listen for events and put raw output into queue.

        Return status code upon termination.

        Returns:
            status (int): status code

        Status codes:
            1: connection error
            2: query returned error
            3: auth error
        """
        # Establish connection
        self._logger.info("Establishing query connection")
        status = self._connect()
        if status != 0:
            self._logger.error("Could not establish query connection!")
            self._logger.critical(f"Terminating! ({status})")
            return status

        # Register for events.
        self._logger.info("Registering for events")
        status = self._register()
        if status != 0:
            self._logger.error("Event registration failed completely!")
            self._logger.critical(f"Terminating! ({status})")
            return status

        # Listen.
        self._logger.info(f"Listening on query at {self._query.HOST}:" \
                          f"{self._query.PORT}")
        while True:
            status, event = self._query.read_line(timeout=120)
            if status == 0:
                self._logger.debug("Found event.")
                self.queue.put(event)
            elif status == 2:
                self._query.keep_alive()
            else:
                self._logger.error("Lost query connection!")
                return status

    def _connect(self):
        """Establish query connection.
        
        Returns:
            status (int): status code

        Status codes:
            0: OK
            1: connection error
            3: auth error
        """
        # 3 Attempts before aborting
        for attempt in range(1, 4):
            self._logger.debug(f"Connection attempt {attempt}")
            status = self._query.connect()
            if status == 0:
                self._logger.info("Connection established")
                break
            time.sleep(3)
        return status

    def _register(self):
        """Register for event notifications.
        
        Returns:
            status (int): status code

        Status codes:
            0: OK
            1: connection error
        """
        for event in self.EVENTS:
            self._logger.debug(f"Registering for event {event}")
            status, response = self._query.notify_register(event)
            if status == 0:
                self._logger.info(f'Registered for event "{event}"')
                continue
            elif status == 1:
                self._logger.error("Lost query connection!")
                return status
            else:
                self._logger.error(f'Registration for event "{event}"' \
                                   'failed!')
                self._logger.debug(response)
                continue
        return 0