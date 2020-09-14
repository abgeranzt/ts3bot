# local
from .query.errors import QueryError, QueryTimeout
from .parser.parser import Parser

class Q_Interface:
    """Various methods for interaction with query objects."""
    def __init__(self):
        pass

    @staticmethod
    def send(query, line, response_len=1):
        """
        Write line to query and return returned lines in list.
        Also return exit code:
        0: OK
        1: Query returned error
        2: Unexpected query behavior
        """
        response = []
        query.write(line)
        try:
            for _ in range(response_len):
                response.append(query.read_line(timeout=2))
            return response, 0
        except QueryTimeout:
            # The query returns only 1 line when the command failed.
            if len(response) == 1:
                return response, 1
            else:
                return response, 2

    @classmethod
    def keep_alive(cls, query):
        """Keep query connection alive."""
        cls.send(query, "whoami", response_len=2)

    @classmethod
    def notify_register(cls, query, event, schandlerid):
        """
        Register for event notifcations.
        Return error and exit code:
        0: OK
        1: Registration failed
        """
        response = cls.send(query,
                            f"clientnotifyregister " \
                            f"schandlerid={schandlerid} " \
                            f"event={event}")
        error = Parser.parse_error(response[0])
        if error["ID"] == 0:
            return error, 0
        else:
            return error, 1

    @classmethod
    def notify_unregister(cls, query):
        """Unregister from event notifications.
         Return error and exit code:
        0: OK
        1: Registration failed
        """
        response = cls.send(query, "clientnotifyunregister")
        error = Parser.parse_error(response[0])
        if error["ID"] == 0:
            return error, 0
        else:
            return error, 1
       