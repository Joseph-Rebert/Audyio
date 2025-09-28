from flask import Flask, render_template, request, send_file
from gtts import gTTS
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    print("hello")
    return render_template('index.html', test = "as")

if __name__ == '__main__':
    app.run(debug=True)