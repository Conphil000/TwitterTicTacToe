# -*- coding: utf-8 -*-
"""
Created on Sat May  7 16:24:51 2022

@author: Conor
"""

from importlib import reload
import json 
import tweepy
import pandas as pd
import random

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
        players = pd.DataFrame({'obj':[]})
    
    new = pd.DataFrame([i._json for i in APIHandling.get_API_mention(api,since_id = CID)])
    
    new['screen_name'] = new.apply(lambda x: x['user']['screen_name'],axis = 1)
    new['user_id'] = new.apply(lambda x: x['user']['id'],axis = 1)
    new['player'] = new.apply(lambda x: players.get(x.user_id,None),axis = 1)
    
    new.sort_values(by = ['user_id','created_at'],inplace = True)
    # Can update screen_names here...
    # new_players = new[~new.index.isin(players.index)][['user_id','screen_name','game_tweet']]
    
    # new_players = new_players.groupby(by = ['user_id','screen_name']).game_tweet.max().reset_index()
    
    # new_players['obj'] = \
    #     new_players.apply(
    #         lambda x: 
    #             PLAYERHandling.twitter_user(
    #                 x.user_id
    #             ) if x.game_tweet == 1 else None,
    #         axis = 1
    #     )
            
    # new_players.set_index('user_id',inplace = True)
    # players = players.append(new_players[['obj']])
    
    
    # new.set_index('user_id',inplace = True)
    
    # players['current_tweets'] = players.apply(lambda x: new.loc[[x.name]],axis = 1)
    
    # CID = new['id'].max()
    
    x = new.iloc[1].squeeze()
    
    def response(x,GID,api,apiID):
        player = x['player']
        
        uid = x['user_id']
        rid = x['in_reply_to_status_id']
        tid = x['id']
        screen_name = x['screen_name']
        
        text = x['text']
        tweet = text.split(' ')[1]
        if player == None:
            if rid == GID:
                if tweet.isnumeric() and len(tweet) == 1 and int(tweet) != 0:
                    print('Create a player and a game.')
                    player = PLAYERHandling.PLAYER(uid)
                    player.new_game()
                    player.player_move(tweet)
                    player.computer_move(random.choice(player.available_moves()))
                    payload =\
                        {
                        'MSG':player.current_board_str(),
                        'TO':{'id':tid,'screen_name':screen_name}
                    }
                    APIHandling.post_API_tweet(api, payload)
                    player.set_correct_response_id(APIHandling.get_account_last_post(api, account_id)['id'])
                else:
                    payload =\
                        {
                        'MSG':'Please use a number between 1-9.',
                        'TO':{'id':tid,'screen_name':screen_name}
                    }
                    APIHandling.post_API_tweet(api, payload)
            else:
                payload =\
                        {
                        'MSG':"idk dude/dudette i'd respond to the game tweet.",
                        'TO':{'id':tid,'screen_name':screen_name}
                    }
                APIHandling.post_API_tweet(api, payload)
        else:
            if rid == player.get_correct_response_id():
                if tweet.isnumeric() and len(tweet) == 1 and int(tweet) != 0:
                    if text in player.available_moves():
                        if player.player_move(tweet):
                            print('player wins')
                            player.win()
                            player.new_game()
                            payload =\
                                {
                                'MSG':'You Won!',
                                'TO':{'id':tid,'screen_name':screen_name}
                            }
                            APIHandling.post_API_tweet(api, payload)
                            player.set_correct_response_id(GID)
                        else:
                            if player.computer_move(random.choice(player.available_moves())):
                                print('computer wins')
                                player.loss()
                                player.new_game()
                                payload =\
                                    {
                                    'MSG':'You Lost!',
                                    'TO':{'id':tid,'screen_name':screen_name}
                                }
                                APIHandling.post_API_tweet(api, payload)
                                player.set_correct_response_id(GID)
                            else:
                                if len(player.available_moves()) == 0:
                                    player.tie()
                                    player.new_game()
                                    payload =\
                                        {
                                        'MSG':'We Tied!',
                                        'TO':{'id':tid,'screen_name':screen_name}
                                    }
                                    APIHandling.post_API_tweet(api, payload)
                                    player.set_correct_response_id(GID)
                                else:
                                    payload =\
                                        {
                                        'MSG':player.current_board_str(),
                                        'TO':{'id':tid,'screen_name':screen_name}
                                    }
                                    APIHandling.post_API_tweet(api, payload)
                                    player.set_correct_response_id(APIHandling.get_account_last_post(api, account_id)['id'])
                    else:
                        payload =\
                            {
                            'MSG':'Move not available.',
                            'TO':{'id':tid,'screen_name':screen_name}
                        }
                        APIHandling.post_API_tweet(api, payload)
                else:
                    payload =\
                        {
                        'MSG':'Not a valid move.',
                        'TO':{'id':tid,'screen_name':screen_name}
                    }
                    APIHandling.post_API_tweet(api, payload)
                
            else:
                payload =\
                    {
                    'MSG':'You responded to the wrong tweet.',
                    'TO':{'id':tid,'screen_name':screen_name}
                }
                APIHandling.post_API_tweet(api, payload)
        return player
    
    new['player'] = new.apply(lambda x: response(x,GID,api,account_id),axis = 1)
    
    temp_players = new[~new['player'].isnull()]
    temp_players = temp_players[temp_players.id.isin(temp_players.groupby(by = 'user_id')['id'].max().to_list())][['user_id','player']].set_index('user_id').to_dict()['player']
    
    for k,d in temp_players.items():
        if k in players.index:
            players.loc[k,'obj'] = d
        else:
            players = players.append(pd.DataFrame({'obj':[d]},index = [k]))
    
    1/0
    
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
    
    
    
        
