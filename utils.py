import json

def load_data():
    with open('storage.json', 'r') as file:
        return json.load(file)

def save_data(data):
    with open('storage.json', 'w') as file:
        json.dump(data, file, indent=4)