import speech_recognition as sr
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import os
from playsound import playsound
import time
from dotenv import load_dotenv
import json
from datetime import datetime
import msvcrt
import select
import sys

class SpeechTranslator:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.translator = Translator()
        self.temp_audio_file = "temp_audio.mp3"
        self.history_file = "translation_history.json"
        self.is_paused = False
        self.load_history()
        
    def load_history(self):
        """Load translation history from file"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            else:
                self.history = []
        except Exception as e:
            print(f"Error loading history: {e}")
            self.history = []

    def save_history(self, original_text, translated_text, source_lang, target_lang):
        """Save translation to history"""
        translation = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'original_text': original_text,
            'translated_text': translated_text,
            'source_lang': source_lang,
            'target_lang': target_lang
        }
        self.history.append(translation)
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving history: {e}")

    def show_available_languages(self):
        """Display available languages"""
        print("\nAvailable Languages:")
        for code, name in LANGUAGES.items():
            print(f"{code}: {name}")
        print()

    def select_language(self):
        """Let user select target language"""
        self.show_available_languages()
        while True:
            lang_code = input("Enter language code (e.g., 'hi' for Hindi): ").lower()
            if lang_code in LANGUAGES:
                return lang_code
            print("Invalid language code. Please try again.")

    def toggle_pause(self):
        """Toggle pause/resume state"""
        self.is_paused = not self.is_paused
        status = "paused" if self.is_paused else "resumed"
        print(f"\nTranslation {status}")

    def show_history(self):
        """Display recent translation history"""
        if not self.history:
            print("\nNo translation history available.")
            return
        
        print("\nRecent Translations:")
        for i, translation in enumerate(self.history[-5:], 1):
            print(f"\n{i}. {translation['timestamp']}")
            print(f"Original ({translation['source_lang']}): {translation['original_text']}")
            print(f"Translated ({translation['target_lang']}): {translation['translated_text']}")

    def listen_and_recognize(self):
        """Listen to microphone input and convert speech to text"""
        with sr.Microphone() as source:
            print("Listening... Speak now! (Press 'p' to pause/resume, 'h' for history, 'q' to quit)")
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
        """Convert text to speech and play it"""
        if not text:
            return
            
        try:
            tts = gTTS(text=text, lang=lang)
            tts.save(self.temp_audio_file)
            playsound(self.temp_audio_file)
            os.remove(self.temp_audio_file)
        except Exception as e:
            print(f"TTS error: {e}")

    def run(self, target_lang='hi'):
        """Main loop for real-time speech translation"""
        print("Real-time Speech Translator")
        print("Press 'p' to pause/resume")
        print("Press 'h' to view history")
        print("Press 'q' to quit")
        
        while True:
            try:
                # Check for user input
                if os.name == 'nt':  # Windows
                    if msvcrt.kbhit():
                        key = msvcrt.getch().decode().lower()
                        if key == 'p':
                            self.toggle_pause()
                        elif key == 'h':
                            self.show_history()
                        elif key == 'q':
                            print("\nExiting...")
                            return
                else:  # Unix-like systems
                    if select.select([sys.stdin], [], [], 0.0)[0]:
                        key = sys.stdin.read(1).lower()
                        if key == 'p':
                            self.toggle_pause()
                        elif key == 'h':
                            self.show_history()
                        elif key == 'q':
                            print("\nExiting...")
                            return

                if not self.is_paused:
                    # Step 1: Listen and recognize speech
                    text = self.listen_and_recognize()
                    
                    if text:
                        # Step 2: Translate the text
                        translated_text = self.translate_text(text, target_lang)
                        
                        if translated_text:
                            # Step 3: Convert to speech and play
                            self.text_to_speech(translated_text, target_lang)
                            # Step 4: Save to history
                            self.save_history(text, translated_text, 'en', target_lang)
                
                time.sleep(0.1)  # Small delay between iterations
                
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                time.sleep(1)

if __name__ == "__main__":
    translator = SpeechTranslator()
    target_lang = translator.select_language()
    translator.run(target_lang) 