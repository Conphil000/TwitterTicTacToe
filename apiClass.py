# -*- coding: utf-8 -*-
"""
Created on Sat May 29 14:20:00 2021

@author: Conor

Create the API Class

"""

import json
import tweepy
import sys

class twtAPI:
    """When passed a set of required keys launch an API Instance that handles all Tweepy API related tasks"""
    def __init__(
            self,
        ):
        '''
        Import your Twitter Developer Keys;
    
        I have stored them in a json under the following structure...
    
        json = {
            "APIK": "API Key"
            "SAPIK": "API Secret Key", 
            "BT": "Bearer Token", 
            "AT": "Access Token", 
            "SAT": "Access Token Secret"
        }
        '''
        with open('JSONHelper\keys.json') as json_file:
            keyPayload = json.load(json_file)
        self.__setKeys(keyPayload)
    def __setKeys(
            self,
            keyPayload
        ):
        """
        Define key parameters from keyPayload

        :keyPayload: Dictionary of keys associated with twitter authentication
            {
            "APIK": "API Key"
            "SAPIK": "API Secret Key", 
            "BT": "Bearer Token", 
            "AT": "Access Token", 
            "SAT": "Access Token Secret"
        }
        """
        try:
            self.__apik = keyPayload['APIK']
            self.__sapik = keyPayload['SAPIK']
            self.__at = keyPayload['AT']
            self.__sat = keyPayload['SAT']
            self.__bt = keyPayload['BT']
            try:
                self.__launchAPI()
                # Store some items from the me() method
                # https://docs.tweepy.org/en/latest/api.html

                self.__user = self.__API.me().screen_name
                self.__userID = self.__API.me().id
            except:
                # If Tweepy is unable to connect to your account,
                # throw an error.
                print('Unable to connect to API.')
                return
        except:
            # If all keys are not provided in the keyPayLoad,
            # throw an error.
            print('Unable to unpack Payload.')
            return 

    def __launchAPI(
            self,
        ):
        """
        Connect to Twitter API using Tweepy
        """
        # Use Tweepy documentation to handle authentication
        # https://docs.tweepy.org/en/latest/getting_started.html

        auth = tweepy.OAuthHandler(
            self.__apik,
            self.__sapik
        )
        
        auth.set_access_token(
            self.__at,
            self.__sat
        )
        
        self.__API = \
            tweepy.API(
                auth,
                wait_on_rate_limit =True,
                wait_on_rate_limit_notify=(True)
            )
    def __getLastPost(
            self,
        ):
        """
        Get the ID of the last tweet posted by the API/ACCOUNT
        """
        latest = self.__API.user_timeline(user_id = self.__userID,count=1)
        return latest[0].id
    def getRecentMention(self,sinceID = 1, nTweets = 25):
        """
        Get recent tweets sent to the API user
        :sinceID: The earliest tweet you would want to include,
                    normally this is that last handled ID + 1
        :nTweets: This is the number of tweets the method will pull, 
                    balance this number with frequency to satisfy rate limits
        """
        # Rate Limits are a pain in the ASS; most of this project is hacking these limits haha
        # https://developer.twitter.com/en/docs/twitter-api/v1/rate-limits

        responses = self.__API.mentions_timeline(since_id = sinceID, count = nTweets)
        return responses
    def postTweet(
            self,
            twtPayload
        ):
        
        """ 
        Use this function to either post on a timeline or respond to a tweet.
        
        :twtPayload: Dictionary of parameters needed to post on twitter;
            {
            'MSG': 'The message of the tweet',
            'JSON': 'The json of the tweet you are responding too, empty implies timeline post.'
                {
                'UN':'Name of the account who sent the tweet',
                'TID':'ID of the Tweet'
            }
            
        }
        """
        if twtPayload.get('JSON',False) == False:
            # Post tweet to timeline
            try:
                self.__API.update_status(twtPayload['MSG'])
                return self.__getLastPost()
            except:
                return sys.exc_info()
        else:
            # Post tweet in response to another tweet, Include their @Name when referencing.
            try:
                self.__API.update_status(
                    f"@{twtPayload['JSON']['UN']}\n {twtPayload['MSG']}",
                    in_reply_to_status_id = twtPayload['JSON']['ID']
                    )
                return self.__getLastPost()
            except:
                return sys.exc_info()
    def getLastPost(
            self,
        ):
        return self.__getLastPost()
    def checkStatus(
            self,
            ID
        ):
        try:
            self.__API.get_status(ID)
            return False
        except:
            return True
 
    def Me(
            self,
        ):
        print(f'Hi, I am using the @{self.__user} twitter to communicate.')
        return \
            {
            'UN':self.__user,
            'UID':self.__userID
        }
 
if __name__ == '__main__':
    
    apiTest = twtAPI()
    apiTest.Me()


