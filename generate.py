"""
    Spotify Playlist Generator -- Given a song or band name, this program creates a spotify playlist with similar music.

    By Eli Anderson
"""

import sys

import spotipy
import spotipy.util as util

"""
    since we need to be able to access the user's data in order to create a playlsit, we'll need to use
    the Authorization Code Flow
"""

# scope to write access to a user's public playlists
scope = 'playlist-modify-public'

# get the user's username
if len(sys.argv) > 1 :
    username = sys.argv[1]
    print(username)
else :
    username = sys.argv[0]

token = util.prompt_for_user_token(username, scope, client_secret='84fea3c48dc74976bb683ec81a9b9236',
                                   client_id='0902803f3ac24a998e14d0ee5c8d622a',
                                   redirect_uri='https://example.com/callback/')

if token :
    print(True)
else :
    print(False)