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

        # FIXME: Remove carriage returns and line breaks from logs.
        # TODO: Query config, currently hardcoded
        self._freq = 5
        self._max_retry = 5

    def notify_register(self, query, schandlerid, event):
        """
        Register for output of some commands.
        - query: Client_Query
        - schandlerid: str
        - event: str
        """
        self.logger.debug(f'(1/3) Registering for event "{event}".')
        status = query.send_cmd(f"clientnotifyregister schandlerid={schandlerid} " \
                                f"event={event}")
        self.logger.debug(f'(2/3) Status = "{status}".')
        self.logger.debug(f'(3/3) Registered for event "{event}".')

    def notify_unregister(self, query):
        """
        Unregister from command output.
        - query Client_Query
        """
        self.logger.debug("(1/3) Unregistering from all events.")
        status = query.send_cmd("clientnotifyunregister")
        self.logger.debug(f'(2/3) Status = "{status}".')
        self.logger.debug("(3/3) Unregistered from all events.")

    def get_current_clients(self, query):
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
                                     self._max_retry,
                                     2)
        return self.parser.parse_response(msg)

    def get_servergroups(self, query, schandlerid):
        """
        List all servergroups on the server.
        - query: Client_Query
        - schandlerid: str

        Return dicts in list:
        servergroups[{id: ID, ...}, ...]
        """
        servergroups = []
        self.logger.info("Querying for servergroups.")
        self.notify_register(query, schandlerid, "notifyservergrouplist")
        msg = query.send_cmd("servergrouplist",
                             self._freq,
                             self._max_retry)
        self.notify_unregister(query)
        return self.parser.parse_notify(msg, "schandlerid=\d+\s")

    def get_servergroup_perms(self, query, schandlerid, sgid):
        """
        List permissions of specified servergroup.
        - query: Client_query
        - sgid: str

        Return dict
        """
        perms = []
        self.logger.info(f'Querying permissions for servergroup id "{sgid}".')
        self.notify_register(query, schandlerid, "notifyservergrouppermlist")
        msg = query.send_cmd(f"servergrouppermlist sgid={sgid}",
                             self._freq,
                             self._max_retry)
        self.notify_unregister(query)
        return self.parser.parse_notify(msg, "schandlerid=\d+\s")
