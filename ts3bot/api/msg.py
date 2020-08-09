class Msg:
    """ Simple message object."""
    def __init__(self, raw):
        self._raw = raw
        self._kind, self._head, self._body = None
