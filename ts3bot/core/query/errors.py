class AuthError(ConnectionError):
    """Raise when query authentification fails."""
    pass

class QueryTimeout(Exception):
    """Raise when query did not produce output."""
    pass