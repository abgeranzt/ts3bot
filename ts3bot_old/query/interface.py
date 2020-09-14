# local
from ts3bot.errors import QueryError
from ts3bot.query.parser import Parser

class Interface:
    """Various methods for interaction with query objects."""
    def __init__(self):
        pass

    @staticmethod
    def send(query, line, response_len=1):
        """Write line to query and return reponse lines as [str, ...]."""
        response = []
        query.write(line)
        try:
            for _ in range(response_len):
                response.append(query.read_line(2))
        except QueryTimeout:
            # The query returns only 1 line when the command failed.
            if len(reponse) > 0 and response_len > 1:
                response[1] = response[0]
                response[0] = False
            else:
                raise QueryError("Query did not answer properly!")
        return response

    @classmethod
    def keep_alive(cls, query):
        """Keep query connection alive."""
        cls.send(query, "whoami", 2)

    @classmethod
    def notify_register(cls, query, event, schandlerid):
        """
        Register for event notifcations.
        Return True if successfull, otherwise return error object.
        """
        response = cls.send(query,
                            f"clientnotifyregister " \
                            f"schandlerid={schandlerid} " \
                            f"event={event}")
        error = Parser.parse_error(response[0])
        if error.error_id == 0:
            return True
        else:
            return error
    @classmethod
    def notify_unregister(cls, query):
        """Unregister from event notifications."""
        cls.send(query, "clientnotifyunregister")
