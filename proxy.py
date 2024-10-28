from werkzeug.wrappers import Request, Response
from request_errors import gateway_errors
from wsgiref.simple_server import make_server
import requests

def get_headers(request):
    return {header: value for header, value in request.headers.items()}

def rm_HopByHop(headers):
    hop_by_hop_headers = {
        "Connection", "Proxy-Connection", "Keep-Alive", 
        "Transfer-Encoding", "TE", "Trailer", "Upgrade"
    }
    return {key: value for key, value in headers.items() if key not in hop_by_hop_headers}

def application(env, start_response):
    request = Request(env)
    upstream_url = env["PATH_INFO"]
    
    client_headers = get_headers(request)

    if env['REQUEST_METHOD'] == 'GET':
        try:
            # send request to upstream server
            r = requests.get(
                url=upstream_url,
                headers=client_headers
            )
            # extract response from upstream server 
            status = str(r.status_code)
            body = r.content if r.content is not None else b""
            server_headers = rm_HopByHop(r.headers)
            
            # send the response back to client 
            response = Response(
                response=body,  
                status=status,     
                headers={key: value for key, value in server_headers.items()}
            )
            return response(env, start_response)

        except RequestException as e:
            response = gateway_errors(e)
            return response(env, start_response)

    if env['REQUEST_METHOD'] == 'POST':
        try:
            content_length = int(env.get('CONTENT_LENGTH', 0))
            
            # Read the request body
            request_body = env['wsgi.input'].read(content_length)

            r = requests.post(
                url=upstream_url,
                headers=client_headers,
                data=request_body
            )

            status = str(r.status_code)
            body = r.content if r.content is not None else b""
            server_headers = r.headers

            response = Response(
                response=body,  
                status=status,     
                headers={key: value for key, value in server_headers.items()}
            )
        except RequestException as e:
            response = gateway_errors(e)
            return response(env, start_response)

    if env['REQUEST_METHOD'] == 'PUT':
        try:
            content_length = int(env.get('CONTENT_LENGTH', 0))
            request_body = env['wsgi.input'].read(content_length)

            r = requests.put(
                url=upstream_url,
                headers=client_headers,
                data=request_body
            )

            status = str(r.status_code)
            body = r.content if r.content is not None else b""
            server_headers = r.headers

            response = Response(
                response=body,  
                status=status,     
                headers={key: value for key, value in server_headers.items()}
            )
        except RequestException as e:
            response = gateway_errors(e)
            return response(env, start_response)

    if env['REQUEST_METHOD'] == 'DELETE':
        try:
            r = requests.delete(
                url=upstream_url,
                headers=client_headers
            )

            status = str(r.status_code)
            body = r.content if r.content is not None else b""
            server_headers = r.headers

            response = Response(
                response=body,
                status=status,
                headers={key: value for key, value in server_headers.items()}
            )
        except RequestException as e:
            response = gateway_errors(e)
            return response(env, start_response)

if __name__ == "__main__":
    port = 8080
    print(f"Starting WSGI server on port {port}...")
    with make_server('', port, application) as server:
        server.serve_forever()
