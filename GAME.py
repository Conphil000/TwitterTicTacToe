# -*- coding: utf-8 -*-
"""
Created on Sat May  7 16:24:51 2022

@author: Conor
"""

from importlib import reload
import json 
import tweepy
import pandas as pd
from flask import jsonify

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

first = True
find_id = pd.DataFrame([i._json for i in api.user_timeline(exclude_replies = True)])
find_id = find_id[find_id['text'] == game_tweet()['MSG']]['id'].iloc[0]

temp = api.user_timeline()
temp = api.user_timeline(max_id = 1372627496341020672)

tdf = pd.DataFrame([i._json for i in temp])
tdf['text'] == game_tweet()['MSG']

def post_game_tweet(api):
    # this way 2 complicated
    try:
        with open('JSONHelper\\activeGame.json') as json_file:
            last_active = json.load(json_file)
        try:
            if len(api.lookup_statuses(id = [last_active['ID']])) == 0:
                raise BaseException('No Tweet found from saved ID')
            print('Tweet ID pulled from Local JSON')
            return [True,last_active['ID']]
        except BaseException:
            print('Tween ID pulled from local JSON no longer exists on twitter, recreating...')
            APIHandling.post_API_tweet(api, game_tweet())
            tid = APIHandling.get_account_last_post(api, APIHandling.get_API_info(api)['id'])['id']
            temp = {'ID':int(tid)}
            with open('JSONHelper\\activeGame.json', 'w') as outfile:
                json.dump(temp,outfile)
            return [True,temp['ID']]
    except FileNotFoundError:
        print('No JSON Found for Game ID...',end= '')
        try:
            APIHandling.post_API_tweet(api, game_tweet()) == 'Twee'
            tid = APIHandling.get_account_last_post(api, APIHandling.get_API_info(api)['id'])['id']
            temp = {'ID':tid}
            with open('JSONHelper\\activeGame.json', 'w') as outfile:
                json.dump(temp, outfile)
            return [True,temp['ID']]
        except tweepy.Forbidden:
            print("A game tweet exists you just don't have the ID Saved.")
            find_id = pd.DataFrame([i._json for i in api.user_timeline(exclude_replies = True)])
            find_id = find_id[find_id['text'] == game_tweet()['MSG']]['id']
            if find_id.shape[0] == 0:
                print('You gotta delete the game tweet yourself.')
                return [False,None]
            else:
                print('Found previous tweet that matches, creating json file')
                find_id = find_id.iloc[0]
                temp = {'ID':int(find_id)}
                with open('JSONHelper\\activeGame.json', 'w') as outfile:
                    json.dump(temp, outfile)
                return [True,temp['ID']]
def respond(payload):
    if payload['test']:
        return False
        
try_post = post_game_tweet(api)

if try_post[0]:
    GID = try_post[1]
    try:
        with open('JSONHelper\\lastSeen.json') as json_file:
            CID = json.load(json_file)
    except FileNotFoundError:
        CID = GID
        
    CID = GID # DELETE ME WHEN DONE WITH THE RIPPER MA GEE
    
    # loop every 15 seconds
    # start loop
    try:
        with open('JSONHelper\\players.json') as json_file:
            players = json.load(json_file)
    except FileNotFoundError:
        players = pd.DataFrame({'obj':[],'current_tweets':[]})
    
    new = pd.DataFrame([i._json for i in APIHandling.get_API_mention(api,since_id = CID)])
    new['screen_name'] = new.apply(lambda x: x['user']['screen_name'],axis = 1)
    new['user_id'] = new.apply(lambda x: x['user']['id'],axis = 1)
    new['game_tweet'] = new.apply(lambda x: 1 if x['in_reply_to_status_id'] == GID else 0,axis = 1)
    
    # Can update screen_names here...
    new_players = new[~new.index.isin(players.index)][['user_id','screen_name','game_tweet']]
    
    new_players = new_players.groupby(by = ['user_id','screen_name']).game_tweet.max().reset_index()
    
    new_players['obj'] = \
        new_players.apply(
            lambda x: 
                PLAYERHandling.PLAYER(
                    x.user_id,
                    x.screen_name
                ) if x.game_tweet == 1 else None,
            axis = 1
        )
            
    new_players.set_index('user_id',inplace = True)
    players = players.append(new_players[['obj']])
    
    new.sort_values(by = ['user_id','created_at'],inplace = True)
    new.set_index('user_id',inplace = True)
    
    players['current_tweets'] = players.apply(lambda x: new.loc[[x.name]],axis = 1)
    
    CID = new['id'].max()
    
    x = players.sample(1).squeeze()
    
    def response(x,GID):
        obj = x['obj']
        tweets = x['current_tweets']
        
        if obj == None:
            print('u dont have an active game and are not talking to correct tweet!')
        else:
            if isinstance(tweets,pd.DataFrame):    
                print('Found a tweet!')
            else:
                print('u inactive')
        
        
        return x['obj']
    
    players['obj'] = players.apply(lambda x: response(x,GID),axis = 1)
    
    1/0
    
    players = players[~players['obj'].isnull()]
    players['current_tweets'] = None
    
    with open('JSONHelper\\lastSeen.json', 'w') as outfile:
        json.dump(int(CID), outfile)
        
    with open('JSONHelper\\players.json', 'w') as outfile:
        json.dump(players, outfile)
        
    def response(x,GID,players):
        print(x)
        overwrite = 'No'
        p = {}
        if players.get(x.name,None) == None:
            # No active game
            if x.in_reply_to_status_id == GID:
                # Responding to the game tweet.
                tweet = x.text.split(' ')[1]
                if tweet.isnumeric() and len(tweet) == 1 and int(tweet) != 0:
                    # Tweet has valid number in it
                    print('Creating a player for',x.name)
                    p = PLAYERHandling.PLAYER(x.user['id'], x.user['screen_name'])
                    overwrite = 'Append'
                else:
                    # Tweet does not have a number in it
                    print(NotImplementedError("Can't handle non-numeric, len>1, or 0 inputs."))
            else:
                # Tweet is not in response to the game tweet.
                print(NotImplementedError("Can't handle tweets outside of the game."))   
        else:
            print('Existing Player')
            print(NotImplementedError("Can't handle existing players."))
            p = {}
            # Need to make sure they responded to the correct tweet
            overwrite = 'Yes'
        return [p,overwrite]
    
    new[['obj','overwrite']] = new.apply(lambda x: response(x,GID,players),result_type = 'expand',axis = 1)
    
    players = players.append(new[new['overwrite']=='Append'][['obj']])
    players = new[new['overwrite'] == 'Yes'].index.apply(lambda x: x,axis = 1)
    
    
    
        
