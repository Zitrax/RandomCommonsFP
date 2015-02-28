#!/usr/bin/python3
import argparse
import json
import random
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

    if "continue" in data:
        cmcontinue = data["continue"]["cmcontinue"]
    else:
        cmcontinue = None
    print(cmcontinue)
    images = {i["pageid"]: i["title"] for i in data["query"]["categorymembers"]}
    return cmcontinue, images


def find_all_images():
    # First collect a list of all images and dump to disk
    # Further uses can continue from where left off
    all_images = {}
    cmcontinue, images = partial_image_list()
    while True:
        all_images.update(images)
        if cmcontinue is None or images is None:
            break
        cmcontinue, images = partial_image_list(cmcontinue)
    with open('images.json', 'w') as f:
        f.write(json.dumps(all_images))
    return all_images


def load_images():
    with open('images.json', 'r') as f:
        return json.loads(f.read())


parser = argparse.ArgumentParser(description='Bot for tweeting featured pictures from wikimedia commons.')
parser.add_argument('--auth_url', action="store_true", help='Retrieve an auth url')
parser.add_argument('--find_all_images', action="store_true", help='Retrieve the list of all images')
parser.add_argument('--load_images', action="store_true", help='Load previously stored images')
args = parser.parse_args()

if args.auth_url:
    print(get_auth_url())
elif args.find_all_images:
    find_all_images()
elif args.load_images:
    images = load_images()
    image_id = random.choice(list(images.keys()))
    print(images[image_id])