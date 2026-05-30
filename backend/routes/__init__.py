from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')
contacts_bp = Blueprint('contacts', __name__, url_prefix='/api/contacts')

# Import route handlers
from routes.auth import *
from routes.chat import *
from routes.contacts import *
