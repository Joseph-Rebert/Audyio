from contextlib import closing
from io import BytesIO

import stripe
from dotenv import load_dotenv, find_dotenv
from flask_sqlalchemy import SQLAlchemy
import boto3
from flask import Flask, render_template, url_for, session, redirect, request, send_file, jsonify
from authlib.integrations.flask_client import OAuth
import os
from models.user import User, db

local_env = True

STARTER_TIER = 220000

application = Flask(__name__)
polly = boto3.client('polly', region_name='us-east-2')
application.secret_key = os.urandom(24)
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
application.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQL_URL')
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

stripe.api_key = os.getenv('STRIPE_SECRET')
db.init_app(application)

oauth = OAuth(application)

oauth.register(
    name='oidc',
    authority='https://cognito-idp.us-east-2.amazonaws.com/us-east-2_znDYdNNxu',
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    server_metadata_url='https://cognito-idp.us-east-2.amazonaws.com/us-east-2_znDYdNNxu/.well-known/openid-configuration',
    client_kwargs={'scope': 'email openid phone'}
)


@application.route('/', methods=['GET', 'POST'])
def home():
    user = session.get('user')
    user_tier = session.get('user_tier')
    input_text = request.form.get('input_text')

    if input_text:
        can_use_tts = update_users_word_count(user['email'], len(input_text.split()))
        response = None
        try:
            if can_use_tts:
                response = polly.synthesize_speech(
                    OutputFormat='mp3',
                    Text=input_text,
                    VoiceId='Joanna')
            else:
                response = None
                return "Cant use tts no more words left"
        except:
            print("Error in synthesize speech")
            return "Error in synthesize speech"

        print(response)
        if response is not None and "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:
                audio_data = BytesIO(stream.read())
                audio_data.seek(0)
                return send_file(audio_data, mimetype='audio/mp3', as_attachment=True, download_name='speech.mp3')
        else:
            return "Error in synthesize speech 2"

    return render_template('index.html', user=user, user_tier=user_tier)


@application.route('/login')
def login():
    redirect_uri = request.host_url.rstrip('/') + '/authorize'
    return oauth.oidc.authorize_redirect(redirect_uri)


@application.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('user_tier', None)
    return redirect(url_for('home'))


@application.route('/authorize')
def authorize():
    token = oauth.oidc.authorize_access_token()
    user = token['userinfo']
    session['user'] = user
    db_user = attempt_add_user_to_database(user['email'], user['cognito:username'], 'starter')
    session['user_tier'] = db_user.tier
    return redirect(url_for('home'))


@application.route('/pricing')
def pricing():
    user = session.get('user')
    user_tier = session.get('user_tier')
    return render_template('pricing.html', user=user, user_tier=user_tier)


def attempt_add_user_to_database(email, username, tier):
    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        print(f"User with email {email} already exists with ID: {existing_user.id}")
        return existing_user

    user = User(email=email, username=username, tier=tier)
    db.session.add(user)
    db.session.commit()
    print(f"New user added with ID: {user.id}")
    return user


def update_users_word_count(email, words_used):
    try:
        # Find the user by email
        user = User.query.filter_by(email=email).first()

        if user:
            if user.words_used + words_used <= STARTER_TIER:
                user.words_used += words_used
                db.session.commit()
                print(f"Updated word count for {email}: +{words_used} words (Total: {user.words_used})")
                return True
            else:
                print(f"Unable to use service for {email}: Words exceed cap (Total: {user.words_used})")
                return False
        else:
            print(f"User with email {email} not found")
            return False
    except Exception as e:
        print(f"Error updating word count: {e}")
        db.session.rollback()
        return False


@application.route('/create_checkout_session', methods=['GET'])
def create_checkout_session():
    if local_env:
        session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price": "price_1SKISxPbLAL4Mjp0LYQBhsjX",
                    "quantity": 1
                }
            ],
            mode='subscription',
            success_url='http://localhost:5000/success',  # need to change on live servers
            cancel_url='http://localhost:5000/cancel',  # need to change on live servers
            automatic_tax={'enabled': True}
        )
    else:
        session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price": "price_1SKISxPbLAL4Mjp0LYQBhsjX",
                    "quantity": 1
                }
            ],
            mode='subscription',
            success_url='https://audyio.com/success',  # need to change on live servers
            cancel_url='https://audyio.com/cancel',  # need to change on live servers
            automatic_tax={'enabled': True}
        )

    return redirect(session.url, code=303)


@application.route('/success')
def success():
    return 'Your subscription has been activated!'


if __name__ == '__main__':
    if local_env:
        application.run(host="localhost", port=5000, debug=True)
    else:
        application.run(debug=True)
