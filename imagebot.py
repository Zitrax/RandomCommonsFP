#!/usr/bin/python3
import argparse
from twython import Twython

APP_KEY = 'd2qYJ5oe7Iul5uQhZj0Sdlmin'
APP_SECRET = 'RwrM6iKAmkVJ7A08BXkXQdJXtHa2LEk85ypKFYie65Q8LhEWdP'


def get_auth_url():
    twitter = Twython(APP_KEY, APP_SECRET)
    auth = twitter.get_authentication_tokens()
    OAUTH_TOKEN = auth['oauth_token']
    OAUTH_TOKEN_SECRET = auth['oauth_token_secret']
    return auth['auth_url']


parser = argparse.ArgumentParser(description='Bot for tweeting featured pictures from wikimedia commons.')
parser.add_argument('--auth_url', action="store_true", help='Retrieve an auth url')
args = parser.parse_args()

print(args)
