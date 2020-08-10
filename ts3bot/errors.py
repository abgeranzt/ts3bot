class AuthError(ConnectionError):
    """Raise when query authentification fails."""
    pass

class PermissionError(Exception):
    """Raise when client has insufficient permissions to perform command."""
    pass

class QueryError(Exception):
    """Raise when query behaves unexpectedly."""
    pass

class QueryTimeout(Exception):
    """Raise when query did not produce output."""
    pass
