# TODO Syntax check. This does not look right.

class AuthError(ConnectionError):
    """Raise when query authentification fails."""

class PermissionError():
    """Raise when client has insufficient permissions to perform command."""

class QueryError():
    """Raise when query behaves unexpectedly."""
