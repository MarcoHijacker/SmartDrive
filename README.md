# Back-end Progetto SmartDrive (Longo-Tarantino)

## Panoramica
SmartDrive è un progetto volto a fornire servizi backend per l'elaborazione e l'analisi dei dati di guida. Questo progetto include una raccolta di API definite in una collezione Postman, che possono essere distribuite e testate utilizzando le istruzioni fornite di seguito.

## Prerequisiti
Assicurati di avere installato:
- Python 3.8 o superiore
- MongoDB

## Installazione

### Passo 1: Clona il Repository
```bash
git clone https://github.com/MarcoHijacker/SmartDrive
cd SmartDrive

### Passo 2: Installa le Dipendenze del Backend
Installa le librerie necessarie usando `pip`:
```bash
pip install -r requirements.txt
```

## Avvio dei Servizi Backend
Per avviare i servizi backend, esegui il seguente comando:
```bash
python3 Server.py
```
Oppure:
```bash
python Server.py
```

## Configurazione del Database
Se hai bisogno di ricreare il database per scopi dimostrativi, segui questi passaggi per caricare i dati di esempio in MongoDB:

1. Assicurati che MongoDB sia in esecuzione sul tuo computer locale o accessibile dal tuo ambiente.
2. Crea un nuovo database chiamato `SmartDrive`.
3. Carica le collezioni JSON in MongoDB. Puoi utilizzare i seguenti comandi (assicurati di navigare nella directory contenente i file JSON):

```bash
mongoimport --db SmartDrive --collection user --file database/SmartDrive.user_final.json --jsonArray
mongoimport --db SmartDrive --collection test --file database/SmartDrive.test_final.json --jsonArray
mongoimport --db SmartDrive --collection samples --file database/SmartDrive.samples_final.json --jsonArray
mongoimport --db SmartDrive --collection session --file database/SmartDrive.session_final.json --jsonArray
```

**Nota:** La password per tutti gli utenti nella collezione `SmartDrive.user_final.json` è `prova`.

## Utilizzo
Una volta che i servizi backend sono in esecuzione, puoi interagire con le API come definito nella collezione Postman inclusa nel repository. Utilizza strumenti come Postman per testare gli endpoint e verificare la funzionalità. I servizi attivi consentono un corretto funzionamento anche del front-end (`SmartDrive-Panel`).

## Contributi
Sentiti libero di contribuire a questo progetto inviando issue o pull request. Per modifiche importanti, apri prima un'issue per discutere cosa vorresti cambiare.

## Licenza
Questo progetto è concesso in licenza sotto la Licenza MIT - vedi il file [LICENSE](LICENSE) per i dettagli.

## Contatti
Per qualsiasi domanda o supporto, contatta [marco.longo@studenti.unisalento.it](mailto:marco.longo@studenti.unisalento.it) oppure [priamo.tarantino@studenti.unisalento.it](mailto:priamo.tarantino@studenti.unisalento.it).
```