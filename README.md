# 💰 Personal Finance Tracker

A simple, Streamlit-based web app to track your income and expenses. Features Firebase authentication, real-time data storage, and analytics.
You can use it here: https://personal-finance-tracker-project.streamlit.app/
## 🔧 Features

- 🔐 User Authentication (Login/Signup using Firebase)
- ➕ Add, Edit & Delete Transactions
- 📆 Filter Transactions by Month
- 📊 View Transaction Summary with Pie Chart
- 🗑️ Reset All Data
- 🌐 Deployed using Streamlit Cloud

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Backend**: Firebase (Authentication + Realtime Database)
- **Database**: Firebase Realtime Database
- **Charts**: Plotly with Pandas
- **Auth Library**: Pyrebase

## 🚀 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/personal-finance-tracker.git
cd personal-finance-tracker
```
### 2. Install Requirements
```bash
pip install -r requirements.txt
```
### 3. Firebase Configuration

- Go to Firebase Console
- Create a new project
- Enable Email/Password authentication
- Create a Realtime Database
- Get your Firebase config from ```bash Project Settings > Web App```

Create a ```bash firebase_config.py``` file:
```bash
import pyrebase

firebaseConfig = {
    "apiKey": "your_api_key",
    "authDomain": "your_project.firebaseapp.com",
    "databaseURL": "https://your_project.firebaseio.com",
    "projectId": "your_project",
    "storageBucket": "your_project.appspot.com",
    "messagingSenderId": "your_sender_id",
    "appId": "your_app_id"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()
```
### 4. Run the App
```bash
streamlit run app.py
```
