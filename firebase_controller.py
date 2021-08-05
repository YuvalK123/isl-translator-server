import pyrebase
import os

config = {
    'apiKey': "AIzaSyC6fSdjqphX6v5aZ8dXRoqdan3uF4jMdFE",
    'authDomain': "islcsproject.firebaseapp.com",
    "databaseURL": '',
    'projectId': "islcsproject",
    'storageBucket': "islcsproject.appspot.com",
    'messagingSenderId': "685169809464",
    'appId': "1:685169809464:web:e853d0ded3b18fae3eeecd",
    'measurementId': "G-P7GSQ5W32C",
    'serviceAccount': 'ServiceAccountKey.json'
}

firebase_storage = pyrebase.initialize_app(config)
storage = firebase_storage.storage()

'''
creating a text file with a single line and uploading it to the firebase server.
used in flask_ngrok2.py to upload the ngrok address to firebase so the users can us it
to log to the server.
'''
def upload_server_address(url: str):
    with open('addr.txt', 'w') as file:
        file.write(url)
    storage.child('addr.txt').put('addr.txt')
    os.remove('addr.txt')

'''
simplefy firebase download function
'''
def download(firebase_path: str, local_name: str):
    storage.child(firebase_path).download(firebase_path, local_name)

'''
simplefy firebase download function
'''
def upload(firebase_path: str, local_name: str):
    storage.child(firebase_path).put(local_name)