import random
import firebase_admin
from firebase_admin import credentials, firestore


path_to_key = "fairytale-ai-5aa59-firebase-adminsdk-ys8ug-c369a0a224.json"
cred = credentials.Certificate(path_to_key)
firebase_admin.initialize_app(cred)
db = firestore.client()
collection_name = 'fairytales_AI'


def add_history_part1(title_en, title_ru, mood, main_character, place, history_en, history_ru, summary,
                      decisions_en, decisions_ru):
    id_history = random.randint(100000, 999999999999)
    while db.collection(collection_name).document(str(id_history)).get().exists:
        id_history = random.randint(100000, 999999999999)
    doc_ref = db.collection(collection_name).document(str(id_history))
    doc_ref.set({
        "id": id_history,
        "title_en": title_en,
        "title_ru": title_ru,
        "character": main_character,
        "mood": mood,
        "setting": place,
        "history_en": history_en,
        "history_ru": history_ru,
        "summary": summary,
        "decisions_en": decisions_en,
        "decisions_ru": decisions_ru,
    })
    return id_history


def load_history_part1(id_history, num_choice):
    docs = db.collection(collection_name).stream()
    target_doc = {}
    for doc in docs:
        data = doc.to_dict()
        if data['id'] == id_history:
            target_doc = data
            break
    decision = target_doc["decisions_en"][int(num_choice)-1]
    return target_doc["mood"], target_doc["character"], target_doc["setting"], target_doc["summary"], decision


def add_history_part2(id_history, history_en, history_ru):
    doc = db.collection(collection_name).where("id", "==", id_history).get()
    doc_ref = db.collection(collection_name).document(doc[0].id)
    prev_part_en = doc[0].to_dict()["history_en"]
    prev_part_ru = doc[0].to_dict()["history_ru"]
    doc_ref.update({
        "history_en": prev_part_en + history_en,
        "history_ru": prev_part_ru + history_ru
    })
