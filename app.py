import os

from flask import Flask, request, render_template
from dotenv import load_dotenv
# from multiprocessing import freeze_support

from views.audio_to_text import SpeechToText
from views.facebook_text_analysis import facebook_sentiment_analyse
from views.google_sentiment_analysis import SentimentAnalysis
from views.microsoft_azure_face_analysis import AzureFace
from views.pyaudio_audio_analysis import PyAudio
from views.sentiment_loughran import get_sentiment_analysis
from views.video_to_audio import convert
from views.video_to_frame import get_frames
from views.face_plus_plus import get_face_analysis
from views.word_to_text import conver_word_to_text

app = Flask(__name__)

APP_ROOT = os.path.dirname(__file__)
load_dotenv()


@app.route('/')
def hello_world():
    return render_template('index.html', title='Welcome')


@app.route('/video-to-audio')
def video_to_audio_template():
    return render_template('video_to_audio.html')


@app.route('/video-to-audio/perform/', methods=['POST', 'GET'])
def video_to_audio():
    if request.method == 'POST':
        folder = request.form.get('folder')
        output_folder = request.form.get('output_folder')
        return convert(folder, output_folder)


@app.route('/video-to-frame')
def video_to_frame_template():
    return render_template('video_to_frame.html')


@app.route('/video-to-frame/perform', methods=['POST', 'GET'])
def video_to_frame():
    if request.method == 'POST':
        folder = request.form.get('folder')
        output_folder = request.form.get('output_folder')
        get_frames(folder, output_folder)
        return "Done"


@app.route('/audio-to-text')
def audio_to_text_template():
    return render_template('audio_to_text.html')


@app.route('/audio-to-text/perform/', methods=['POST', 'GET'])
def audio_to_text():
    if request.method == 'POST':
        folder = request.form.get('folder')
        output_folder = request.form.get('output_folder')
        speech = SpeechToText()
        speech.get_text(folder, output_folder)
        return "Done"


@app.route('/google-sentiment-analysis')
def sentiment_template():
    return render_template('google_sentiment_analysis.html')


@app.route('/google-sentiment-analysis/perform', methods=['POST', 'GET'])
def google_sentiment_analysis():
    if request.method == 'POST':
        folder = request.form.get('folder')
        output_folder = request.form.get('output_folder')
        sentiment = SentimentAnalysis()
        return sentiment.get_analysis(folder, output_folder)


@app.route('/audio-analysis')
def audio_template():
    return render_template('pyaudio_audio_analysis.html')


@app.route('/audio-analysis/perform', methods=['POST', 'GET'])
def audio_analysis():
    if request.method == 'POST':
        folder = request.form.get('folder')
        output_folder = request.form.get('output_folder')
        pyaudio = PyAudio()
        return pyaudio.get_audio_analysis(folder, output_folder)


@app.route('/loughran-sentiment-analysis')
def sentiment_analysis_loughran_template():
    return render_template('loughran_sentiment_analysis.html')


@app.route('/loughran-sentiment-analysis/perform', methods=['POST', 'GET'])
def sentiment_analysis_loughran():
    if request.method == 'POST':
        folder = request.form.get('folder')
        output_folder = request.form.get('output_folder')
        get_sentiment_analysis(folder, output_folder)
        return "Done"


@app.route('/face-plus-plus')
def face_plus_template():
    return render_template('face_plus_plus.html')


@app.route('/face-plus-plus/perform', methods=['POST', 'GET'])
def face_plus():
    if request.method == 'POST':
        folder = request.form.get('folder')
        output_folder = request.form.get('output_folder')
        get_face_analysis(folder, output_folder)
        return "Done"


@app.route('/facebook-sentiment-analysis')
def facebook_sentiment_template():
    return render_template('facebook_text_analysis.html')


@app.route('/facebook-sentiment-analysis/perform', methods=['POST', 'GET'])
def facebook_sentiment():
    if request.method == 'POST':
        folder = request.form.get('folder')
        output_folder = request.form.get('output_folder')
        labels = request.form.get('labels')
        labels = labels.split(",")
        return facebook_sentiment_analyse(folder, output_folder, labels)


@app.route('/word-to-text/')
def word_to_text_template():
    return render_template('word_to_txt.html')


@app.route('/word-to-text/perform', methods=['POST', 'GET'])
def convert_to_text():
    if request.method == 'POST':
        folder = request.form.get('folder')
        output_folder = request.form.get('output_folder')
        return conver_word_to_text(folder, output_folder)


@app.route('/azure-face')
def azure_face_template():
    return render_template('azure_face.html')


@app.route('/azure-face/perform', methods=["POST"])
def azure_face_analysis():
    if request.method == "POST":
        folder = request.form.get('folder')
        output_folder = request.form.get('output_folder')
        az = AzureFace(input_folder=folder, output_folder=output_folder)
        return az.analyse()

if __name__ == '__main__':
    # freeze_support()
    app.run()
