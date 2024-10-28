
def handle_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.ConnectionError as e:
            print("[CONN ERR]", e)
            return Response(
                response=b"Connection Error: Unable to connect to the upstream server.",
                status=502  # Bad Gateway
            )
        except requests.exceptions.Timeout as e:
            print("[TIMEOUT ERR]", e)
            return Response(
                response=b"Gateway Timeout: The upstream server is taking too long to respond.",
                status=504  # Gateway Timeout
            )
        except requests.exceptions.TooManyRedirects as e:
            print("[REDIRECT ERR]", e)
            return Response(
                response=b"Too Many Redirects: The upstream server is redirecting too many times.",
                status=502  # Bad Gateway
            )
        except requests.exceptions.RequestException as e:
            print("[REQUEST ERR]", e)
            return Response(
                response=b"An error occurred with the request.",
                status=500  # Internal Server Error
            )
    return wrapper
