# routes/ocr_route.py
from flask import Blueprint, request, jsonify
import logging
import os
from config import Config
from utils.text_processing import improve_text_with_ollama
from PIL import Image
from io import BytesIO
import base64

logger = logging.getLogger(__name__)

ocr_bp = Blueprint('ocr_bp', __name__)

@ocr_bp.route('/process_ocr', methods=['POST'])
def process_ocr():
    """
    OCR-Endpunkt: Nimmt ein Bild, extrahiert Text mithilfe von OCR, verbessert den Text mit Ollama und gibt den verbesserten Text zurück.
    """
    data = request.get_json()

    if not data:
        logger.warning('Keine JSON-Daten bereitgestellt')
        return jsonify({'error': 'Keine JSON-Daten bereitgestellt'}), 400

    image_str = data.get('image')

    if not image_str:
        logger.warning('Bilddaten fehlen')
        return jsonify({'error': 'Bilddaten fehlen'}), 400

    try:
        # Dekodiere das Base64-Bild
        if ',' in image_str:
            header, encoded = image_str.split(',', 1)
        else:
            header, encoded = '', image_str
        img_data = base64.b64decode(encoded)
        img = Image.open(BytesIO(img_data))

        # Validierung des Bildformats
        if img.format.lower() not in Config.ALLOWED_EXTENSIONS:
            logger.warning(f'Ungültiges Bildformat: {img.format}')
            return jsonify({'error': f'Ungültiges Bildformat: {img.format}'}), 400

        # Speichere das Bild temporär
        img_filename = "temp_ocr.png"
        img_path = os.path.join(Config.UPLOAD_FOLDER, img_filename)
        img.save(img_path)

        # Führe OCR durch (hier solltest du deine OCR-Logik einfügen)
        # Beispiel: extrahierter_text = perform_ocr(img_path)
        # Da OCR-Logik nicht bereitgestellt wurde, nehmen wir an, es wird Text extrahiert
        extrahierter_text = "Beispieltext aus OCR."

        # Verbessere den Text mit Ollama
        verbesserter_text = improve_text_with_ollama(extrahierter_text, model='llama3.2')

        return jsonify({'improved_text': verbesserter_text}), 200

    except Exception as e:
        logger.error(f'Fehler beim Verarbeiten des OCR: {str(e)}')
        return jsonify({'error': f'Fehler beim Verarbeiten des OCR: {str(e)}'}), 500

    finally:
        # Bereinige das temporäre Bild
        if os.path.exists(img_path):
            os.remove(img_path)
