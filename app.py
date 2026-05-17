from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import time

leads = []

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

        leads.append(lead)

        print("LEAD STORED:", lead)
        print("TOTAL LEADS:", len(leads))

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'{"status":"stored"}')

def run():
    server = HTTPServer(("0.0.0.0", 10000), Handler)
    print("WEBHOOK RUNNING WITH STORAGE")
    server.serve_forever()

if __name__ == "__main__":
    run()
