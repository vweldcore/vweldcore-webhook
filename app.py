from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import time
import smtplib
from email.mime.text import MIMEText

leads = []

# ====== EMAIL CONFIG (PUT YOUR DETAILS HERE) ======
GMAIL_USER = "info.vweldcore@gmail.com"
APP_PASSWORD = "fmkhrgfzmmddzlfp"

def send_email(to_email, name, service):
    subject = "VWELDCORE Inquiry Received"
    body = f"""
Hello {name},

We have received your request for: {service}

Our team will contact you shortly with pricing and details.

VWELDCORE SYSTEM
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = GMAIL_USER
    msg["To"] = to_email

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=20)
    server.login(GMAIL_USER, APP_PASSWORD)
    server.sendmail(GMAIL_USER, to_email, msg.as_string())
    server.quit()


class Handler(BaseHTTPRequestHandler):

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        data = json.loads(self.rfile.read(length).decode())

        name = data.get("name")
        email = data.get("email")
        service = data.get("service")

        lead = {
            "name": name,
            "email": email,
            "service": service,
            "message": data.get("message"),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        leads.append(lead)

        print("LEAD STORED:", lead)
        print("TOTAL LEADS:", len(leads))

        try:
            send_email(email, name, service)
            print("EMAIL SENT TO:", email)
        except Exception as e:
            print("EMAIL FAILED:", e)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'{"status":"processed"}')


def run():
    server = HTTPServer(("0.0.0.0", 10000), Handler)
    print("VWELDCORE AUTO-REPLY ACTIVE")
    server.serve_forever()


if __name__ == "__main__":
    run()
