from flask import Blueprint, jsonify, request
import requests
import time
import configparser
from Merge import merge_song

config = configparser.RawConfigParser()
config.read('config.ini')

token = config['DEFAULT']['token']
mixpanel = config['DEFAULT']['mixpanel']
mx_acc = config['DEFAULT']['mixpanel_acc']

cookies = {
    mx_acc: mixpanel,
    'access_token': '''Bearer {}'''.format(token),
    'G_AUTHUSER_H': '1',
    'G_ENABLED_IDPS': 'google',
}

songs_api = Blueprint('songs_api', __name__)
artists = {
    "kanye": "kanye-west-rap",
    "nas": "nas",
    "biggie": "biggie",
    "jayz": "jayz",
    "ross": "rick-ross",
    "kendrick": "kendrick-lamar",
    "50cent": "50-cent"
}

# kendrick


@songs_api.route("/combineSong/", methods=['POST'])
def combine():

    data = request.get_json(force=True)

    artist = data['artist']
    vocal_url = data['url']

    my_url = merge_song(artist, vocal_url)

    return jsonify({
        "Success": "Combined worked",
        "Url": my_url
    })


@songs_api.route("/getVocals/", methods=['POST'])
def get_vocals():
    data = request.get_json(force=True)

    

    artist = data['artist']
    lyrics = data['lyrics']
    pace = data['pace']

    print(lyrics)

    if not pace or pace == 1:
        pace = 1.0

    if artist not in artists or not lyrics:
        return jsonify({
            "Error": "Artist not found or lyrics are empty"
        })

    return send_lyric_request(artists[artist], lyrics, pace)


def send_lyric_request(artist, song, pace):
    headers = {
        'Authorization': '',
        'Referer': 'https://uberduck.ai/',
        'Connection': 'keep-alive',
        'Origin': 'https://uberduck.ai',
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
        'Content-Type': 'text/plain;charset=UTF-8',
        'Accept-Language': 'en-us',
        'Host': 'api.uberduck.ai',
        'Content-Length': '52',
    }

    data = '{"speech":"%s.~","voice":"%s", "pace":%1.1f}' % (
        song, artist, pace)

    if pace == 1.0:
        data = '{"speech":"%s.~","voice":"%s", "pace":1}' % (song, artist)

    response = requests.post(
        'https://api.uberduck.ai/speak', headers=headers, cookies=cookies, data=data.encode('utf-8').strip())

    print(response.json())
    if ('uuid' in response.json()):
        url = get_status(response.json()['uuid'])
        return url
    else:
        return jsonify({
            "Error": "Couldn't submit request"
        })


def get_status(uid):
    count = 0
    while count <= 15:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
            'Host': 'api.uberduck.ai',
            'Accept-Language': 'en-us',
            'Connection': 'keep-alive',
            'Referer': 'https://uberduck.ai/',
            'Accept': '*/*',
            'Origin': 'https://uberduck.ai',
        }

        params = (
            ('uuid', uid),
        )

        response = requests.get('https://api.uberduck.ai/speak-status',
                                headers=headers, params=params, cookies=cookies)

        if (response.json()['path'] != None):
            url_path = response.json()['path']
            return jsonify({
                "Success": "Synthesis worked",
                "Url": url_path
            })

        if (response.json()['failed_at'] != None):
            return jsonify({
                "Error": "Synthesis timeout"
            })

        time.sleep(2)
        count += 1

    return jsonify({
        "Error": "Synthesis timeout"
    })
