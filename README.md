# Back-End-Development-Songs

Flask REST service that serves the band's songs from MongoDB.

## Environment setup

This repository is based on the official IBM Developer Skills Network
`hvlga-Back-End-Development-Songs` course template. The IBM lab setup uses
Python 3.9.x and provides `bin/setup.sh`. In this workspace, the project was
also tested using Python 3.9.25 in the named `backend-songs-venv` environment.
That named environment is separate from the course script's default `~/venv`.

```bash
bash bin/setup.sh  # IBM course-lab setup
# In a fresh terminal, activate the course-created environment:
source ~/venv/bin/activate
python3.9 --version
# Or use the separately named local environment:
python3.9 -m venv ~/backend-songs-venv
source ~/backend-songs-venv/bin/activate
python --version  # Python 3.9.25 in this workspace
pip install -r requirements.txt
pip install requests  # test client dependency
pytest
```

`bin/setup.sh` is the provided course setup script. It uses `sudo apt-get`,
appends environment settings to `~/.bashrc`, and calls `make db`; run it only in
the IBM course lab where those prerequisites are configured. The `backend-songs-venv`
environment and Songs tests were verified locally with Python 3.9.25 and MongoDB.

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
