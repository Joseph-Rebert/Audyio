from contextlib import closing
from io import BytesIO

import boto3
from flask import Flask, render_template, request, send_file, url_for
import os

app = Flask(__name__)
polly = boto3.client('polly')

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_input = request.form['input']
        try:
            response = polly.synthesize_speech(Text=user_input, OutputFormat='mp3', VoiceId='Joanna')
        except:
            print("ERROR")

        if "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:
                audio_data = BytesIO(stream.read())
                audio_data.seek(0)
                return send_file(audio_data, mimetype='audio/mp3', as_attachment=True, download_name='speech.mp3')
    else:
        return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)