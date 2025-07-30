from firebase_config import auth

def signup(email, password):
    try:
        auth.create_user_with_email_and_password(email, password)
        return True
    except Exception as e:
        print("Signup error:", e)
        return False

def login(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        return user
    except Exception as e:
        print("Login error:", e)
        return None
