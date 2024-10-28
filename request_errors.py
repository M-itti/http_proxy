from requests.exceptions import ConnectionError, Timeout, TooManyRedirects, RequestException

def gateway_errors(e):
    if isinstance(e, ConnectionError):
        print("[CONN ERR]", e)
        return resp("Connection Error: Unable to connect to the upstream server.", 502)
    elif isinstance(e, Timeout):
        print("[TIMEOUT ERR]", e)
        return resp("Gateway Timeout: The upstream server is taking too long to respond.", 504)
    elif isinstance(e, TooManyRedirects):
        print("[REDIRECT ERR]", e)
        return resp("Too Many Redirects: The upstream server is redirecting too many times.", 502)
    elif isinstance(e, RequestException):
        print("[REQUEST ERR]", e)
        return resp("An error occurred with the request.", 500)

def resp(message: str, status: int) -> Response:
    """Helper function to create a Response object."""
    return Response(
        response=message.encode('utf-8'),  # Encode the message as bytes
        status=status
    )
