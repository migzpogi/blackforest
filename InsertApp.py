from pymongo import MongoClient
import pprint
import logging
import requests


logger = logging.getLogger(__name__)
api_token = 'YOUR_API_TOKEN_FROM_GENERATE_TOKEN_PY'

# the order of data information based on index
input_txt_mapping = {
    "wrapped_year": 0,
    "wrapped_rank": 1,
    "spotify_id": 2
}

# MongoDB client
client = MongoClient('0.0.0.0',
                     username='YOUR_MONGO_USERNAME',
                     password='YOUR_MONGO_USERNAME!',
                     authSource='YOUR_MONGO_AUTHSOURCE',
                     authMechanism='YOUR_MONGO_AUTHMECH')
db = client["YOUR_DBNAME"]
collection = db["YOUR_COLLECTIONNAME"]


class Song:
    def __init__(self, spotify_id, wrapped_year, wrapped_rank):
        self.spotify_id = spotify_id
        self.wrapped_year = wrapped_year
        self.wrapped_rank = wrapped_rank

        self.song_name = None
        self.song_artist = None
        self.song_artist_id = None
        self.all_artists = None
        self.genres = None

    def get_info_from_spotify(self):
        token = api_token
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f'https://api.spotify.com/v1/tracks/{self.spotify_id}', headers=headers).json()

        all_artists = []
        for artists in response['artists']:
            all_artists.append(artists['name'])

        self.song_name = response['name']
        self.song_artist = response['album']['artists'][0]['name']
        self.song_artist_id = response['album']['artists'][0]['id']
        self.all_artists = all_artists

        response_artist = requests.get(f'https://api.spotify.com/v1/artists/{self.song_artist_id}', headers=headers).json()

        self.genres = response_artist['genres']


def insert_song(song):
    data = {
        "songName": song.song_name,
        "wrappedYear": int(song.wrapped_year),
        "wrappedRank": int(song.wrapped_rank),
        "songSpotifyId": song.spotify_id,
        "songArtist": song.song_artist,
        "allArtists": song.all_artists
    }

    collection.insert_one(data)


def find_all_year(year):
    results = collection.find({ "wrappedYear": year })
    for r in results:
        print(f'Year: {year} - #{r["wrappedRank"]} - {r["songName"]} - {r["songArtist"]}')


def find_all_rank(rank):
    results = collection.find({ "wrappedRank": rank })
    for r in results:
        print(f'#{r["wrappedRank"]} - {r["wrappedYear"]} - {r["songName"]} - {r["songArtist"]}')


def find_in_song_collection(song_spotify_id):
    results = collection.find({"songSpotifyId": song_spotify_id})
    return results


def find_duplicate_songs():
    results = collection.aggregate(
        [
            {"$group": {"_id": "$songSpotifyId", "count":{ "$sum": 1 }}},
            {"$match": {"count": { "$gt": 1 }}}
        ]
    )
    for song in results:
        result = find_in_song_collection(song["_id"])
        for r in result:
            print(f"{r['songName']} - {r['wrappedYear']} - #{r['wrappedRank']}")


def get_songs_from_input(input_file="input.txt", delimiter=";", mapping=None):
    list_of_songs = []
    if mapping is None:
        mapping = input_txt_mapping
    with open(input_file, 'r') as f:
        for lines in f.readlines():
            line = lines.strip().split(delimiter)
            song = Song(spotify_id=line[mapping.get("spotify_id")],
                        wrapped_year=line[mapping.get("wrapped_year")],
                        wrapped_rank=line[mapping.get("wrapped_rank")]
                        )
            list_of_songs.append(song)

    return list_of_songs


def foo():
    return 1


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',
        handlers=[
            # logging.FileHandler("songs.log"),
            logging.StreamHandler()
        ]
    )

    logger.info("Starting InsertApp")

    list_of_songs = get_songs_from_input()

    for song in list_of_songs:
        song.get_info_from_spotify()
        logging.info(vars(song))
        insert_song(song)

    find_all_year(2016)
    print("--- --- ---")
    find_all_rank(1)
    print("--- --- ---")
    find_duplicate_songs()