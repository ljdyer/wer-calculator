import speech_recognition as sr
from levenshtein import get_wer
from flask import Flask, render_template, request


app = Flask(__name__)
app.secret_key = "VatsalParsaniya"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/audio_to_text/')
def audio_to_text():
    return render_template('audio_to_text.html')

@app.route('/audio', methods=['POST'])
def audio():
    r = sr.Recognizer()
    with open('upload/audio.wav', 'wb') as f:
        f.write(request.data)
  
    with sr.AudioFile('upload/audio.wav') as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data, language='en-GB', show_all=True)
        try:
            transcription = text['alternative'][0]['transcript']
            # confidence = text['alternative'][0]['confidence']
            # return_text = f"Google Web Speech API: '{transcription}' ({confidence*100:.2f}%)"
            return_text = transcription
        except:
            return_text = "ERR"
        
    return str(return_text)

@app.route('/wer', methods=['POST'])
def wer():
    if request.method == "POST":

        data = request.get_json(force=True)
        hypothesis = data['hypothesis']
        reference = data['reference']
        html = get_wer(reference, hypothesis)
        # return_lines = [
        #     f"You said: '{reference}'",
        #     f"Google Web Speech API heard: '{hypothesis}'",
        #     f"Number of edits required: {edits}",
        #     f"Word error rate: {wer}%"
        # ]
        return html

if __name__ == "__main__":
    app.run(debug=True)
