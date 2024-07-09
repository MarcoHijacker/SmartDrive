from pymongo import MongoClient
import math



# mi connetto al db e alla collection di test
client = MongoClient('mongodb://localhost:27017/')
db = client['SmartDrive']
collection = db['test']

#itero su tutte le istanze presenti nel db e ne stimo lo stile di guida
def update_classification():

    # Trova tutte le istanze nel database
    instances = collection.find()

    for instance in instances:

        accel_x = instance.get('accel_x', 0.0)  # accelerazione lungo x
        accel_y = instance.get('accel_y', 0.0)  # accelerazione lungo y
        accel_z = instance.get('accel_z', 0.0)  # accelerazione lungo z
        accel = math.sqrt(accel_x**2 + accel_y**2 + accel_z**2)  # calcolo l'accelerazione totale

        speed = instance.get('speed', 0.0)

        classification = calculateStyle(accel, speed * 3.6)

        # Aggiorna il documento nel database con la nuova classificazione
        collection.update_one(
            {'_id': instance['_id']},
            {'$set': {'classification': classification}}
        )

        collection.update_one(
            {'_id': instance['_id']},
            {'$set': {'total_acceleration': accel}}
        )



def calculateStyle(acceleration, speed):
    # Definizione delle soglie per ciascuno stile di guida

    if 0 <= speed and speed < 40:
        if acceleration >= 0 and acceleration < 4:
            print("Prudent")
            return 1
        elif 4 <= acceleration and acceleration < 6:
            print("Normal")
            return 2
        elif 6 <= acceleration and acceleration < 9:
            print("Sporty")
            return 3
        elif acceleration >= 9:
            print("Aggressive")
            return 4
    elif 40 <= speed and speed < 60:
        if acceleration >=0 and acceleration < 3:
            print("Prudent")
            return 1
        elif 3 <= acceleration and acceleration < 5:
            print("Normal")
            return 2
        elif 5 <= acceleration and acceleration < 8:
            print("Sporty")
            return 3
        elif acceleration >= 8:
            print("Aggressive")
            return 4
    elif 60 <= speed and speed < 80:
        if acceleration >= 0 and acceleration < 2:
            print("Prudent")
            return 1
        elif 2 <= acceleration and acceleration < 4:
            print("Normal")
            return 2
        elif 4 <= acceleration and acceleration < 7:
            print("Sporty")
            return 3
        elif acceleration >= 7:
            print("Aggressive")
            return 4
    elif 80 <= speed:
        if acceleration == 0:
            print("Prudent")
            return 1
        elif 0 < acceleration and acceleration < 3:
            print("Normal")
            return 2
        elif 3 <= acceleration and acceleration < 6:
            print("Sporty")
            return 3
        elif 6 <= acceleration: #
            print("Aggressive")
            return 4


#calculateStyle(3, 10)
#update_classification()
