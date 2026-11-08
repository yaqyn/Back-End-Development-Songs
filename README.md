# Back-End-Development-Songs

Flask REST service that serves the band's songs from MongoDB.

## Endpoints

| Method | Endpoint | Result |
|---|---|---|
| GET | `/health` | `{"status":"OK"}` |
| GET | `/count` | `{"count":20}` |
| GET | `/song` | `{"songs":[...]}` |
| GET | `/song/<id>` | One song or 404 |
| POST | `/song` | Create a song, 201 |
| PUT | `/song/<id>` | Update a song, 201 |
| DELETE | `/song/<id>` | Delete a song, 204 |

## Run and test

Start MongoDB, then:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
MONGODB_SERVICE=localhost MONGODB_PORT=27017 flask --app app run --debug
pytest
```
