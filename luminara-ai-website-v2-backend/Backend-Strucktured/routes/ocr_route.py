# routes/ocr_route.py
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
import logging

from config import Config
from utils.ocr import perform_ocr
from utils.text_processing import improve_text_with_ollama
from utils.markdown_converter import convert_to_markdown

logger = logging.getLogger(__name__)

ocr_bp = Blueprint('ocr_bp', __name__)

@ocr_bp.route('/api/ocr', methods=['POST'])
def ocr_endpoint():
    """
    OCR Endpunkt: Nimmt ein Bild entgegen, führt OCR durch, verbessert den Text mit Ollama und gibt beide Versionen zurück.
    """
    if 'image' not in request.files:
        logger.warning('Kein Bild bereitgestellt')
        return jsonify({'error': 'Kein Bild bereitgestellt'}), 400

    file = request.files['image']

    if file.filename == '':
        logger.warning('Kein ausgewähltes Bild')
        return jsonify({'error': 'Kein ausgewähltes Bild'}), 400

    if file and allowed_file(file.filename, Config.ALLOWED_EXTENSIONS):
        filename = secure_filename(file.filename)
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        logger.info(f'Bild gespeichert: {filepath}')

        try:
            # OCR durchführen
            ocr_text = perform_ocr(filepath, lang=Config.TESSERACT_LANG)
            logger.info(f'OCR Extrahierter Text: {ocr_text}')

            if not ocr_text.strip():
                logger.warning('OCR hat keinen Text gefunden')
                return jsonify({'error': 'OCR hat keinen Text gefunden'}), 400

            # Text mit Ollama verbessern
            markdown_text = improve_text_with_ollama(ocr_text, model=Config.OLLAMA_MODEL_DEFAULT)
            logger.info(f'Verbesserter Text: {markdown_text}')

            if not markdown_text.strip():
                logger.warning('Ollama hat den Text nicht verbessert')
                return jsonify({'error': 'Ollama hat den Text nicht verbessert'}), 500

            # In Markdown umwandeln
            markdown_text = convert_to_markdown(markdown_text)
            logger.info('Markdown generiert')

            # Rückgabe beider Versionen
            return jsonify({
                'ocr_text': ocr_text,
                'markdown': markdown_text
            }), 200
        except Exception as e:
            logger.error(f'Fehler bei der Verarbeitung: {str(e)}')
            return jsonify({'error': str(e)}), 500
        finally:
            # Optional: Lösche das hochgeladene Bild nach der Verarbeitung
            if os.path.exists(filepath):
                os.remove(filepath)
                logger.info(f'Bild gelöscht: {filepath}')
    else:
        logger.warning('Ungültiger Dateityp')
        return jsonify({'error': 'Ungültiger Dateityp'}), 400

def allowed_file(filename, allowed_extensions):
    """
    Überprüft, ob die Datei eine erlaubte Erweiterung hat.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions
