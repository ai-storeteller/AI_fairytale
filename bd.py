import firebase_admin
from firebase_admin import credentials, firestore


path_to_key = "loveaiverce-firebase-adminsdk-ok3a3-d0856cc9f9.json"
cred = credentials.Certificate(path_to_key)
firebase_admin.initialize_app(cred)
db = firestore.client()
collection_name = 'fairytales'


def add_history(settings, history, annotation):
    set_story = settings+number_history(settings)
    doc_ref = db.collection(collection_name).document(set_story)
    doc_ref.set({"id": set_story, "name": history[0],  "annotation": annotation, "history": history[1:]})


def number_history(id_history):
    collection_ref = db.collection('fairytales')
    docs = collection_ref.stream()
    count = 0
    for doc in docs:
        if id_history in doc.id:
            count += 1
    return str(count)
