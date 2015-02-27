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


def partial_image_list(cmcontinue=None):
    payload = {"action": "query", "list": "categorymembers", "cmtype": "file", "format": "json", "continue": "",
               "cmsort": "timestamp", "cmlimit": "100", "cmtitle": "Category:Featured_pictures_on_Wikimedia_Commons"}
    if cmcontinue:
        payload["cmcontinue"] = cmcontinue

    headers = {'User-Agent': 'ImageBot/0.1 (daniel@bengtssons.info)'}
    r = requests.get("http://commons.wikimedia.org/w/api.php", params=payload, headers=headers)
    r.raise_for_status()
    data = r.json()
    if "warnings" in data:
        print("WARNINGS:")
        print(yaml.dump(data["warnings"], default_flow_style=False))
    #print(yaml.dump(data, default_flow_style=False))

    if "continue" in data:
        cmcontinue = data["continue"]["cmcontinue"]
    else:
        cmcontinue = None
    print(cmcontinue)
    images = {i["pageid"]: i["title"] for i in data["query"]["categorymembers"]}
    return cmcontinue, images


def find_image():
    # First collect a list of all images and dump to disk
    # Further uses can continue from where left off
    all_images = {}
    cmcontinue, images = partial_image_list()
    while True:
        all_images.update(images)
        if cmcontinue is None or images is None:
            break
        cmcontinue, images = partial_image_list(cmcontinue)
    print(all_images)

parser = argparse.ArgumentParser(description='Bot for tweeting featured pictures from wikimedia commons.')
parser.add_argument('--auth_url', action="store_true", help='Retrieve an auth url')
parser.add_argument('--find_image', action="store_true", help='Find a commons image')
args = parser.parse_args()

if args.auth_url:
    print(get_auth_url())
elif args.find_image:
    find_image()