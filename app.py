from flask import Flask, render_template, request, send_file
from gtts import gTTS
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/account', methods=['GET', 'POST'])
def account():
    return render_template('account.html')

if __name__ == '__main__':
    app.run(debug=True)