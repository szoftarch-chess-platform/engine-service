from http.server import BaseHTTPRequestHandler, HTTPServer
import os


class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"healthy")
            return

        self.send_response(404)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"not found")

    def log_message(self, format, *args):
        return


def run():
    port = int(os.getenv("PORT", "80"))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    print(f"Health check service listening on port {port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
