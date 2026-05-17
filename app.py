from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import time

class Handler(BaseHTTPRequestHandler):

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        data = json.loads(self.rfile.read(length).decode())

        lead = {
            "name": data.get("name"),
            "email": data.get("email"),
            "service": data.get("service"),
            "message": data.get("message"),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        print("LEAD RECEIVED:", lead)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'{"status":"received"}')

def run():
    server = HTTPServer(("0.0.0.0", 10000), Handler)
    print("CLOUD WEBHOOK READY")
    server.serve_forever()

if __name__ == "__main__":
    run()
