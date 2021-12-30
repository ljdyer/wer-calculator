import speech_recognition as sr

def get_best_hypothesis(audio_file: str) -> str:
    """Get Google Web Speech API's best hypothesis transcription of the audio file
    specified."""

    r = sr.Recognizer()

    with sr.AudioFile(audio_file) as source:
        audio_data = r.record(source)
    text = r.recognize_google(audio_data, language='en-GB', show_all=True)
    hypothesis = text['alternative'][0]['transcript']
    
    return hypothesis