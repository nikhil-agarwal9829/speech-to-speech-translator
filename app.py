from flask import Flask, request, jsonify, send_from_directory
from speech_translator import SpeechTranslator
import os
from werkzeug.utils import secure_filename
import wave
import contextlib

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

translator = SpeechTranslator()

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/translate', methods=['POST'])
def translate():
    try:
        # Get the audio file from the request
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        target_lang = request.form.get('target_lang', 'hi')
        
        if audio_file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
            
        # Save the audio file temporarily
        filename = secure_filename(audio_file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        audio_file.save(filepath)
        
        # Verify the WAV file
        try:
            with contextlib.closing(wave.open(filepath, 'rb')) as wav_file:
                # Check if it's a valid WAV file
                if wav_file.getnchannels() not in [1, 2]:
                    return jsonify({'error': 'Invalid WAV file: must be mono or stereo'}), 400
                if wav_file.getsampwidth() != 2:
                    return jsonify({'error': 'Invalid WAV file: must be 16-bit'}), 400
        except Exception as e:
            return jsonify({'error': f'Invalid WAV file: {str(e)}'}), 400
        
        # Process the audio file
        text = translator.listen_and_recognize(filepath)
        if not text:
            return jsonify({'error': 'Could not understand audio'}), 400
            
        # Translate the text
        translated_text = translator.translate_text(text, target_lang)
        if not translated_text:
            return jsonify({'error': 'Translation failed'}), 400
            
        # Generate speech
        audio_path = translator.text_to_speech(translated_text, target_lang)
        
        # Clean up
        os.remove(filepath)
        
        return jsonify({
            'original_text': text,
            'translated_text': translated_text,
            'audio_url': audio_path
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/preview', methods=['POST'])
def preview_language():
    try:
        data = request.get_json()
        text = data.get('text', '')
        language = data.get('language', 'en')
        
        # Generate audio file
        audio_path = f'static/preview_{language}.wav'
        translator.text_to_speech(text, language, audio_path)
        
        return jsonify({
            'audio_url': f'/static/preview_{language}.wav'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 