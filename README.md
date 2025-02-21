# Blackforest
Analyze trends from my Spotify Wrapped playlists.

# Methodology

## Gathering the data
I wanted to programmatically get the data from Spotify using its API. Some parts I was able to do so
easily. Others -- namely the song titles from my playlists -- proved to be challenging for me.  

I settled on just gathering the song id, the year, and its position manually. It is then inserted into
MongoDB wherein I make queries to analyze the trends.

## Spotify API
Visit [this website](https://developer.spotify.com/documentation/web-api) for the instructions on how
to use Spotify's web API.

## Inserting to MongoDB
The `InsertApp.py` takes in a text input file and inserts it to the database.
