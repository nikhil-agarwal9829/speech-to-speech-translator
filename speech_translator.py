import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
from playsound import playsound
import time
from dotenv import load_dotenv

class SpeechTranslator:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.translator = Translator()
        self.temp_audio_file = "temp_audio.mp3"
        
    def listen_and_recognize(self):
        """Listen to microphone input and convert speech to text"""
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
                        self.text_to_speech(translated_text, target_lang)
                
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