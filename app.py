from flask import Flask, render_template, request, send_file, url_for
from gtts import gTTS
import os

from werkzeug.utils import redirect

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/<user>', methods=['GET', 'POST'])
def user(user):
    return f"<h1> {user} </h1>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
            username = request.form['username']
            return redirect(url_for('user', user=username))
    else:
        return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)