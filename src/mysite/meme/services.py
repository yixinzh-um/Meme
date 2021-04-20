import os
import requests

def get_fliker():
    url = 'https://www.flickr.com/services/rest'
    r = requests.get(url, headers={'Authorization':'Bearer %s' % 'access_token'})
    fliker = r.json()
    droplet_list = []
    for i in range(len(fliker['fliker'])):
        droplet_list.append(fliker['fliker'][i])
    return droplet_list