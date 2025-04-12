from flask import Blueprint, request, send_file
from gtts import gTTS
import os

# Create a Blueprint (modular Flask component)
tts_bp = Blueprint("tts", __name__)

@tts_bp.route('/speak')
def speak():
    text = request.args.get('text', '')
    lang = request.args.get('lang', 'ta')  # Default to Tamil

    if not text:
        return "Error: No text provided.", 400

    audio_path = "static/audio.mp3"

    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(audio_path)
    except Exception as e:
        return f"Error generating speech: {str(e)}", 500

    return send_file(audio_path, mimetype="audio/mpeg")
