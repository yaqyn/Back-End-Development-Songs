from . import app
import os
import json
import sys

import pymongo
from flask import jsonify, request
from pymongo import MongoClient
from bson import json_util
from pymongo.errors import OperationFailure
from pymongo.results import InsertOneResult

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "songs.json")
songs_list: list = json.load(open(json_url))

mongodb_service = os.environ.get("MONGODB_SERVICE")
mongodb_username = os.environ.get("MONGODB_USERNAME")
mongodb_password = os.environ.get("MONGODB_PASSWORD")
mongodb_port = os.environ.get("MONGODB_PORT", "27017")

if mongodb_service is None:
    app.logger.error("Missing MongoDB server in the MONGODB_SERVICE variable")
    sys.exit(1)

if mongodb_username and mongodb_password:
    url = (
        f"mongodb://{mongodb_username}:{mongodb_password}"
        f"@{mongodb_service}:{mongodb_port}"
    )
else:
    url = f"mongodb://{mongodb_service}:{mongodb_port}"

print(f"Connecting to MongoDB at {mongodb_service}:{mongodb_port}")

try:
    client = MongoClient(url, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")
except OperationFailure as exc:
    app.logger.error(f"Authentication error: {exc}")
    sys.exit(1)

db = client.songs
# Keep the service idempotent: seed the collection only when it is empty.
if db.songs.count_documents({}) == 0:
    db.songs.insert_many(songs_list)


def parse_json(data):
    return json.loads(json_util.dumps(data))


######################################################################
# RETURN HEALTH OF THE APP
######################################################################
@app.route("/health")
def health():
    return jsonify({"status": "OK"}), 200


######################################################################
# COUNT THE NUMBER OF SONGS
######################################################################
@app.route("/count")
def count():
    """Return the number of documents in the songs collection."""
    return {"count": db.songs.count_documents({})}, 200


######################################################################
# GET ALL SONGS
######################################################################
@app.route("/song", methods=["GET"])
def songs():
    """Return every song in the collection."""
    results = list(db.songs.find({}))
    return {"songs": parse_json(results)}, 200


######################################################################
# GET A SONG
######################################################################
@app.route("/song/<int:id>", methods=["GET"])
def get_song_by_id(id):
    song = db.songs.find_one({"id": id})
    if not song:
        return {"message": f"song with id {id} not found"}, 404
    return parse_json(song), 200


######################################################################
# CREATE A SONG
######################################################################
@app.route("/song", methods=["POST"])
def create_song():
    song_in = request.get_json(silent=True)
    if not isinstance(song_in, dict) or "id" not in song_in:
        return {"message": "invalid song payload"}, 400

    song = db.songs.find_one({"id": song_in["id"]})
    if song:
        return {
            "Message": f"song with id {song_in['id']} already present"
        }, 302

    insert_id: InsertOneResult = db.songs.insert_one(song_in)
    return {"inserted id": parse_json(insert_id.inserted_id)}, 201


######################################################################
# UPDATE A SONG
######################################################################
@app.route("/song/<int:id>", methods=["PUT"])
def update_song(id):
    song_in = request.get_json(silent=True)
    if not isinstance(song_in, dict):
        return {"message": "invalid song payload"}, 400

    song = db.songs.find_one({"id": id})
    if song is None:
        return {"message": "song not found"}, 404

    result = db.songs.update_one({"id": id}, {"$set": song_in})
    if result.modified_count == 0:
        return {"message": "song found, but nothing updated"}, 200

    return parse_json(db.songs.find_one({"id": id})), 201


######################################################################
# DELETE A SONG
######################################################################
@app.route("/song/<int:id>", methods=["DELETE"])
def delete_song(id):
    result = db.songs.delete_one({"id": id})
    if result.deleted_count == 0:
        return {"message": "song not found"}, 404
    return "", 204
