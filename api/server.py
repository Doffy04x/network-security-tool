"""HTTP interface for the port checker used in TP 1 and TP 2."""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

from network_check import check_port, is_valid_port


class Handler(BaseHTTPRequestHandler):
    server_version = "NetSecure"
    sys_version = ""

    def reply(self, status, data):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        request = urlsplit(self.path)
        if request.path == "/health":
            self.reply(200, {"status": "ok"})
            return
        if request.path == "/":
            self.reply(200, {"service": "network-security-tool", "check": "/api/check?port=8000"})
            return
        if request.path != "/check":
            self.reply(404, {"error": "Not found"})
            return
        try:
            query = parse_qs(request.query, strict_parsing=True, keep_blank_values=True)
            if set(query) != {"port"} or len(query["port"]) != 1:
                raise ValueError("Supply one port")
            port = int(query["port"][0])
            if not is_valid_port(port):
                raise ValueError("Invalid port")
        except ValueError:
            self.reply(400, {"error": "Supply one integer port between 1 and 65535"})
            return
        try:
            opened = check_port("127.0.0.1", port, timeout=0.5)
        except OSError:
            self.reply(502, {"error": "Local connection failed"})
            return
        self.reply(200, {"host": "127.0.0.1", "port": port, "open": opened})


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
