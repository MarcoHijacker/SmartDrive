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
            {'$set': {'classification': classification},}
        )

       # collection.update_one(
       #     {'_id': instance['_id']},
       #     {'$set': {'total_acceleration': accel}}
       # )



def calculateStyle(acceleration, speed):
    # Definizione delle soglie per ciascuno stile di guida
    #limits = {
        #"Prudent": {"acceleration": (0, 2), "speed": (0, 60)},
        #"Normal": {"acceleration": (2, 4), "speed": (60, 80)},
        #"Sporty": {"acceleration": (4, 6), "speed": (80, 100)},
        #"Aggressive": {"acceleration": (6, float('inf')), "speed": (100, float('inf'))}
    #}

    limits = {
        "Prudent": {"speed": (0, 60)},
        "Normal": {"speed": (60, 80)},
        "Sporty": {"speed": (80, 100)},
        "Aggressive": {"speed": (100, float('inf'))}
    }



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
        elif 6 <= acceleration:
            print("Aggressive")
            return 4

        #if acc_min <= acceleration < acc_max and spe_min <= speed < spe_max:
            #print(style)
            #return style

    # Se non rientra in nessun criterio, determina lo stile più vicino in base alla distanza dalle soglie
    # distances = {}
    # for style, measure in limits.items():
    #     acc_min, acc_max = measure["acceleration"]
    #     spe_min, spe_max = measure["speed"]
    #
    #     # Calcola la distanza dalle soglie
    #     dist_acc = min(abs(acceleration - acc_min), abs(acceleration - acc_max))
    #     dist_spe = min(abs(speed - spe_min), abs(speed - spe_max))
    #
    #     # Calcola la distanza totale
    #     total_distance = dist_acc + dist_spe
    #     distances[style] = total_distance
    #
    # # Trova lo stile con la distanza minore
    # style_approximation = min(distances, key=distances.get)

    #print(style_approximation)
    #return style_approximation


#calculateStyle(1, 80)
update_classification()
