import speech_recognition as sr
from flask import Flask, jsonify, render_template, request
import os

from levenshtein import get_levenshtein_html
from test.test_levenshtein import test_get_wer_info

# Error messages
RETRIEVE_REF_ERROR = 'Could not retrieve reference sentence. Please try again.'
SR_ERROR = 'No speech detected. Please try again.'
LEVENSHTEIN_ERROR = 'An error occurred while calculating the WER. ' + \
                    'Please try again.'

app = Flask(__name__)


# ====================
def get_best_hypothesis(audio_file: str) -> str:
    """Get Google Web Speech API's best hypothesis transcription of the audio file
    specified."""

    r = sr.Recognizer()

    with sr.AudioFile(audio_file) as source:
        audio_data = r.record(source)
    text = r.recognize_google(audio_data, language='en-GB', show_all=True)
    hypothesis = text['alternative'][0]['transcript']

    return hypothesis


# ====================
@app.route('/')
def index():
    return render_template('index.html')


# ====================
@app.route('/main/')
def main():
    return render_template('main.html')


# ====================
@app.route('/save_audio', methods=['POST'])
def save_audio():

    # Attempt to save sound blob sent from frontend
    try:
        sound_blob = request.data
        with open('upload/audio.wav', 'wb') as f:
            f.write(sound_blob)
        return "SUCCESS"
    except Exception as e:
        print(os.getcwd())
        print(e)
        return "ERR"


# ====================
@app.route('/get_wer', methods=['POST'])
def get_wer():

    # Get reference sentence sent from frontend
    try:
        data = request.get_json(force=True)
        reference = data['reference']
    except Exception as e:
        print(e)
        return {'error': RETRIEVE_REF_ERROR}

    # Get hypothesis sentence from Google Web Speech API
    try:
        hypothesis = get_best_hypothesis('upload/audio.wav')
    except Exception as e:
        print(e)
        return {'error': SR_ERROR}

    # Get WER information to display to user
    try:
        html = get_levenshtein_html(reference, hypothesis)
    except Exception as e:
        print(e)
        return {'error': LEVENSHTEIN_ERROR}
    return jsonify(html)


# ====================
if __name__ == "__main__":
    test_get_wer_info()
    app.run(debug=True)
