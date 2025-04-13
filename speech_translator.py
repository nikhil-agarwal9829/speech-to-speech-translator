import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
from playsound import playsound
import time
from dotenv import load_dotenv
import uuid
import wave
import contextlib

class SpeechTranslator:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.translator = Translator()
        self.audio_output_dir = "static/audio"
        os.makedirs(self.audio_output_dir, exist_ok=True)
        
    def listen_and_recognize(self, audio_file=None):
        """Listen to microphone input or process audio file and convert speech to text"""
        if audio_file:
            # Verify the WAV file format
            try:
                with contextlib.closing(wave.open(audio_file, 'rb')) as wav_file:
                    if wav_file.getnchannels() not in [1, 2]:
                        print("Invalid WAV file: must be mono or stereo")
                        return None
                    if wav_file.getsampwidth() != 2:
                        print("Invalid WAV file: must be 16-bit")
                        return None
            except Exception as e:
                print(f"Error reading WAV file: {e}")
                return None

            with sr.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)
        else:
            with sr.Microphone() as source:
                print("Listening... Speak now!")
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source)
            
        try:
            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None

    def translate_text(self, text, target_lang='hi'):
        """Translate text to target language"""
        if not text:
            return None
            
        try:
            translation = self.translator.translate(text, dest=target_lang)
            print(f"Translation: {translation.text}")
            return translation.text
        except Exception as e:
            print(f"Translation error: {e}")
            return None

    def text_to_speech(self, text, lang='hi'):
        """Convert text to speech and save it"""
        if not text:
            return None
            
        try:
            # Generate unique filename
            filename = f"{uuid.uuid4()}.mp3"
            filepath = os.path.join(self.audio_output_dir, filename)
            
            tts = gTTS(text=text, lang=lang)
            tts.save(filepath)
            return f"/static/audio/{filename}"
        except Exception as e:
            print(f"TTS error: {e}")
            return None

    def run(self, target_lang='hi'):
        """Main loop for real-time speech translation"""
        print("Real-time Speech Translator (English to Hindi)")
        print("Press Ctrl+C to exit")
        
        while True:
            try:
                # Step 1: Listen and recognize speech
                text = self.listen_and_recognize()
                
                if text:
                    # Step 2: Translate the text
                    translated_text = self.translate_text(text, target_lang)
                    
                    if translated_text:
                        # Step 3: Convert to speech and play
                        audio_path = self.text_to_speech(translated_text, target_lang)
                        if audio_path:
                            playsound(os.path.join("static", audio_path.lstrip("/")))
                
                time.sleep(0.5)  # Small delay between iterations
                
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                time.sleep(1)

if __name__ == "__main__":
    translator = SpeechTranslator()
    translator.run() 