import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from kiteconnect import KiteConnect
from core.interfaces import BaseAuth

class KiteAuth(BaseAuth):
    def __init__(self, api_key: str, api_secret: str, port: int = 5000):
        self.api_key = api_key
        self.api_secret = api_secret
        self.port = port
        self.kite = KiteConnect(api_key=api_key)
        self.captured_request_token = None

    def login(self) -> str:
        login_url = self.kite.login_url()
        print(f"Opening browser for Kite login: {login_url}")
        webbrowser.open(login_url)

        port = self.port
        captured = self.captured_request_token

        class RedirectHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                nonlocal captured
                parsed_path = urlparse(self.path)
                query_params = parse_qs(parsed_path.query)
                if "request_token" in query_params:
                    outer_self = self
                    # Store via closure/ nonlocal reference
                    global _last_captured_token
                    _last_captured_token = query_params["request_token"][0]
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(b"<h3>Authentication successful! You can close this tab.</h3>")
                else:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b"<h3>Error: Request token not found.</h3>")
            
            def log_message(self, format, *args):
                pass

        server_address = ('127.0.0.1', self.port)
        httpd = HTTPServer(server_address, RedirectHandler)
        print(f"Listening on http://127.0.0.1:{self.port} for redirect...")
        httpd.handle_request() # Handle single auth request

        global _last_captured_token
        if '_last_captured_token' in globals() and _last_captured_token:
            data = self.kite.generate_session(_last_captured_token, api_secret=self.api_secret)
            access_token = data["access_token"]
            self.kite.set_access_token(access_token)
            print("Kite session generated successfully.")
            return access_token
        raise RuntimeError("Failed to capture request token.")
