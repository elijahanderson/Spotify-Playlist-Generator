import sys

import spotipy
import spotipy.util as util

"""
    since we need to be able to access the user's data in order to create a playlsit, we'll need to use
    the Authorization Code Flow
"""

# TODO -- make into executable program?

# scope to write access to a user's public playlists
scope = 'playlist-modify-public'

# get the user's username
if len(sys.argv) > 1 :
    username = sys.argv[1]
    print(username)
else :
    username = sys.argv[0]

# create token
token = util.prompt_for_user_token(username, scope,
                                   client_id='0902803f3ac24a998e14d0ee5c8d622a',
                                   client_secret='84fea3c48dc74976bb683ec81a9b9236',
                                   redirect_uri='https://example.com/callback/')
if token :
    sp = spotipy.Spotify(auth=token)
    username = sp.current_user()['id']
    print("\nEnter the artist's name: ", end='')
    artist = input().strip().title()
    print("\nEnter the song name: ", end='')
    song_name = input().strip().title()
    print('\nYour jam: ' + song_name + ' - ' + artist)
    print('\nHow many songs? ', end='')
    limit = input().strip()
    print('\nWhat do you want to name your playlist? ', end='')
    name = input().strip()

    try :
        song_list = sp.search(artist + ' ' + song_name, limit=None, type='track')
        track_id = song_list['tracks']['items'][0]['id']
    except IndexError :
        # if spotify can't find the song in the searchf
        print('Unable to find a song by that name. Try entering just an artist or specific genre: ', end='')
        alt_name = input().strip()
        song_list = sp.search(alt_name, limit=None)
        track_id = song_list['tracks']['items'][0]['id']

    id_list = []

    # use spotipy's recommendations() function to get a list of related song id's
    # Spotify already has a list of attributes that describe your song -- this just identifies songs with similar
    # attributes and returns them as dict objects
    recommendations = sp.recommendations(seed_tracks=[song_list['tracks']['items'][0]['id']], limit=limit)
    recommendations = recommendations['tracks']
    print(recommendations)
    for track in recommendations :
        id_list.append(track['id'])

    print(id_list)

    # create the playlist for the user
    sp.user_playlist_create(username, name, public=True)

    # get the id of the playlist just created (will always be the first element)
    playlist_id = sp.user_playlists(username)['items'][0]['id']
    sp.user_playlist_add_tracks(username, playlist_id, id_list, position=None)

    print('Your playlist has been created! It should now appear in your profile. Enjoy!')

else :
    print('Couldn\'t get token for ' + username)