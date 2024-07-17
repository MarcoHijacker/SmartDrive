## SmartDrive REST Endpoints

**Base URI**  
`http://localhost:8000`

**Nota**
Gli endpoints con il suffisso *-JWT richiedono il suddetto token nell'header della richiesta.

### USER ENDPOINTS

---

#### user/new_user

**Descrizione**  
Permette di registrare un nuovo utente.

**Resource URI**  
`/user/new_user`

**Tipo di richiesta http**  
`POST`

**Headers**  
Nessuno

**Corpo della richiesta**  
| Parameter | Type   | Description       |
|-----------|--------|-------------------|
| email     | String | Email dell'utente |
| password  | String | Password dell'utente |

**Parametri della risposta**  
| Parameter | Type   | Description       |
|-----------|--------|-------------------|
| user_id   | String | ID dell'utente    |

**Codici di stato**  
| Codice | Descrizione |
|--------|-------------|
| 201    | Created     |

---

#### user/login

**Descrizione**  
Permette di autenticare un utente e ottenere un token JWT.

**Resource URI**  
`/user/login`

**Tipo di richiesta http**  
`POST`

**Headers**  
Nessuno

**Corpo della richiesta**  
| Parameter | Type   | Description       |
|-----------|--------|-------------------|
| email     | String | Email dell'utente |
| password  | String | Password dell'utente |

**Parametri della risposta**  
| Parameter | Type   | Description       |
|-----------|--------|-------------------|
| token     | String | Token JWT         |

**Codici di stato**  
| Codice | Descrizione |
|--------|-------------|
| 200    | OK          |

---

#### user/find_all

**Descrizione**  
Trova tutti gli utenti.

**Resource URI**  
`/user/find_all`

**Tipo di richiesta http**  
`GET`

**Headers**  
Nessuno

**Corpo della richiesta**  
Nessuno

**Parametri della risposta**  
| Parameter | Type   | Description       |
|-----------|--------|-------------------|
| user_id   | String | ID dell'utente    |
| email     | String | Email dell'utente |

**Codici di stato**  
| Codice | Descrizione |
|--------|-------------|
| 200    | OK          |

---

#### user/find_by_id

**Descrizione**  
Trova un utente per ID.

**Resource URI**  
`/user/find_by_id`

**Tipo di richiesta http**  
`GET`

**Headers**  
Nessuno

**Corpo della richiesta**  
Nessuno

**Parametri della risposta**  
| Parameter | Type   | Description       |
|-----------|--------|-------------------|
| user_id   | String | ID dell'utente    |
| email     | String | Email dell'utente |

**Codici di stato**  
| Codice | Descrizione |
|--------|-------------|
| 200    | OK          |
| 404    | Not Found   |

---

#### user/style_average-JWT

**Descrizione**  
Ottiene lo stile medio dell'utente.

**Resource URI**  
`/user/style_average`

**Tipo di richiesta http**  
`GET`

**Headers**  
| Chiave       | Valore                        |
|--------------|-------------------------------|
| Authorization| Bearer `YOUR_JWT_TOKEN`       |

**Corpo della richiesta**  
Nessuno

**Parametri della risposta**  
| Parameter      | Type   | Description          |
|----------------|--------|----------------------|
| style_average  | Float  | Media dello stile    |

**Codici di stato**  
| Codice | Descrizione               |
|--------|---------------------------|
| 200    | OK                        |
| 401    | Unauthorized (invalid JWT)|

---

#### user/get_session_statistics-JWT

**Descrizione**  
Ottiene le statistiche delle sessioni dell'utente.

**Resource URI**  
`/user/get_session_statistics`

**Tipo di richiesta http**  
`GET`

**Headers**  
| Chiave       | Valore                        |
|--------------|-------------------------------|
| Authorization| Bearer `YOUR_JWT_TOKEN`       |

**Corpo della richiesta**  
Nessuno

**Parametri della risposta**  
| Parameter           | Type   | Description               |
|---------------------|--------|---------------------------|
| average_acceleration| Float  | Accelerazione media       |
| average_speed       | Float  | Velocità media            |
| max_acceleration    | Float  | Accelerazione massima     |
| max_speed           | Float  | Velocità massima          |

**Codici di stato**  
| Codice | Descrizione               |
|--------|---------------------------|
| 200    | OK                        |
| 401    | Unauthorized (invalid JWT)|

---

#### user/get_global_statistics-JWT

**Descrizione**  
Ottiene le statistiche globali dell'utente.

**Resource URI**  
`/user/get_global_statistics`

**Tipo di richiesta http**  
`GET`

**Headers**  
| Chiave       | Valore                        |
|--------------|-------------------------------|
| Authorization| Bearer `YOUR_JWT_TOKEN`       |

**Corpo della richiesta**  
Nessuno

**Parametri della risposta**  
| Parameter           | Type   | Description               |
|---------------------|--------|---------------------------|
| average_acceleration| Float  | Accelerazione media       |
| average_speed       | Float  | Velocità media            |
| max_acceleration    | Float  | Accelerazione massima     |
| max_speed           | Float  | Velocità massima          |

**Codici di stato**  
| Codice | Descrizione               |
|--------|---------------------------|
| 200    | OK                        |
| 401    | Unauthorized (invalid JWT)|

---

#### user/modify-JWT

**Descrizione**  
Modifica le informazioni dell'utente.

**Resource URI**  
`/user/modify`

**Tipo di richiesta http**  
`PATCH`

**Headers**  
| Chiave       | Valore                        |
|--------------|-------------------------------|
| Authorization| Bearer `YOUR_JWT_TOKEN`       |

**Corpo della richiesta**  
| Parameter | Type   | Description       |
|-----------|--------|-------------------|
| email     | String | Email dell'utente |
| password  | String | Password dell'utente |

**Parametri della risposta**  
| Parameter | Type   | Description               |
|-----------|--------|---------------------------|
| message   | String | Messaggio di conferma     |

**Codici di stato**  
| Codice | Descrizione               |
|--------|---------------------------|
| 200    | OK                        |
| 401    | Unauthorized (invalid JWT)|

---

#### user/delete-JWT

**Descrizione**  
Elimina un utente.

**Resource URI**  
`/user/delete`

**Tipo di richiesta http**  
`DELETE`

**Headers**  
| Chiave       | Valore                        |
|--------------|-------------------------------|
| Authorization| Bearer `YOUR_JWT_TOKEN`       |

**Corpo della richiesta**  
Nessuno

**Parametri della risposta**  
| Parameter | Type   | Description               |
|-----------|--------|---------------------------|
| message   | String | Messaggio di conferma     |

**Codici di stato**  
| Codice | Descrizione               |
|--------|---------------------------|
| 200    | OK                        |
| 401    | Unauthorized (invalid JWT)|
| 404    | Not Found                 |

---

### SESSION ENDPOINTS

---

#### session/new_session-JWT

**Descrizione**  
Crea una nuova sessione per l'utente.

**Resource URI**  
`/session/new_session`

**Tipo di richiesta http**  
`POST`

**Headers**  
Nessuno

**Corpo della richiesta**  
| Parameter | Type   | Description        |
|-----------|--------|--------------------|
| name      | String | Nome della sessione|

**Parametri della risposta**  
| Parameter   | Type   | Description       |
|-------------|--------|-------------------|
| session_id  | String | ID della sessione |

**Codici di stato**  
| Codice | Descrizione               |
|--------|---------------------------|
| 201    | Created                   |
| 401    | Unauthorized (invalid JWT)|

---

#### session/find_by_user-JWT

**Descrizione**  
Trova tutte le sessioni associate a un utente specifico.

**Resource URI**  
`/session/find_by_user`

**Tipo di richiesta http**  
`GET`

**Headers**  
| Chiave       | Valore                                                                                              |
|--------------|------------------------------------------------------------------------------------------------------|
| Authorization| Bearer `<YOUR_JWT_TOKEN>` |

**Corpo della richiesta**  
Nessuno

**Parametri della risposta**  
| Parameter       | Type   | Description                 |
|-----------------|--------|-----------------------------|
| _id             | String | ID della sessione           |
| created_at      | String | Data di creazione           |
| latitude        | String | Latitudine                  |
| longitude       | String | Longitudine                 |
| name            | String | Nome della sessione         |
| status          | Null   | Stato della sessione        |
| style_average   | Null   | Media dello stile           |
| updated_at      | String | Data di aggiornamento       |
| user_id         | String | ID dell'utente              |

**Codici di stato**  
| Codice | Descrizione               |
|--------|---------------------------|
| 200    | OK                        |
| 401    | Unauthorized (invalid JWT)|

---

#### session/find_by_id

**Descrizione**  
Trova una sessione per ID.

**Resource URI**  
`/session/{session_id}`

**Tipo di richiesta http**  
`GET`

**Headers**  
Nessuno

**Corpo della richiesta**  
Nessuno

**Parametri della risposta**  
| Parameter   | Type   | Description       |
|-------------|--------|-------------------|
| _id         | String | ID della sessione |
| latitude    | String | Latitudine        |
| longitude   | String | Longitudine       |
| name        | String | Nome della sessione |
| status      | Null   | Stato della sessione|
| created_at  | String | Data di creazione |
| updated_at  | String | Data di aggiornamento|

**Codici di stato**  
| Codice | Descrizione |
|--------|-------------|
| 200    | OK          |
| 404    | Not Found   |

---

#### session/find_all

**Descrizione**  
Trova tutte le sessioni.

**Resource URI**  
`/session/find_all`

**Tipo di richiesta http**  
`GET`

**Headers**  
Nessuno

**Corpo della richiesta**  
Nessuno

**Parametri della risposta**  
| Parameter   | Type   | Description       |
|-------------|--------|-------------------|
| _id         | String | ID della sessione |
| latitude    | String | Latitudine        |
| longitude   | String | Longitudine       |
| name        | String | Nome della sessione |
| status      | Null   | Stato della sessione|
| created_at  | String | Data di creazione |
| updated_at  | String | Data di aggiornamento|

**Codici di stato**  
| Codice | Descrizione |
|--------|-------------|
| 200    | OK          |

---

#### session/activate_by_id-JWT

**Descrizione**  
Attiva una sessione per ID.

**Resource URI**  
`/session/activate/{session_id}`

**Tipo di richiesta http**  
`PATCH`

**Headers**  
| Chiave       | Valore                                                                                              |
|--------------|------------------------------------------------------------------------------------------------------|
| Authorization| Bearer `<YOUR_JWT_TOKEN>` |

**Corpo della richiesta**  
Nessuno

**Parametri della risposta**  
| Parameter   | Type   | Description       |
|-------------|--------|-------------------|
| _id         | String | ID della sessione |
| latitude    | String | Latitudine        |
| longitude   | String | Longitudine       |
| name        | String | Nome della sessione |
| status      | Int    | Stato della sessione|
| created_at  | String | Data di creazione |
| updated_at  | String | Data di aggiornamento|

**Codici di stato**  
| Codice | Descrizione               |
|--------|---------------------------|
| 200    | OK                        |
| 401    | Unauthorized (invalid JWT)|
| 404    | Not Found                 |

---

#### session/deactivate_by_id-JWT

**Descrizione**  
Disattiva una sessione per ID.

**Resource URI**  
`/session/deactivate/{session_id}`

**Tipo di richiesta http**  
`PATCH`

**Headers**  
| Chiave       | Valore                                                                                              |
|--------------|------------------------------------------------------------------------------------------------------|
| Authorization| Bearer `<YOUR_JWT_TOKEN>` |

**Corpo della richiesta**  
Nessuno

**Parametri della risposta**  
| Parameter   | Type   | Description       |
|-------------|--------|-------------------|
| _id         | String | ID della sessione |
| latitude    | String | Latitudine        |
| longitude   | String | Longitudine       |
| name        | String | Nome della sessione |
| status      | Int    | Stato della sessione|
| created_at  | String | Data di creazione |
| updated_at  | String | Data di aggiornamento|

**Codici di stato**  
| Codice | Descrizione               |
|--------|---------------------------|
| 200    | OK                        |
| 401    | Unauthorized (invalid JWT)|
| 404    | Not Found                 |

---

#### session/style_average/{id_session}

**Descrizione**  
Aggiorna lo stile medio della sessione.

**Resource URI**  
`/session/style_average/{id_session}`

**Tipo di richiesta http**  
`PATCH`

**Headers**  
Nessuno

**Corpo della richiesta**  
Nessuno

**Parametri della risposta**  
| Parameter   | Type    | Description           |
|-------------|---------|-----------------------|
| _id         | String  | ID della sessione     |
| latitude    | Float   | Latitudine            |
| longitude   | Float   | Longitudine           |
| name        | String  | Nome della sessione   |
| status      | Int     | Stato della sessione  |
| style_average | Int   | Media dello stile     |
| created_at  | String  | Data di creazione     |
| updated_at  | String  | Data di aggiornamento |

**Codici di stato**  
| Codice | Descrizione               |
|--------|---------------------------|
| 200    | OK                        |
| 404    | Not Found                 |

---

#### session/delete_by_id

**Descrizione**  
Elimina una sessione per ID.

**Resource URI**  
`/session/delete/{session_id}`

**Tipo di richiesta http**  
`DELETE`

**Headers**  
Nessuno

**Corpo della richiesta**  
Nessuno

**Parametri della risposta**  
| Parameter | Type   | Description                                  |
|-----------|--------|----------------------------------------------|
| message   | String | Messaggio di conferma dell'eliminazione della sessione |

**Codici di stato**  
| Codice | Descrizione |
|--------|-------------|
| 200    | OK          |
| 404    | Not Found   |

---

### SAMPLES ENDPOINTS

#### samples/find_by_id_session

**Descrizione**  
Trova i campioni per ID della sessione.

**Resource URI**  
`samples/find_by_session/{session_id}`

**Tipo di richiesta http**  
`GET`

**Headers**  
Nessuno

**Corpo della richiesta**  
Nessuno

**Parametri della risposta**  
| Parameter         | Type    | Description               |
|-------------------|---------|---------------------------|
| _id               | String  | ID del campione           |
| accel_x           | Float   | Accelerazione X           |
| accel_y           | Float   | Accelerazione Y           |
| accel_z           | Float   | Accelerazione Z           |
| gyro_x            | Float   | Giroscopio X              |
| gyro_y            | Float   | Giroscopio Y              |
| gyro_z            | Float   | Giroscopio Z              |
| latitude          | Float   | Latitudine                |
| longitude         | Float   | Longitudine               |
| session_id        | String  | ID della sessione         |
| speed             | Float   | Velocità                  |
| style             | Int     | Stile                     |
| time              | String  | Tempo                     |
| total_acceleration| Float   | Accelerazione totale      |
| created_at        | String  | Data di creazione         |
| updated_at        | String  | Data di aggiornamento     |

**Codici di stato**  
| Codice | Descrizione |
|--------|-------------|
| 200    | OK          |
| 404    | Not Found   |

---

#### samples/find_all

**Descrizione**  
Trova tutti i campioni.

**Resource URI**  
`samples/find_all`

**Tipo di richiesta http**  
`GET`

**Headers**  
Nessuno

**Corpo della richiesta**  
Nessuno

**Parametri della risposta**  
| Parameter         | Type    | Description               |
|-------------------|---------|---------------------------|
| _id               | String  | ID del campione           |
| accel_x           | Float   | Accelerazione X           |
| accel_y           | Float   | Accelerazione Y           |
| accel_z           | Float   | Accelerazione Z           |
| gyro_x            | Float   | Giroscopio X              |
| gyro_y            | Float   | Giroscopio Y              |
| gyro_z            | Float   | Giroscopio Z              |
| latitude          | Float   | Latitudine                |
| longitude         | Float   | Longitudine               |
| session_id        | String  | ID della sessione         |
| speed             | Float   | Velocità                  |
| style             | Int     | Stile                     |
| time              | String  | Tempo                     |
| total_acceleration| Float   | Accelerazione totale      |
| created_at        | String  | Data di creazione         |
| updated_at        | String  | Data di aggiornamento     |

**Codici di stato**  
| Codice | Descrizione |
|--------|-------------|
| 200    | OK          |

---

### samples/find_by_id

**Descrizione**  
Trova un campione per ID.

**Resource URI**  
`samples/find_by_id`

**Tipo di richiesta http**  
`GET`

**Headers**  
Nessuno

**Corpo della richiesta**  
Nessuno

**Parametri della risposta**  
| Parameter           | Type   | Description                 |
|---------------------|--------|-----------------------------|
| sample_id           | String | ID del campione             |
| accel_x             | Float  | Accelerazione X             |
| accel_y             | Float  | Accelerazione Y             |
| accel_z             | Float  | Accelerazione Z             |
| created_at          | String | Data di creazione           |
| gyro_x              | Float  | Giroscopio X                |
| gyro_y              | Float  | Giroscopio Y                |
| gyro_z              | Float  | Giroscopio Z                |
| latitude            | Float  | Latitudine                  |
| longitude           | Float  | Longitudine                 |
| session_id          | String | ID della sessione           |
| speed               | Float  | Velocità                    |
| style               | Int    | Stile                       |
| time                | String | Tempo                       |
| total_acceleration  | Float  | Accelerazione totale        |
| updated_at          | String | Data di aggiornamento       |

**Codici di stato**  
| Codice | Descrizione               |
|--------|---------------------------|
| 200    | OK                        |
| 404    | Not Found                 |