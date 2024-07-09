import pymongo
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

global forest_model
forest_model = None

def train_model_mongodb():
    # Connessione a MongoDB
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['SmartDrive']
    collection = db['test']

    # Estrazione dei dati dal database
    cursor = collection.find({})
    data = list(cursor)

    # Preparazione dei dati
    X = []
    y = []

    for entry in data:
        X.append([entry['total_acceleration'], entry['speed']])  # Features: total_acceleration e speed
        y.append(entry['classification'])  # Target: classification

    # Split dei dati in set di addestramento e test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Creazione del modello Random Forest
    forest_model = RandomForestClassifier(n_estimators=100, random_state=42)

    # Addestramento del modello
    forest_model.fit(X_train, y_train)

    # Valutazione del modello con cross-validation
    scores = cross_val_score(forest_model, X_train, y_train, cv=5)
    print(f'Cross-Validation Scores: {scores}')
    print(f'Mean Cross-Validation Accuracy: {scores.mean()}')

    # Predizione sui dati di test
    y_pred = forest_model.predict(X_test)

    # Valutazione delle prestazioni del modello sui dati di test
    print(classification_report(y_test, y_pred))

    # Test con nuovi dati
    # new_data = [[acceleration, speed]]
    # prediction = forest_model.predict(new_data)
    # print(f'Predizione : {prediction}')
    # return prediction[0]

    # Ritorna il modello addestrato
    return forest_model


def calculateStyle(acceleration, speed):
    # Connessione a MongoDB
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['SmartDrive']
    collection = db['test']

    # Estrazione dei dati dal database
    cursor = collection.find({})
    data = list(cursor)

    # Preparazione dei dati
    X = []
    y = []

    for entry in data:
        X.append([entry['total_acceleration'], entry['speed']])  # Features: total_acceleration e speed
        y.append(entry['classification'])  # Target: classification

    # Split dei dati in set di addestramento e test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Creazione del modello Random Forest
    forest_model = RandomForestClassifier(n_estimators=100, random_state=42)

    # Addestramento del modello
    forest_model.fit(X_train, y_train)

    # # Valutazione del modello con cross-validation
    # scores = cross_val_score(forest_model, X_train, y_train, cv=5)
    # print(f'Cross-Validation Scores: {scores}')
    # print(f'Mean Cross-Validation Accuracy: {scores.mean()}')
    #
    # # Predizione sui dati di test
    # y_pred = forest_model.predict(X_test)
    #
    # # Valutazione delle prestazioni del modello sui dati di test
    # print(classification_report(y_test, y_pred))

    # Test con nuovi dati
    new_data = [[acceleration, speed]]
    prediction = forest_model.predict(new_data)
   # print(f'Predizione : {prediction}')
    return prediction[0]

    # Ritorna il modello addestrato
    #return forest_model


# def estimate_driving_style(acceleration, speed):
#     global forest_model
#
#     # Controlla se il modello è già stato addestrato
#     if forest_model is None:
#         print("Addestra il modello prima di fare previsioni.")
#         return None
#
#     # Effettua la previsione utilizzando il modello addestrato
#     prediction = forest_model.predict([[acceleration, speed]])
#     return prediction[0]


#train_model_mongodb()

