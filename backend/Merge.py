#!/bin/env python
# Requires: youtube_dl module
# Requires: ffmpeg
# Usage:
#
# python youtube2mp3.py <URL>, ...
#
# Example:
#
# python youtube2mp3.py https://www.youtube.com/watch?v=dQw4w9WgXcQ
import urllib
import re
from random import randint
import urllib.request
import youtube_dl
import uuid
from pydub import AudioSegment
from pydub import AudioSegment
from pydub.playback import play
import os
from firebase_admin import credentials, initialize_app, storage

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


def merge_song(artist, my_url):
    name = "/tmp/" + artists[artist] + "typebeat"

    ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': name + '.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '192',
    }],
    }

    url = beat_find(artists[artist])
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    
    name = name + ".wav"

    audio = AudioSegment.from_wav(name)
    louder_audio = audio - 7
    louder_audio.export(name, format='wav')

    my_file = merge_audio(artists[artist], name, my_url)
    return store_song(my_file)


# find youtube video of beat given an artist's name
def beat_find(artist):
    search = artist + "typebeat"
    html = urllib.request.urlopen(
        "https://www.youtube.com/results?search_query=" + search)
    vidIDList = re.findall(r"watch\?v=(\S{11})", html.read().decode())

    # randomly select for 10 videos in search result
    i = randint(0, 9)
    return "https://www.youtube.com/watch?v=" + vidIDList[i]


# layer audio files of singing and beat
def merge_audio(artist, name, url):
    sec_start = 30
    startTime = sec_start * 1000
    endTime = 60 * 1000
    trim = AudioSegment.from_wav(name)
    trim = trim[startTime:endTime]
    trim.export(name, format="wav")

    sound1 = AudioSegment.from_file(name)  # beat

    new_name = "/tmp/" + str(uuid.uuid4()) + ".wav"
    urllib.request.urlretrieve(url, new_name)

    sound2 = AudioSegment.from_file(new_name)  # vocals

    merge = sound1.overlay(sound2)
    merged = "/tmp/" + artist + "-" + str(uuid.uuid4())+ ".wav"
    merge.export(merged, format='wav')

    return merged

def store_song(merged):
    # Put your local file path 
    bucket = storage.bucket()
    blob = bucket.blob(merged)
    blob.upload_from_filename(merged)

    blob.make_public()
    return blob.public_url
