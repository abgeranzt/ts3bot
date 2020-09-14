class AuthError(ConnectionError):
    """Raise when query authentification fails."""
    pass

class QueryError(Exception):
    """Raise when query behaves unexpectedly."""
    pass

class QueryTimeout(Exception):
    """Raise when query did not produce output."""
    pass