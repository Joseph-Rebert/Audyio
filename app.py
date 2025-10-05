from flask_sqlalchemy import SQLAlchemy
import boto3
from flask import Flask, render_template, url_for, session, redirect
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
    new_user = User(
        email='testuser@example.com',
        password_hash='hashed_password_here',
        tier='starter'
    )
    db.session.add(new_user)
    db.session.commit()
    print(f"New user added with ID: {new_user.id}")
    user = session.get('user')
    if user:
        return f'Hello, {user.get("cognito:username", "User")}. <a href="/logout">Logout</a>'
    else:
        return f'Welcome! Please <a href="/login">Login</a>.'

@app.route('/login')
def login():
    # Redirect to Cognito's authorization endpoint
    # redirect_uri = url_for('authorize', _external=True)
    # return oauth.cognito.authorize_redirect(redirect_uri)
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
        return redirect(url_for('home'))

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)