import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

path_to_key = "loveaiverce-firebase-adminsdk-ok3a3-c317ab3ab4.json"
cred = credentials.Certificate(path_to_key)
firebase_admin.initialize_app(cred)
db = firestore.client()
collection_name = 'fairytales_ALL'


df = pd.read_excel("fairytale_rus.xlsx")

name, id, tag, annotation, reading_time, fairytale = (df.loc[0, 'name'], int(df.loc[0, 'id']), df.loc[0, 'tag'],
                                                      df.loc[0, 'annotation'], df.loc[0, 'reading time'], [])
for index, row in df.iterrows():
    fairytale.append(row["fairytale"])
if reading_time == ' ':
    reading_time = ""
print(reading_time)
data = {"name": name, "id": id, "tag": tag, "annotation": annotation, "reading_time": reading_time,
        "fairytale": fairytale, "mood": "magic", "character": "boy", "place": "space"}
print(name)
new_doc_ref = db.collection(collection_name).add(data)
