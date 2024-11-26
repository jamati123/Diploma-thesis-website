# routes/chat_route.py
from flask import Blueprint, request, jsonify
import logging

from config import Config
from utils.text_processing import ask_ollama

logger = logging.getLogger(__name__)

chat_bp = Blueprint('chat_bp', __name__)

@chat_bp.route('/ask_ollama', methods=['POST'])
def ask_ollama_endpoint():
    """
    Chat-Endpunkt: Nimmt eine Benutzeranfrage und ein Modell, kommuniziert mit Ollama und gibt die Antwort zurück.
    """
    data = request.get_json()

    if not data:
        logger.warning('Keine JSON-Daten bereitgestellt')
        return jsonify({'error': 'Keine JSON-Daten bereitgestellt'}), 400

    prompt = data.get('prompt')
    model = data.get('model', Config.OLLAMA_MODEL_DEFAULT)  # Standardmodell

    if not prompt:
        logger.warning('Prompt fehlt')
        return jsonify({'error': 'Prompt fehlt'}), 400

    try:
        response = ask_ollama(prompt, model=model)

        if 'choices' in response:
            return jsonify(response), 200
        else:
            return jsonify(response), 500

    except Exception as e:
        logger.error(f'Fehler beim Kommunizieren mit Ollama: {str(e)}')
        return jsonify({'error': 'Fehler beim Kommunizieren mit Ollama'}), 500
