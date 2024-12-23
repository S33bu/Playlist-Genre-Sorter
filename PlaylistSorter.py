from time import sleep
import requests
import urllib.parse
import os

user_id = "YOUR_USER_ID"
client_id = "YOUR_CLIENT_ID"
url = "https://api.spotify.com/v1/playlists/YOUR_PLAYLIST_ID (that you want to search)/tracks"
client_secret = "YOUR_CLIENT_SECRET"
redirect_uri = "YOUR_REDIRECT_URI"
scopes = "playlist-modify-public playlist-read-private"

auth_url = (
    "https://accounts.spotify.com/authorize"
    "?response_type=code"
    f"&client_id={client_id}"
    f"&redirect_uri={urllib.parse.quote(redirect_uri)}"
    f"&scope={urllib.parse.quote(scopes)}"
)

print("Please go to this URL and authorize the app:", auth_url)
##Copy the long string after code=... and paste here
token = input("Enter the new token: ")  

data = {
    'grant_type': 'authorization_code',
    'code': token,
    'redirect_uri': redirect_uri,
    'client_id': client_id,
    'client_secret': client_secret
}

jsonData = {
    "name": "Combined Playlist",
    "description": "one genre",
    "public": True
}

response = requests.post('https://accounts.spotify.com/api/token', data=data)
token_info = response.json()
access_token = token_info['access_token']
print("Access Token:", access_token)

headers = {
    "Authorization": f"Bearer {access_token}"
}
playlistUrl = f"https://api.spotify.com/v1/users/{user_id}/playlists"
userResponse = requests.post(playlistUrl, json=jsonData, headers=headers)
newPlaylistData = userResponse.json()
newPlaylistID = newPlaylistData["id"]

response = requests.get(url, headers=headers)
data = response.json()

i = 1
songUri = set()

for item in data['items']:
    track = item['track']
    name = track['name']
    uri = track['uri']
    
    artists = [artist['name'] for artist in track['artists']]
    artistID = [artist['id'] for artist in track['artists']]

    genres = []

    for artist_id in artistID:
        artist_url = f"https://api.spotify.com/v1/artists/{artist_id}"
        response_artist = requests.get(artist_url, headers=headers)
        data_artist = response_artist.json()
        
        artist_genres = data_artist.get('genres', [])
        genres.extend(artist_genres)

    if any("Drum and Bass" in genre or "dnb" in genre for genre in genres): ##Right now searches for drun and bass artists
        songUri.add(uri)
        print(f"Nr: {i}")
        i += 1
        print(f"Song: {name}")
        print(f"Song uri: {uri}")
        print(f"Artists: {', '.join(artists)}")
        print(f"ArtistIDs: {', '.join(artistID)}")
        print(f"Genres: {genres}")
        print("-" * 20)

listTrackURI = list(songUri)
newPlaylistURL = f"https://api.spotify.com/v1/playlists/{newPlaylistID}/tracks"
requests.post(newPlaylistURL, json=listTrackURI, headers=headers)