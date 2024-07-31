# Enhanced Language Detection and Translation API

This Flask-based API provides comprehensive language-related services using Google Cloud APIs and other libraries.

## Features

- Detect language of a given text
- Detect languages of multiple texts
- Translate text to a target language
- Translate text to multiple target languages
- Detect language from uploaded file
- Auto-translate text (detect source language and translate to target)
- Get list of supported languages
- Convert text to speech
- Summarize text
- Perform sentiment analysis
- Use custom language models for classification

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install flask langdetect google-cloud-translate google-cloud-texttospeech google-cloud-language bert-extractive-summarizer
   ```
3. Set up Google Cloud credentials:
   - Create a Google Cloud project
   - Enable the Cloud Translation API, Cloud Text-to-Speech API, and Cloud Natural Language API
   - Create a service account and download the JSON key
   - Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to the path of your JSON key file

## Usage

Start the Flask application:
```
python model.py
```
The server will start on `http://127.0.0.1:5000/`.

## API Endpoints

### POST /detect_language
Detect the language of a given text.
Request body:
```json
{
  "text": "Hello, world!"
}
```

### POST /detect_languages
Detect languages of multiple texts.
Request body:
```json
{
  "texts": ["Hello, world!", "Bonjour le monde!", "Hola, mundo!"]
}
```

### POST /translate_text
Translate text to a target language.
Request body:
```json
{
  "text": "Hello, world!",
  "target_language": "fr"
}
```

### POST /translate_texts
Translate text to multiple target languages.
Request body:
```json
{
  "text": "Hello, world!",
  "target_languages": ["fr", "es", "de"]
}
```

### POST /detect_language_file
Detect language from an uploaded file.
Send a POST request with a file upload named "file".

### POST /auto_translate
Automatically detect source language and translate to target language.
Request body:
```json
{
  "text": "Hello, world!",
  "target_language": "fr"
}
```

### GET /supported_languages
Get a list of supported languages.

### POST /text_to_speech
Convert text to speech.
Request body:
```json
{
  "text": "Hello, world!",
  "language_code": "en-US"
}
```

### POST /text_summary
Summarize a given text.
Request body:
```json
{
  "text": "Long text to be summarized..."
}
```

### POST /sentiment_analysis
Perform sentiment analysis on a given text.
Request body:
```json
{
  "text": "I love this product! It's amazing!"
}
```

### POST /custom_language_model
Use a custom language model for text classification.
Request body:
```json
{
  "text": "Text to be classified...",
  "model_name": "your-custom-model-name"
}
```

## Error Handling

The API returns appropriate error messages and status codes for invalid inputs or processing errors.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open-source and available under the MIT License.
