import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyDbVxnX-JyM6LrfZn2Sj_IEZRC1GYuP-sk",
    "authDomain": "personal-finance-tracker-rishi.firebaseapp.com",
    "projectId": "personal-finance-tracker-rishi",
    "storageBucket": "personal-finance-tracker-rishi.appspot.com",
    "messagingSenderId": "815652739645",
    "appId": "1:815652739645:web:1d35eaac56dd0577dae854",
    "measurementId": "G-7H1Y6B8F0V",
    "databaseURL": "https://personal-finance-tracker-rishi-default-rtdb.firebaseio.com"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

def signup(email, password):
    try:
        auth.create_user_with_email_and_password(email, password)
        return True
    except:
        return False

def login(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        return user
    except:
        return None
