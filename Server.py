import math
import dash
import time
from dash.dependencies import Output, Input
from dash import dcc, html
from datetime import datetime, timedelta
import json
import plotly.graph_objs as go
from collections import deque
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from bson import ObjectId  # For handling MongoDB IDs
from pymongo import MongoClient
import numpy as np
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
import TestDrive
import Service
import jwt
from functools import wraps

server = Flask(__name__)
server.config['SECRET_KEY'] = 'supersecretkey'  # Chiave segreta per JWT
CORS(server, resources={r"/*": {"origins": "*"}})  # Enable CORS

app = dash.Dash(__name__, server=server)

# Configure Flask-Limiter
limiter = Limiter(
    get_remote_address,
    app=server,
    default_limits=["2 per second"]  # Limit to 2 requests per second
)

MAX_DATA_POINTS = 1000
UPDATE_FREQ_MS = 100

times = deque(maxlen=MAX_DATA_POINTS)
accel_x = deque(maxlen=MAX_DATA_POINTS)
accel_y = deque(maxlen=MAX_DATA_POINTS)
accel_z = deque(maxlen=MAX_DATA_POINTS)
gyro_x = deque(maxlen=MAX_DATA_POINTS)
gyro_y = deque(maxlen=MAX_DATA_POINTS)
gyro_z = deque(maxlen=MAX_DATA_POINTS)
latitude = deque(maxlen=MAX_DATA_POINTS)
longitude = deque(maxlen=MAX_DATA_POINTS)

app.layout = html.Div(
    [
        dcc.Markdown(
            children="""
            # Live Sensor Readings
            Streamed from Sensor Logger: tszheichoi.com/sensorlogger
        """
        ),
        dcc.Graph(id="live_graph"),
        dcc.Interval(id="counter", interval=UPDATE_FREQ_MS),
    ]
)


client = MongoClient('mongodb://localhost:27017/')
db = client['SmartDrive']
collection_sensor = db['samples']
collection_session = db['session']
collection_user = db['user']


#jwt_token = JWTManager(server)

# Funzione per verificare il token JWT
# Funzione per verificare il token JWT
def verify_token(token):
    try:
        payload = jwt.decode(token, server.config['SECRET_KEY'], algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token scaduto
    except jwt.InvalidTokenError:
        return None  # Token non valido

# Decoratore per verificare l'autenticazione
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token mancante!'}), 401

        token = token.split(" ")[1]  # Formato del token "Bearer <token>"
        payload = verify_token(token)

        if not payload:
            return jsonify({'message': 'Token non valido o scaduto!'}), 401

        # Aggiungi il payload decodificato alla richiesta per utilizzarlo nel resto della funzione
        request.current_user = payload
        return f(*args, **kwargs)

    return decorated

@app.callback(Output("live_graph", "figure"), Input("counter", "n_intervals"))
def update_graph(_counter):
    data = [
        go.Scatter(x=list(time), y=list(d), name=name)
        for d, name in zip(
            [accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z],
            ["Accel X", "Accel Y", "Accel Z", "Gyro X", "Gyro Y", "Gyro Z"]
        )
    ]

    graph = {
        "data": data,
        "layout": go.Layout(
            {
                "xaxis": {"type": "date"},
                "yaxis": {"title": "Acceleration and Gyro readings"},
            }
        ),
    }
    if len(time) > 0:  # cannot adjust plot ranges until there is at least one data point
        graph["layout"]["xaxis"]["range"] = [min(time), max(time)]
        graph["layout"]["yaxis"]["range"] = [
            min(accel_x + accel_y + accel_z + gyro_x + gyro_y + gyro_z),
            max(accel_x + accel_y + accel_z + gyro_x + gyro_y + gyro_z),
        ]

    return graph


accelerometer_x = 0
accelerometer_y = 0
accelerometer_z = 0
gyroscope_x = 0
gyroscope_y = 0
gyroscope_z = 0
longitude = 0
latitude = 0
speed = 0

free = True

def convert_numpy_int64_to_int(doc):
    """ Convert numpy.int64 to int in a given dictionary """
    for key, value in doc.items():
        if isinstance(value, np.int64):
            doc[key] = int(value)
    return doc

@server.route("/data", methods=["POST"])
def new_data():  # listens to the data streamed from the sensor logger

    session_response, session_status_code = get_active_session()

    global longitude, latitude, speed, free, accelerometer_x, accelerometer_y, accelerometer_z, gyroscope_x, gyroscope_y, gyroscope_z

    if session_status_code == 200:
        # Se c'è una sola sessione attiva, continua con il metodo
        active_session = session_response.json
        session_id = active_session['_id']
        # Continua con il resto del metodo usando session_id
        print(f"Session ID: {session_id}")
        # Inserisci qui il resto della tua logica

        if str(request.method) == "POST":
            #print(f'received data: {request.data}')
            data = json.loads(request.data)
            for d in data['payload']:
                ts = datetime.fromtimestamp(d["time"] / 1000000000)
                if len(times) == 0 or ts > times[-1]:
                    times.append(ts)


                    # Iteriamo attraverso gli elementi di payload per cercare le informazioni desiderate
                    for item in data['payload']:
                        if 'longitude' in item['values'] and 'latitude' in item['values'] and 'speed' in item['values']:
                            longitude = item['values']['longitude']
                            latitude = item['values']['latitude']
                            speed = item['values']['speed']
                            break  # Terminiamo il loop una volta trovati i valori desiderati
                        if item['name'] == 'accelerometer' and 'values' in item and 'x' in item['values']:
                            accelerometer_x = item['values']['x']
                            accelerometer_y = item['values']['y']
                            accelerometer_z = item['values']['z']
                        elif item['name'] == 'gyroscope' and 'values' in item and 'x' in item['values']:
                            gyroscope_x = item['values']['x']
                            gyroscope_y = item['values']['y']
                            gyroscope_z = item['values']['z']

                    if latitude != 0 and longitude != 0 and free == True:
                        free = False

                        doc = {"time": ts}

                        # if d.get("name", None) == "accelerometer":
                        #     accel_x.append(d["accelerometer"]["values"]["x"])
                        #     accel_y.append(d["accelerometer"]["values"]["y"])
                        #     accel_z.append(d["accelerometer"]["values"]["z"])
                        # if d.get("name", None) == "gyroscope":
                        #     gyro_x.append(d["gyroscope"]["values"]["x"])
                        #     gyro_y.append(d["gyroscope"]["values"]["y"])
                        #     gyro_z.append(d["gyroscope"]["values"]["z"])
                        #
                        # ac_x = d["accelerometer"]["values"]["x"]
                        # ac_y = d["accelerometer"]["values"]["y"]
                        # ac_z = d["accelerometer"]["values"]["z"]
                        ac_tot = math.sqrt(accelerometer_x**2 + accelerometer_y**2 + accelerometer_z**2)

                        style = TestDrive.calculateStyle(ac_tot, speed)

                        print(session_id)
                        print(accelerometer_x)
                        print(accelerometer_y)
                        print(accelerometer_z)
                        print(ac_tot)
                        print(latitude)
                        print(longitude)
                        print(speed)
                        print(style)

                        time.sleep(1)


                        roll, pitch = Service.madgwick_filter(accelerometer_x, accelerometer_z, accelerometer_z, gyroscope_x, gyroscope_y, gyroscope_z, 1)

                        doc.update({
                            "session_id": session_id,
                            "accel_x": accelerometer_x,
                            "accel_y": accelerometer_y,
                            "accel_z": accelerometer_z,
                            "total_acceleration": ac_tot,
                            "gyro_x": gyroscope_x,
                            "gyro_y": gyroscope_y,
                            "gyro_z": gyroscope_z,
                            "latitude": latitude,
                            "longitude": longitude,
                            "speed": speed,
                            "style": style,
                            "roll": roll,
                            "pitch": pitch,
                            "created_at": datetime.now(),
                            "updated_at": datetime.now()
                        })


                        # Convert numpy.int64 to int in doc before insertion
                        doc = convert_numpy_int64_to_int(doc)
                        collection_sensor.insert_one(doc)

                        #aggiorno la session con i dati relativi alla posizione dell'ultima acquisizione
                        session_object_id = ObjectId(session_id)
                        collection_session.find_one_and_update(
                             {"_id": session_object_id},
                             {"$set": {
                                 "latitude": latitude,
                                 "longitude": longitude,
                                 "updated_at": datetime.now()
                             }})

                        free = True

    else:
        # Se non ci sono sessioni attive o ci sono più di una, esci dall'if
        print(f"Errore: {session_response.json['message'] if 'message' in session_response.json else session_response.json['error']}")

    return "success"


# verifica che ci sia una sessione attiva e ritorna il suo id
@server.route("/session/get_active", methods=["GET"])
def get_active_session():
    try:
        # Trova tutte le sessioni con status 1
        active_sessions = list(collection_session.find({"status": 1}))

        if len(active_sessions) == 1:
            # Se esiste una sola sessione attiva, restituisci il suo ID
            active_session = active_sessions[0]
            active_session['_id'] = str(active_session['_id'])  # Converti ObjectId in stringa per la serializzazione JSON
            return jsonify(active_session), 200
        elif len(active_sessions) == 0:
            # Se non ci sono sessioni attive
            return jsonify({"message": "No active sessions found"}), 404
        else:
            # Se ci sono più di una sessione attiva
            return jsonify({"error": "Multiple active sessions found"}), 409

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# chiamata api per creare una nuova sessione
@server.route("/session/new_session", methods=["POST"])
def newSession():
    # Estrarre il nome dalla richiesta API
    name = request.json.get('name')
    status = request.json.get('status')

    # Ottenere la data e ora attuale
    current_time = datetime.now()

    # Creare il documento da inserire nel database
    session_data = {
        'name': name,
        'longitude': '',  # Lasciato vuoto per ora
        'latitude': '',  # Lasciato vuoto per ora
        'status': status,
        'style_average': None,
        'created_at': current_time,
        'updated_at': current_time
    }

    # Inserire il documento nella collezione 'session'
    result = collection_session.insert_one(session_data)

    # Verificare se l'inserimento è avvenuto con successo
    if result.inserted_id:
        # Restituire solo l'ID della sessione creata
        return str(result.inserted_id), 201
    else:
        return '', 500

# find by id
@server.route("/session/<session_id>", methods=["GET"])
def getSession(session_id):
    try:
        # Convertire session_id in ObjectId (necessario per la query)
        session_object_id = ObjectId(session_id)

        # Trovare la sessione con l'ID specificato
        session = collection_session.find_one({'_id': session_object_id})

        if session:
            # Convertire l'ObjectId in una stringa per la serializzazione JSON
            session['_id'] = str(session['_id'])
            # Se la sessione è trovata, restituire il documento come JSON
            return jsonify(session), 200
        else:
            # Se la sessione non è trovata, restituire un messaggio di errore
            return jsonify({'message': 'Sessione non trovata'}), 404

    except Exception as e:
        # Gestire eventuali eccezioni durante il recupero della sessione
        return jsonify({'message': str(e)}), 500


# find all
@server.route("/session/find_all", methods=["GET"])
def getAllSessions():
    try:
        # Trovare tutte le sessioni nella collezione
        sessions = list(collection_session.find())

        # Convertire gli ObjectId in stringhe per la serializzazione JSON
        for session in sessions:
            session['_id'] = str(session['_id'])

        # Restituire tutte le sessioni come JSON
        return jsonify(sessions), 200

    except Exception as e:
        # Gestire eventuali eccezioni durante il recupero delle sessioni
        return jsonify({'message': str(e)}), 500


# tramite questo metodo possiamo attivare una sessione e prepararla alla raccolta dei dati
@server.route("/session/activate/<id>", methods=["PATCH"])
def startSession(id):
    try:
        # Verifica se l'ID è un ObjectId valido
        if not ObjectId.is_valid(id):
            return jsonify({"error": "Invalid ObjectId format"}), 400

        # Converti l'ID in ObjectId
        object_id = ObjectId(id)

        # Controlla se esiste già un'istanza con status 1
        existing_active_instance = collection_session.find_one({"status": 1})
        if existing_active_instance:
            print("An instance with status 1 already exists.")
            return jsonify({"error": "An instance with status 1 already exists"}), 409

        # Trova l'oggetto con l'ID specificato e stampa il risultato prima dell'aggiornamento
        current_object = collection_session.find_one({"_id": object_id})
        if not current_object:
            print(f"Object with id {id} not found.")
            return jsonify({"error": "Object not found"}), 404

        # Aggiorna lo status a 1 e il campo updated_at
        result = collection_session.find_one_and_update(
            {"_id": object_id},
            {"$set": {
                "status": 1,
                "updated_at": datetime.now()
            }},
            return_document=True
        )

        if result:
            # Restituisci l'oggetto aggiornato
            result['_id'] = str(result['_id'])  # Converte ObjectId in stringa per la serializzazione JSON
            return jsonify(result), 200
        else:
            print(f"Failed to update object with id {id}.")
            return jsonify({"error": "Failed to update object"}), 500

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@server.route("/session/deactivate/<id>", methods=["PATCH"])
def end_session(id):
    try:
        # Verifica se l'ID è un ObjectId valido
        if not ObjectId.is_valid(id):
            return jsonify({"error": "Invalid ObjectId format"}), 400

        # Converti l'ID in ObjectId
        object_id = ObjectId(id)

        # Trova l'oggetto con l'ID specificato
        current_object = collection_session.find_one({"_id": object_id})
        if not current_object:
            print(f"Object with id {id} not found.")
            return jsonify({"error": "Object not found"}), 404

        # Aggiorna lo status a 2 e il campo updated_at
        result = collection_session.find_one_and_update(
            {"_id": object_id},
            {"$set": {
                "status": 2,
                "updated_at": datetime.now()
            }},
            return_document=True
        )

        if result:
            # Restituisci l'oggetto aggiornato
            result['_id'] = str(result['_id'])  # Converte ObjectId in stringa per la serializzazione JSON
            return jsonify(result), 200
        else:
            print(f"Failed to update object with id {id}.")
            return jsonify({"error": "Failed to update object"}), 500

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


# calcolo lo stile medio dei campioni associati alla stessa sessione
@server.route('/session/style_average/<session_id>', methods=['PATCH'])
def calculate_style_average(session_id):
    # Trova la sessione corrispondente all'ID
    session = collection_session.find_one({'_id': ObjectId(session_id)})
    if not session:
        return jsonify({'error': 'Session not found'}), 404

    # Trova tutti i documenti di samples con lo stesso session_id
    samples = collection_sensor.find({'session_id': session_id})

    total_style_sum = 0
    count = 0

    # Calcola la somma dei valori di style
    for sample in samples:
        total_style_sum += sample['style']
        count += 1

    if count == 0:
        return jsonify({'error': 'No samples found for the session'}), 404

    # Calcola la media arrotondando all'intero più vicino
    style_average = round(total_style_sum / count)

    object_id = ObjectId(session_id)

    # Aggiorna lo status a 2 e il campo updated_at
    result = collection_session.find_one_and_update(
        {"_id": object_id},
        {"$set": {
            "style_average": style_average,
            "updated_at": datetime.now()
        }},
        return_document=True
    )

    if result:
        # Restituisci l'oggetto aggiornato
        result['_id'] = str(result['_id'])  # Converte ObjectId in stringa per la serializzazione JSON
        return jsonify(result), 200
    else:
        print(f"Failed to update object with id {id}.")
        return jsonify({"error": "Failed to update object"}), 500


@server.route('/session/delete/<id>', methods=['DELETE'])
def delete_session(id):
    try:
        # Verifica se l'ID è un ObjectId valido
        if not ObjectId.is_valid(id):
            return jsonify({"error": "Invalid ObjectId format"}), 400

        # Converti l'ID in ObjectId
        object_id = ObjectId(id)

        # Trova e elimina l'oggetto con l'ID specificato
        result = collection_session.delete_one({"_id": object_id})

        if result.deleted_count > 0:
            return jsonify({"message": f"Session with id {id} deleted successfully"}), 200
        else:
            return jsonify({"error": "Session not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# permette di cercare i campioni associati a una sessione
@server.route('/samples/find_by_session/<session_id>', methods=['GET'])
def get_samples_by_id_session(session_id):
    # Esegui la query per estrarre tutti i campioni con lo stesso session_id
    results = collection_sensor.find({"session_id": session_id})

    # Converti i risultati in una lista di dizionari
    samples = [sample for sample in results]
    for sample in samples:
        sample["_id"] = str(sample["_id"])  # Converti ObjectId in stringa

    return jsonify(samples)

# find all per i campioni
@server.route('/samples/find_all', methods=['GET'])
@token_required
def get_all_samples():
    # Esegui la query per estrarre tutti i campioni
    results = collection_sensor.find()

    # Converti i risultati in una lista di dizionari
    samples = [sample for sample in results]
    for sample in samples:
        sample["_id"] = str(sample["_id"])  # Converti ObjectId in stringa

    return jsonify(samples)

# find by id di una sessione
@server.route('/samples/find_by_id/<sample_id>', methods=['GET'])
def get_sample_by_id(sample_id):
    try:
        # Converti l'id in ObjectId
        object_id = ObjectId(sample_id)
    except:
        return jsonify({"error": "Invalid sample_id format"}), 400

    # Esegui la query per trovare il campione con l'_id specificato
    result = collection_sensor.find_one({"_id": object_id})

    if result:
        result["_id"] = str(result["_id"])  # Converti ObjectId in stringa
        return jsonify(result)
    else:
        return jsonify({"error": "Sample not found"}), 404


# Route to edit a session by ID (name only)
@server.route('/session/edit/<id>', methods=['PATCH'])
def edit_session(id):
    try:
        # Extract the session name from the request
        name = request.json.get('name')
        if not name:
            return jsonify({"error": "Name is required"}), 400

        # Verify if the ID is a valid ObjectId
        if not ObjectId.is_valid(id):
            return jsonify({"error": "Invalid ObjectId format"}), 400

        # Convert the ID to ObjectId
        object_id = ObjectId(id)

        # Update the session name and updated_at fields
        result = collection_session.find_one_and_update(
            {"_id": object_id},
            {"$set": {
                "name": name,
                "updated_at": datetime.now()
            }},
            return_document=True
        )

        if result:
            # Return the updated object
            result['_id'] = str(result['_id'])  # Convert ObjectId to string for JSON serialization
            return jsonify(result), 200
        else:
            return jsonify({"error": "Session not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500





@server.route('/user/login', methods=['POST'])
def login():
    data = request.get_json()
    mail = data.get('mail')
    password = data.get('password')

    if not mail or not password:
        return jsonify({'message': 'Mail e password sono richiesti!'}), 400

    hashed_password = Service.hash_password(password)
    user = collection_user.find_one({"mail": mail, "password": hashed_password})

    if user:
        # Genera un token JWT con informazioni aggiuntive
        payload = {
            "user_id": str(user["_id"]),  # Converti ObjectId in stringa
            "mail": user.get("mail", ""),  # Supponendo che 'email' sia un campo nel documento dell'utente
            #"exp": datetime.utcnow() + timedelta(hours=10)  # Token valido per 10 ore
        }
        token = jwt.encode(payload, server.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'token': token})

    return jsonify({'message': 'Credenziali non valide!'}), 401


@server.route('/user/new_user', methods=['POST'])
def newUser():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['SmartDrive']
    collection_user = db['user']

    # Estrarre il nome dalla richiesta API
    name = request.json.get('name')
    surname = request.json.get('surname')
    mail = request.json.get('mail')
    password = request.json.get('password')

    # Ottenere la data e ora attuale
    current_time = datetime.now()

    # Creare il documento da inserire nel database
    session_data = {
        'name': name,
        'surname': surname,
        'mail': mail,
        'password': Service.hash_password(password),
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


if __name__ == "__main__":
    app.run_server(port=8000, host="0.0.0.0")