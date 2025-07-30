import streamlit as st
import pyrebase

firebaseConfig = {
    "apiKey": st.secrets["API_KEY"],
    "authDomain": st.secrets["AUTH_DOMAIN"],
    "databaseURL": st.secrets["DATABASE_URL"],
    "projectId": st.secrets["PROJECT_ID"],
    "storageBucket": st.secrets["STORAGE_BUCKET"],
    "messagingSenderId": st.secrets["MESSAGING_SENDER_ID"],
    "appId": st.secrets["APP_ID"]
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()
