# -*- coding: utf-8 -*-
"""
Created on Sat May  7 16:24:51 2022

@author: Conor
"""

from importlib import reload
import json 
import tweepy
import pandas as pd

import APIHandling
reload(APIHandling)
import APIHandling

import PLAYERHandling
reload(PLAYERHandling)
import PLAYERHandling

with open('JSONHelper\keys.json') as json_file:
    twtKeys = json.load(json_file)
    
api = \
    APIHandling.get_API_connection(
        twtKeys['APIK'],
        twtKeys['SAPIK'],
        twtKeys['AT'],
        twtKeys['SAT']
    )

account_id = APIHandling.get_API_info(api)['id']

def game_tweet():
    return {'MSG':'Respond to this tweet with a number 1-9 to play, you are X.'}

temp = api.user_timeline(excludes_replies)
tdf = pd.DataFrame([i._json for i in temp])
tdf['text'] == game_tweet()['MSG']


def post_game_tweet(api):
    try:
        with open('JSONHelper\\activeGame.json') as json_file:
            last_active = json.load(json_file)
        try:
            api.lookup_statuses(id = [last_active['ID']])
        except :
            pass
        # Check if still exists.
    except FileNotFoundError:
        print('No JSON Found for Game ID...',end= '')
        try:
            APIHandling.post_API_tweet(api, game_tweet())
        except tweepy.Forbidden:
            print("A game tweet exists you just don't have the ID Saved.")
            # Delete the tweet and post again
        





