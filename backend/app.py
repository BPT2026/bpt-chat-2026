from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'dev-secret-key')

# Enable CORS
CORS(app)

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# Import routes and events
from routes import auth_bp, chat_bp, contacts_bp
from events import socket_events

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(contacts_bp)

@app.route('/')
def home():
    return {'message': 'BPTChat API is running'}

if __name__ == '__main__':
    PORT = int(os.getenv('SERVER_PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=PORT, debug=True)
