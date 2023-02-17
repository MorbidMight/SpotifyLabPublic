import spotipy
import json
from spotipy.oauth2 import SpotifyClientCredentials

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)
birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
results = spotify.playlist('2YRe7HRKNRvXdJBp9nXFza')
results = json.loads(json.dumps(results))
print(results)

def write_tracks(text_file, tracks):
    with open(text_file, 'a') as file_out:
        while True:
            for item in tracks['items']:
                if 'track' in item:
                    track = item['track']
                else:
                    track = item
                try:
                    trackName = track['name']
                    trackArtists = ''
                    for artist in track['artists']:
                        trackArtists += artist['name'] + ' & '
                    trackArtists = trackArtists[0:len(trackArtists)-3]
                    file_out.write(trackName + ', by ' + trackArtists + ', ID: ' + track['id'] + '\n')
                except KeyError:
                    print(u'Skipping track {0} by {1} (local only?)'.format(
                        track['name'], track['artists'][0]['name']))
            # 1 page = 50 results
            # check if there are more pages
            if tracks['next']:
                tracks = spotify.next(tracks)
            else:
                break


def write_playlist(username, playlist_id):
    results = spotify.playlist(username, playlist_id)
    text_file = u'{0}.txt'.format(results['name'], ok='-_()[]{}')
    print(u'Writing {0} tracks to {1}'.format(
        results['tracks']['total'], text_file))
    tracks = results['tracks']
    write_tracks(text_file, tracks)


# example playlist
write_tracks('popularTracks.txt', results['tracks'])
