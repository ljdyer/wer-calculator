# Third-party libraries
from flask import Flask, render_template, request, jsonify

# Project modules
from levenshtein.levenshtein import get_levenshtein_html
from levenshtein.test_levenshtein import test_get_wer_info
from app_helper import *

# Error messages
RETRIEVE_REF_ERROR = 'Could not retrieve reference sentence. Please try again'
SR_ERROR = 'No speech detected. Please try again'
LEVENSHTEIN_ERROR = 'An error occurred while calculating the WER. Please try again'


app = Flask(__name__)

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
    except:
        return "ERR"
  
    
# ====================
@app.route('/get_wer', methods=['POST'])
def get_wer():
    # Get reference sentence sent from frontend
    try:
        data = request.get_json(force=True)
        reference = data['reference']
    except:
        return {'error': RETRIEVE_REF_ERROR}

    # Get hypothesis sentence from Google Web Speech API
    try:
        hypothesis = get_best_hypothesis('upload/audio.wav')
    except:
        return {'error': SR_ERROR}
        
    # Get WER information to display to user
    try:
        html = get_levenshtein_html(reference, hypothesis)
    except:
        return {'error': LEVENSHTEIN_ERROR}
    return jsonify(html)
    

# ====================
if __name__ == "__main__":
    test_get_wer_info()
    app.run(debug=True)