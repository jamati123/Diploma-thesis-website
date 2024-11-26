# routes/__init__.py
from flask import Blueprint

ocr_bp = Blueprint('ocr_bp', __name__)

# routes/__init__.py
from .ocr_route import ocr_bp
from .chat_route import chat_bp
