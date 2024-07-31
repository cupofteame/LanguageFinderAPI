# Language Detection and Translation API

This Flask-based API provides language detection and translation services using Google Cloud Translate and the langdetect library.

## Features

- Detect language of a given text
- Detect languages of multiple texts
- Translate text to a target language
- Translate text to multiple target languages
- Detect language from uploaded file
- Auto-translate text (detect source language and translate to target)
- Get list of supported languages

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install flask langdetect google-cloud-translate
   ```
3. Set up Google Cloud credentials:
   - Create a Google Cloud project
   - Enable the Cloud Translation API
   - Create a service account and download the JSON key
   - Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to the path of your JSON key file

## Usage

Start the Flask application:

```
python app.py
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

## Error Handling

The API returns appropriate error messages and status codes for invalid inputs or processing errors.

## Future Features

The following features are planned for future implementation:

- Text-to-speech conversion
- Text summarization
- Sentiment analysis
- Custom language model integration

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

##
Anyone can use this!