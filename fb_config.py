import pyrebase
config = {
  "apiKey": "AIzaSyDY-TyUDZvhABCe55ditZrVCC1x8d-pMFo",
  "authDomain": "covidtracerpoltekad.firebaseapp.com",
  "projectId": "covidtracerpoltekad",
  "storageBucket": "covidtracerpoltekad.appspot.com",
  "messagingSenderId": "923994986075",
  "appId": "1:923994986075:web:c217b727468faafd08917e",
  "measurementId": "G-5N5GWYGLZB"
}
firebase = pyrebase.initialize_app(config)
storage = firebase.storage()