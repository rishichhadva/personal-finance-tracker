import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyBMstI80felHHuryt8Xr_ADqoSfwwfEdPU",
  "authDomain": "personal-finance-tracker-rish.firebaseapp.com",
  "databaseURL": "https://personal-finance-tracker-rish-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "personal-finance-tracker-rish",
  "storageBucket": "personal-finance-tracker-rish.firebasestorage.app",
  "messagingSenderId": "306440161735",
  "appId": "1:306440161735:web:ffa5f921ba65b041b871e2"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()
