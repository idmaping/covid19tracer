import pyrebase
config = {
  "apiKey": "AIzaSyDY-TyUDZvhABCe55ditZrVCC1x8d-pMFo",
  "authDomain": "covidtracerpoltekad.firebaseapp.com",
  "projectId": "covidtracerpoltekad",
  "databaseURL" : "",
  "storageBucket": "covidtracerpoltekad.appspot.com",
  "messagingSenderId": "923994986075",
  "appId": "1:923994986075:web:c217b727468faafd08917e",
  "measurementId": "G-5N5GWYGLZB"
}
firebase = pyrebase.initialize_app(config)
storage = firebase.storage()


def publish(path_on_cloud,path_local):
    storage.child(path_on_cloud).put(path_local)

#path_on_cloud = "result/3505181604960002_160496.csv"
#path_local = "hasil.csv"
#storage.child(path_on_cloud).put(path_local)
