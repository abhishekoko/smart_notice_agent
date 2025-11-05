# backend/app.py
from flask import Flask, send_from_directory
from flask_cors import CORS
from backend.routes.auth_routes import auth_bp
from backend.routes.notice_routes import notice_bp
import threading
from backend.services.email_listener import EmailReceiver

app = Flask(__name__, static_folder="../frontend", static_url_path="/")
CORS(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix="/api/auth")
# notice blueprint routes are defined relative to '/', so mount at /api/notices
app.register_blueprint(notice_bp, url_prefix="/api/notices")

@app.route("/")
def serve_index():
    return send_from_directory("../frontend", "index.html")

def start_email_listener():
    receiver = EmailReceiver()
    receiver.run()

if __name__ == "__main__":
    # run email listener in background thread (daemon)
    listener_thread = threading.Thread(target=start_email_listener, daemon=True)
    listener_thread.start()
    print("🚀 Flask server started with email listener running in background.")
    app.run(debug=True)
