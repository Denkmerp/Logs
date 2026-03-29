from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from datetime import datetime
import os

chat_logs = []

class ChatHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/log":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)

            try:
                data = json.loads(body)
                player = data.get("player", "Unknown")
                userId = data.get("userId", "N/A")
                message = data.get("message", "")
                timestamp = data.get("timestamp", 0)

                time_str = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

                entry = {
                    "player": player,
                    "userId": userId,
                    "message": message,
                    "time": time_str
                }

                chat_logs.append(entry)
                print(f"[{time_str}] {player} (ID: {userId}): {message}", flush=True)

                self._respond(200, {"status": "ok"})

            except Exception as e:
                print(f"Error: {e}", flush=True)
                self._respond(400, {"status": "error"})

        else:
            self._respond(404, {"status": "not found"})

    def _respond(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Railway uses 8080 by default
    print(f"Chat logger running on port {port}", flush=True)
    HTTPServer(("0.0.0.0", port), ChatHandler).serve_forever()
