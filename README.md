# Real-Time Speech Translator

This application provides real-time speech translation capabilities using Google's Speech-to-Text, Google Translate, and Text-to-Speech services.

## Features

- Real-time speech recognition
- Text translation to multiple languages
- Text-to-speech output in the target language
- Simple command-line interface

## Prerequisites

- Python 3.7 or higher
- Microphone
- Speakers or headphones
- Internet connection (for Google services)

## Installation

1. Clone this repository or download the files
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python speech_translator.py
   ```

2. When prompted, speak into your microphone
3. The application will:
   - Convert your speech to text
   - Translate the text to Spanish (default)
   - Play the translated text as speech
4. Press Ctrl+C to exit the application

## Supported Languages

The application uses Google Translate's supported languages. By default, it translates to Spanish ('es'), but you can modify the target language in the code.

## Troubleshooting

- If you encounter PyAudio installation issues on Windows, you may need to install it using a wheel file
- Make sure your microphone is properly connected and selected as the default input device
- Ensure you have an active internet connection for the Google services to work

## Note

This application requires an internet connection as it uses Google's services for speech recognition, translation, and text-to-speech conversion. 