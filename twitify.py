import twitter
import spotipy
from urllib.parse import urlparse
import requests
from collections import Counter
# from urlextract import URLExtract
# import pprint
import spotipy.util as util
from datetime import datetime
# import http.client
                            
                            # function for shortened URLs
# written by bersam, http://stackoverflow.com/a/30156125/3369482
def unshorten_url(url):
    return requests.head(url, allow_redirects=True).url
    
                            # the TWITTER section
api = twitter.Api(consumer_key='z0MuxyldhHoDKVtK7DiHN8wf5',
        consumer_secret='', # consumer secret key needed
        access_token_key='', # access token key needed
        access_token_secret='', # access token secret
        sleep_on_rate_limit=True)

twitSet = set([])

# run the query, get 5k tweets
x = 0;
twitList = []

# query for near GSU
# twitLocResults = api.GetSearch(raw_query='q="open.spotify.com%2Ftrack%2F"&count=100&url="spotify"&result_type=recent&geocode=33.7529589,-84.3865189,10mi')

while len(twitList) < 5000:
    query = api.GetSearch(raw_query='q="open.spotify.com%2Ftrack%2F"&count=100&url="spotify"&result_type=recent')
    for Status in query:
        if len(Status.urls) > 0:
            tempURL = str(Status.urls[0]).split(',')[0].split(' ')[1].split('?')[0].strip('"')
            parse_object = urlparse(tempURL)
            if parse_object.netloc != 'open.spotify.com':
                # print(tempURL)
                tempURL = unshorten_url(tempURL)     
            twitList.append(str(Status.id)+tempURL)
            print(str(len(twitList)) + ' tweets and counting.')

#for status in twitList:
#    print(status)

spotList = []
for item in twitList:   
    parse_object = urlparse(item[17:])

    if parse_object.netloc == 'open.spotify.com':
            uri = 'spotify:track:' + parse_object.path[7:]
            spotList.append(uri)

print(str(len(spotList)) + ' tracks were used to compile this ranking.')

Count10 = Counter(spotList).most_common(10)

num = 1
for item in Count10:
    print(str(num) + '. ' + str(item))
    num += 1



send10 = list(zip(*Count10))[0]

                               #the SPOTIFY section
# make spotify playlist of hot 100
scope = 'playlist-modify-public'
username = '' # username needed
playlist_name = 'Top 100 for ' + str(datetime.now().strftime('%c'))
client_id = '' # client id needed
client_secret = '' # secret client needed
redirect_uri = 'http://localhost:8888/callback'

token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    playlists = sp.user_playlist_create(username, playlist_name)
    # pprint.pprint(playlists)
    playlist_id = playlists['id']
    adds = sp.user_playlist_add_tracks(username, playlist_id, send10)
    print(adds)

else:
    print('Can''t get token for', username)