
import json
import os

FILE = "memory.json"

def load_memory():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r") as f:
        return json.load(f)

def save_memory(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)

def store_memory(user_id, data):
    db = load_memory()
    db[user_id] = data
    save_memory(db)

def get_memory(user_id):
    db = load_memory()
    return db.get(user_id, None)