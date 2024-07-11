from Server import server

from flask import Flask, request, jsonify
from datetime import datetime
from pymongo import MongoClient

import requests

client = MongoClient('mongodb://localhost:27017/')
db = client['SmartDrive']
collection_user = db['user']


#@server.route('/user/new_user', methods=['POST'])
def newUser():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['SmartDrive']
    collection_user = db['user']

    # Estrarre il nome dalla richiesta API
    name = request.json.get('name')
    surname = request.json.get('surname')
    mail = request.json.get('mail')

    # Ottenere la data e ora attuale
    current_time = datetime.now()

    # Creare il documento da inserire nel database
    session_data = {
        'name': name,
        'surname': surname,
        'mail': mail,
        'created_at': current_time,
        'updated_at': current_time
    }

    # Inserire il documento nella collezione 'session'
    result = collection_user.insert_one(session_data)

    # Verificare se l'inserimento è avvenuto con successo
    if result.inserted_id:
        # Restituire solo l'ID della sessione creata
        return str(result.inserted_id), 201
    else:
        return '', 500




