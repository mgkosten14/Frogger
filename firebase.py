"""Firebase highscore tracker"""
# pylint: disable=broad-exception-caught
from firebase_admin import initialize_app, credentials, firestore

def firebase_access(service_account_key_path):
    """Initialize the Firebase Admin SDK"""
    try:
        cred = credentials.Certificate(service_account_key_path)
        app = initialize_app(cred)
        db = firestore.client(app)
        db.collection("scores")
        return db
    except Exception as e:
        print(f"Error initializing Firebase: {e}")
        return None

def add_entry(db, score, username = "null"):
    """Add record to database"""
    try:
        scores_ref = db.collection("scores")
        scores_ref.add({"score": score, "username" : username})
    except Exception as e:
        print(f"Error adding user / score: {e}")

def get_top_five(db):
    """Get top five highscores"""
    scores_dict = {}
    scores_ref = db.collection("scores")
    query = scores_ref.order_by("score").limit_to_last(5)
    docs = query.get()
    for doc in docs:
        scores_dict[doc.id] = doc.to_dict()
    return scores_dict
