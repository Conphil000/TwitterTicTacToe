# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 15:25:29 2022

@author: Conor
"""

# You need to have a JSON saved in the JSONHelper folder with the following:
    
    
import json
import tweepy
import sys
        
def get_API_connection(
        api_key,
        secret_api_key,
        access_token,
        secret_access_token
    ):
    auth = \
        tweepy.OAuth1UserHandler(
            api_key,
            secret_api_key,
            access_token,
            secret_access_token
        )
        
    return \
        tweepy.API(
            auth,
            wait_on_rate_limit =  True
        )
def get_API_info(
        api
    ):
    return \
        api.get_user(
            screen_name = api.get_settings()['screen_name']
        )._json

def get_API_introduction(
        api
    ):
    info = get_API_info(api)
    print(f"Hi, I am using the @{info['screen_name']} twitter to communicate.")

def get_account_posts(
        api,
        user_id,
        screen_name = None
    ):
    """Get the last 20 posts made by user_id"""
    if screen_name != None:
        d = NotImplementedError
    else:
        d = api.user_timeline(user_id = user_id)
    return d

def get_account_last_post(
        api,
        user_id,
        screen_name = None
    ):
    """Get data from the last post this account has made"""
    return get_account_posts(api, user_id, screen_name)[0]._json

def get_API_mention(
        api,
        since_id = None,
        max_id = None,
        count = 20
    ):
    """
    Get recent tweets sent to the API user
    :sinceID: The earliest tweet you would want to include,
                normally this is that last handled ID + 1
    :nTweets: This is the number of tweets the method will pull, 
                balance this number with frequency to satisfy rate limits
    """
    # Rate Limits are a pain in the ASS; most of this project is hacking these limits haha
    # https://developer.twitter.com/en/docs/twitter-api/v1/rate-limits
    return api.mentions_timeline(count = count,since_id = since_id,max_id = max_id)

def post_API_tweet(
        api,
        payload
    ):
    
    # Tweets will either be to the timeline or in response to someone
    """
    payload should look like:
        {
        'MSG' : 'This is what i want to say',
        'TO' : {'id':'ID of the tweet','sreen_name':'screen_name of author of TID'}
        }
    """
    if payload.get('TO',None) == None:
        api.update_status(
            payload['MSG']
        )
    else:
        api.update_status(
            f"@{payload['TO']['screen_name']} {payload['MSG']}",
            in_reply_to_status_id = payload['TO']['id']
        )
        
if __name__ == '__main__':
    with open('JSONHelper\keys.json') as json_file:
        twtKeys = json.load(json_file)
        
    api = \
        get_API_connection(
            twtKeys['APIK'],
            twtKeys['SAPIK'],
            twtKeys['AT'],
            twtKeys['SAT']
        )
        
    info = get_API_info(api)
    get_API_introduction(api)
    t = get_account_last_post(api,info['id'])
    post_API_tweet(api,{'MSG':'TEST: post to timeline'})
    lp = get_account_last_post(api, info['id'])
    payload = {'MSG':'TEST: respond to post on timeline','TO':{'id':lp['id'],'screen_name':lp['user']['screen_name']}}
    post_API_tweet(api,payload)



