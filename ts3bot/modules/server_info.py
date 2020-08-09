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
        # TODO: Dynamic config, currently hardcoded.
        self._freq = 5
        self._max_retry = 5

    def notify_register(self, query, schandlerid, event):
        """
        Register for output of some commands.
        - query: Client_Query
        - schandlerid: int
        - event: str
        """
        self.logger.debug(f'Registering for event "{event}".')
        status = query.send_cmd("clientnotifyregister " \
                                f"schandlerid={schandlerid} " \
                                f"event={event}")

    def notify_unregister(self, query):
        """
        Unregister from command output.
        - query Client_Query
        """
        self.logger.debug("Unregistering from all events.")
        status = query.send_cmd("clientnotifyunregister")

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
        return self.parser.parse_lines(msg)

    def get_servergroups(self, query, schandlerid):
        """
        List all servergroups on the server.
        - query: Client_Query
        - schandlerid: int

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
        return self.parser.parse_message(msg, "schandlerid=\d+")

    def get_servergroup_perms(self, query, schandlerid, sgid):
        """
        List permissions of specified servergroup.
        - query: Client_query
        - sgid: int

        Return dict
        """
        perms = []
        self.logger.info(f'Querying permissions for servergroup ID "{sgid}".')
        self.notify_register(query, schandlerid, "notifyservergrouppermlist")
        msg = query.send_cmd(f"servergrouppermlist sgid={sgid}",
                             self._freq,
                             self._max_retry)
        self.notify_unregister(query)
        return self.parser.parse_message(msg, "schandlerid=\d+")

    def get_channels(self, query):
        """
        List all server channels.
        - query: Client_Query

        Return dicts in list:
        channels[{id: ID, ...}, ...]
        """
        channels = []
        self.logger.info("Querying for channels on server.")
        msg, status = query.send_cmd("channellist -topic -limits",
                                     self._freq,
                                     self._max_retry,
                                     2)
        return self.parser.parse_lines(msg)

    def get_channel_clients(self, query, cid):
        """
        List all clients currently in specified channel.
        - query: Client_Query
        - cid: int

        Return dicts in list:
        clients[{id: ID, ...}, ...]
        """
        clients = []
        self.logger.info(f'Querying for clients in channel ID "{cid}".')
        msg, status = query.send_cmd(f"channelclientlist cid={cid} " \
                                     "-uid -groups",
                                     self._freq,
                                     self._max_retry,
                                     2)
        return self.parser.parse_lines(msg)

    def get_self_info(self, query):
        """
        List own clid and cid.
        - query: Client_Query

        Return dict:
        self_info{clid: CLID, ...}
        """
        self.logger.info(f"Querying for own IDs.")
        msg, status = query.send_cmd("whoami",
                                     self._freq,
                                     self._max_retry,
                                     2)
        return self.parser.parse_lines(msg)
