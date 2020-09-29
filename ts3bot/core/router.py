#std
import logging.config
import re

class Router:
    """Router for Teamspeak client query events.

    Attributes:
        l_queue (queue): queue from listener
        s_queue (queue): queue for sender
        parser (parse): parser object
        modules (dict): queues and information for active modules as dicts in list
        logging_config (dict): logger configuration
    """
    def __init__(self, l_queue, s_queue, parser,
               modules, logging_config):
        self.l_queue = l_queue
        self.s_queue = s_queue
        self._parser = parser
        self._modules = modules

        # Configure logging.
        logging.config.dictConfig(logging_config)
        self._logger = logging.getLogger("router")

    def route(self):
        """Parse, interpret and route events from queue.

        1. Parse event.
        2. Decide whether and how to act upon event.
        3. Pass job to corresponding queue.
        
        Return status code upon termination.

        Returns:
            status (int): status code

        Status codes:
            1: error
            2: queue error
        """
        queues = self._modules["QUEUES"]
        self._logger.info("Router started")
        while True:
            event = self._parser.parse_event(self.l_queue.get())
            self._logger.debug("Found event")
            # Handle text chat.
            if re.search("notifytextmessage", event["NAME"]):
                message = event["ROWS"][0]["msg"]
                command = re.search(r"^!(\w+)", message)
                if command:
                    command = command.group(1)
                    self._logger.debug(f'Parsing command: "{command}"')
                    try:
                        # Check if command exists
                        module = self._modules["COMMANDS"][command]
                        queues[module].put({"NAME": command,
                                            "EVENT": event})
                    except KeyError:
                        self._logger.debug('Received invalid command')
                        self.s_queue.put({"NAME": "response",
                                          "EVENT": event,
                                          "RESPONSE": "Command not found."})
                # Message has no "!" prefix:
                else:
                    self._logger.debug(f'Ignoring chatmessage: "{message}"')
                    continue
            # Handle serverwide events.
            else:
                try:
                    # Get module name using the event.
                    module = self._modules["EVENTS"][event["NAME"]]
                    # more than one module uses the event:
                    if type(module) == list:
                        for mod in module:
                            queues[module].put({"NAME": mod,
                                                "EVENT": event})
                    else: 
                        queues[module].put({"NAME": module,
                                            "EVENT": event})
                except KeyError:
                    self._logger.warn(f'Event not handled: "{event["NAME"]}"')
                    continue
        return 1
