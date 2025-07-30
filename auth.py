import pyrebase
from firebase_config import firebase_config

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

def login(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        return user
    except:
        return None

def signup(email, password):
    try:
        auth.create_user_with_email_and_password(email, password)
        return True
    except:
        return False
