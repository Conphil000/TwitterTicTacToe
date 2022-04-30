# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 15:25:29 2022

@author: Conor
"""


# You need to have a JSON saved in the JSONHelper folder with the following:
    
    
import json
import tweepy
import sys

class TWEEPY_API:
    def __init__(
            self,
        ):
        print('Creating Tweepy API Object Instance;',end = ' ')
        self.local_keys()
        self.connect_API()
        
        self.me = \
            self.__API.get_user(
                screen_name = \
                    self.__API.get_settings()['screen_name']
            )
                
        self.__user = self.me._json['screen_name']
        self.__id = self.me._json['id']

        print('Success.')
    def local_keys(
            self,
        ):
        try:
            with open('JSONHelper\keys.json') as json_file:
                keyPayload = json.load(json_file)
            try:
                self.__apik = keyPayload['APIK']
                self.__sapik = keyPayload['SAPIK']
                self.__at = keyPayload['AT']
                self.__sat = keyPayload['SAT']
                self.__bt = keyPayload['BT']
            except ValueError:
                print('Dictionary keys are not correct.')
        except FileNotFoundError:
            print('Cant find JSONHelper\keys.json')
    def connect_API(
            self,
        ):
        auth = tweepy.OAuth1UserHandler(
            self.__apik,
            self.__sapik,
            self.__at,
            self.__sat
        )

        self.__API = \
            tweepy.API(
                auth,
                wait_on_rate_limit =  True
            )
    def GET_me(
            self,
        ):
        print(f'Hi, I am using the @{self.__user} twitter to communicate.')
        return \
            {'UN':self.__user}
if __name__ == '__main__':
    API_CURSOR = TWEEPY_API()
    API_CURSOR.local_keys()
    API_CURSOR.GET_me()




