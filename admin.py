"""Firebase admin file to setup firestore"""
import os
import sys
from firebase_admin import firestore

from firebase import firebase_access

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Need admin and json file")
        sys.exit(1)

    json_file_path = sys.argv[1]
    if not os.path.exists(json_file_path):
        print("File Not Found :/")
        sys.exit(1)

    #set up firebase
    script_dir = os.path.dirname(__file__)
    credentials_path = os.path.join(script_dir, "credentials.json")

    db = firebase_access(credentials_path)
    db = firestore.client()
