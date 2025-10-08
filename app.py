from contextlib import closing
from io import BytesIO

from flask_sqlalchemy import SQLAlchemy
import boto3
from flask import Flask, render_template, url_for, session, redirect, request, send_file
from authlib.integrations.flask_client import OAuth
import os
from models.user import User, db

app = Flask(__name__)
polly = boto3.client('polly')
app.secret_key = os.urandom(24)

# Change 'tts-db-1' to your actual database name (e.g., 'postgres' or another existing db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://wibert:Wibert5477!@database-1.cru0g8qc6xkt.us-east-2.rds.amazonaws.com:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

oauth = OAuth(app)

# Configure Cognito OAuth
oauth.register(
  name='oidc',
  authority='https://cognito-idp.us-east-2.amazonaws.com/us-east-2_znDYdNNxu',
  client_id='64r5e5qqfmutvtqv83gpv8rq95',
  client_secret='5llocedslr8qpnihrvq2tb58ik5v9ckq7c4oaqt97esuvo3k1pv',
  server_metadata_url='https://cognito-idp.us-east-2.amazonaws.com/us-east-2_znDYdNNxu/.well-known/openid-configuration',
  client_kwargs={'scope': 'email openid phone'}
)

@app.route('/', methods=['GET', 'POST'])
def home():
    user = session.get('user')
    input_text = request.form.get('input_text')
    if input_text:
        try:
            response = polly.synthesize_speech(
            OutputFormat='mp3',
            Text=input_text,
            VoiceId='Joanna')
        except:
            print("Error in synthesize speech")

        if "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:
                audio_data = BytesIO(stream.read())
                audio_data.seek(0)
                return send_file(audio_data, mimetype='audio/mp3', as_attachment=True, download_name='speech.mp3')

    return render_template('index.html', user=user)

@app.route('/login')
def login():
    return oauth.oidc.authorize_redirect('http://localhost:5000/authorize')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route('/authorize')
def authorize():
        token = oauth.oidc.authorize_access_token()
        user = token['userinfo']
        session['user'] = user
        attempt_add_user_to_database(user['email'], user['cognito:username'], 'starter')
        return redirect(url_for('home'))

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')


def attempt_add_user_to_database(email, username, tier):
    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    
    if existing_user:
        print(f"User with email {email} already exists with ID: {existing_user.id}")
        return existing_user
    
    # User doesn't exist, create new one
    user = User(email=email, username=username, tier=tier)
    db.session.add(user)
    db.session.commit()
    print(f"New user added with ID: {user.id}")
    return user

if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)