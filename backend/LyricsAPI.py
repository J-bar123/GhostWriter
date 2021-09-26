from flask import Blueprint, jsonify, request
from Merge import merge_song
import tensorflow as tf
import numpy as np


cred = credentials.Certificate("shellhacks-327117-firebase-adminsdk-ied2w-40fa331493.json")
initialize_app(cred, {'storageBucket': 'shellhacks-327117.appspot.com'})


artists = {
    "kanye": "kanyewest",
    "nas": "nas",
    "biggie": "biggie",
    "jayz": "jayz",
    "ross": "rick ross",
    "kendrick": "kendrick",
    "50cent": "50cent"
}

lyrics_api = Blueprint('lyrics_api', __name__)

@lyrics_api.route("/generate/", methods=['POST'])
def combine():

    data = request.get_json(force=True)
    artist = data['artist']
    return doSomeWork(artist)


