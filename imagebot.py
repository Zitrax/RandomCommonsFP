#!/usr/bin/python3
import argparse
import requests
import yaml
from twython import Twython

APP_KEY = 'd2qYJ5oe7Iul5uQhZj0Sdlmin'
APP_SECRET = 'RwrM6iKAmkVJ7A08BXkXQdJXtHa2LEk85ypKFYie65Q8LhEWdP'


def get_auth_url():
    twitter = Twython(APP_KEY, APP_SECRET)
    auth = twitter.get_authentication_tokens()
    OAUTH_TOKEN = auth['oauth_token']
    OAUTH_TOKEN_SECRET = auth['oauth_token_secret']
    return auth['auth_url']


def find_image():
    # First collect a list of all images and dump to disk
    # Further uses can continue from where left off
    payload = {"action": "query", "list": "categorymembers", "cmtype": "file", "format": "json", "continue": "",
               "cmsort": "timestamp", "cmlimit": "100", "cmtitle": "Category:Featured_pictures_on_Wikimedia_Commons"}
    r = requests.get("http://commons.wikimedia.org/w/api.php", params=payload)
    data = r.json()
    if "warnings" in data:
        print("WARNINGS:")
        print(yaml.dump(data["warnings"], default_flow_style=False))
    print(yaml.dump(data["query"]["categorymembers"]))

parser = argparse.ArgumentParser(description='Bot for tweeting featured pictures from wikimedia commons.')
parser.add_argument('--auth_url', action="store_true", help='Retrieve an auth url')
parser.add_argument('--find_image', action="store_true", help='Find a commons image')
args = parser.parse_args()

if args.auth_url:
    print(get_auth_url())
elif args.find_image:
    find_image()