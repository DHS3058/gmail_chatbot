from flask import Flask, render_template, url_for, redirect, session, abort
from authlib.integrations.flask_client import OAuth
from authlib.common.security import generate_token
from pymongo import MongoClient
import os


app = Flask(__name__)
app.secret_key = os.urandom(12)

oauth = OAuth(app)

# MongoDB connection
client = MongoClient("mongodb+srv://pragya:seKZJa1gUEz5RA9W@cluster0.skaxv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["client"]
users_collection = db["employee_info"]

@app.route('/')
def index():
    user = session.get('user')
    return render_template('index.html')

@app.route('/google/')
def google():

    GOOGLE_CLIENT_ID = '73030624989-ara9pqralvn55ok2et3upob0o841r4mi.apps.googleusercontent.com'
    GOOGLE_CLIENT_SECRET = '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'

    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

    # Redirect to google_auth function
    redirect_uri = url_for('google_auth', _external=True)
    print(redirect_uri)
    session['nonce'] = generate_token()
    return oauth.google.authorize_redirect(redirect_uri, nonce=session['nonce'])

@app.route('/google/auth/')
def google_auth():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token, nonce=session['nonce'])
    session['user'] = user
    print(" Google User ", user)

    # Store user information in MongoDB
    user_data = {
        "email": user["email"],
        "name": user["name"]
    }
    users_collection.update_one({"email": user["email"]}, {"$set": user_data}, upsert=True)

    # return redirect('/protected_area')
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)