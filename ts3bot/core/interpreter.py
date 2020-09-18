#std
import logging.config

class Interpreter:
    def __init(self, l_queue, s_queue, parser,
               loaded_modules, logging_config, **kwargs):
        """Interpreter for Teamspeak client query events.

        Attributes:
            l_queue (queue): queue from listener
            s_queue (queue): queue for sender
            parser (parse): parser object
            laoded_modules (dict[]): information about active modules
            logging_config (dict): logger configuration
            **kwargs (queue): queues for additional modules
        """
        self.l_queue = l_queue
        self.s_queue = s_queue

        # Configure logging.
        logging.config.dictConfig(logging_config)
        self._logger = logging.getLogger("interpreter")

    def interpret(self):
        """Parse and interpret events from queue.

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
        pass