from flask import Flask, request, jsonify
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
from google.cloud import translate_v2 as translate
from google.cloud import texttospeech
from google.cloud import language_v1
import os
from summarizer import Summarizer

DetectorFactory.seed = 0

app = Flask(__name__)

translate_client = translate.Client()
tts_client = texttospeech.TextToSpeechClient()
language_client = language_v1.LanguageServiceClient()
summarizer = Summarizer()

@app.route('/detect_language', methods=['POST'])
def detect_language():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Invalid input, "text" is required'}), 400
    
    text = data['text']
    try:
        language = detect(text)
        return jsonify({'language': language})
    except LangDetectException as e:
        return jsonify({'error': str(e)}), 500

@app.route('/detect_languages', methods=['POST'])
def detect_languages():
    data = request.get_json()
    if not data or 'texts' not in data:
        return jsonify({'error': 'Invalid input, "texts" is required'}), 400
    
    texts = data['texts']
    results = {}
    
    for text in texts:
        try:
            language = detect(text)
            results[text] = language
        except LangDetectException as e:
            results[text] = {'error': str(e)}
    
    return jsonify(results)

@app.route('/translate_text', methods=['POST'])
def translate_text():
    data = request.get_json()
    if not data or 'text' not in data or 'target_language' not in data:
        return jsonify({'error': 'Invalid input, "text" and "target_language" are required'}), 400
    
    text = data['text']
    target_language = data['target_language']
    
    try:
        translation = translate_client.translate(text, target_language=target_language)
        return jsonify({'translated_text': translation['translatedText']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/translate_texts', methods=['POST'])
def translate_texts():
    data = request.get_json()
    if not data or 'text' not in data or 'target_languages' not in data:
        return jsonify({'error': 'Invalid input, "text" and "target_languages" are required'}), 400
    
    text = data['text']
    target_languages = data['target_languages']
    translations = {}
    
    for lang in target_languages:
        try:
            translation = translate_client.translate(text, target_language=lang)
            translations[lang] = translation['translatedText']
        except Exception as e:
            translations[lang] = {'error': str(e)}
    
    return jsonify(translations)

@app.route('/detect_language_file', methods=['POST'])
def detect_language_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    text = file.read().decode('utf-8')
    
    try:
        language = detect(text)
        return jsonify({'language': language})
    except LangDetectException as e:
        return jsonify({'error': str(e)}), 500

@app.route('/auto_translate', methods=['POST'])
def auto_translate():
    data = request.get_json()
    if not data or 'text' not in data or 'target_language' not in data:
        return jsonify({'error': 'Invalid input, "text" and "target_language" are required'}), 400
    
    text = data['text']
    target_language = data['target_language']
    
    try:
        detected_language = detect(text)
        if detected_language == target_language:
            return jsonify({'translated_text': text})
        
        translation = translate_client.translate(text, target_language=target_language)
        return jsonify({
            'detected_language': detected_language,
            'translated_text': translation['translatedText']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/supported_languages', methods=['GET'])
def supported_languages():
    languages = translate_client.get_languages()
    return jsonify({'languages': languages})

@app.route('/text_to_speech', methods=['POST'])
def text_to_speech():
    data = request.get_json()
    if not data or 'text' not in data or 'language_code' not in data:
        return jsonify({'error': 'Invalid input, "text" and "language_code" are required'}), 400
    
    text = data['text']
    language_code = data['language_code']
    
    try:
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        
        response = tts_client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        
        return jsonify({'audio_content': response.audio_content.decode('utf-8')})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/text_summary', methods=['POST'])
def text_summary():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Invalid input, "text" is required'}), 400
    
    text = data['text']
    
    try:
        summary = summarizer(text)
        return jsonify({'summary': summary})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/sentiment_analysis', methods=['POST'])
def sentiment_analysis():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Invalid input, "text" is required'}), 400
    
    text = data['text']
    
    try:
        document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
        sentiment = language_client.analyze_sentiment(request={'document': document}).document_sentiment
        
        return jsonify({
            'score': sentiment.score,
            'magnitude': sentiment.magnitude
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/custom_language_model', methods=['POST'])
def custom_language_model():
    data = request.get_json()
    if not data or 'text' not in data or 'model_name' not in data:
        return jsonify({'error': 'Invalid input, "text" and "model_name" are required'}), 400
    
    text = data['text']
    model_name = data['model_name']
    
    try:
        document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
        response = language_client.classify_text(request={
            'document': document,
            'classifier_id': model_name
        })
        
        categories = [
            {'name': category.name, 'confidence': category.confidence}
            for category in response.categories
        ]
        
        return jsonify({'categories': categories})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)