import requests
import json
from tag import tags

giphy_key = json.load(open('config.json', 'r'))['giphyKey']

def surprise():
    response = requests.get(f'http://api.giphy.com/v1/gifs/random?tag={tags["surprise"]}&lang=en&api_key={giphy_key}')
    response = response.json()
    return response['data']['url']

def fun_times():
    response = requests.get(f'http://api.giphy.com/v1/gifs/random?tag={tags["funtimes"]}&lang=en&api_key={giphy_key}')
    response = response.json()
    return response['data']['url']