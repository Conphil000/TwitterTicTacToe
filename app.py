# -*- coding: utf-8 -*-
"""
Created on Mon May 31 12:25:02 2021

@author: Conor

Bot system that listens for responses
"""


from importlib import reload

import json
import pickle
import time

import apiClass
reload(apiClass)
from apiClass import twtAPI

API = twtAPI()
def heartbeat():
    print('boink...')
heartbeat()
class twtGame:
    def __init__(
            self,
            timeInterval = 15
        ):
        """
        On initialize, specifiy some constants like interval responses are checked.
        
        :timeInterval: The time (s) between checking responses on the game tweet.
        
        """
        
        twtInfo = API.Me()
        self.__un = twtInfo['UN']
        self.__uid = twtInfo['UID']
        
        self.__intMain = timeInterval
        self.__active = True
        self.__currentID = 0
        
        self.mainLoop()
        
    def kill(
            self,
        ):
        self.__active = False
    def mainLoop(
            self,
        ):
        
        try:
            with open('JSONHelper//activeGame.json') as json_file:
                self.__gameTweet = json.load(json_file)['ID']
            if API.checkStatus(self.__gameTweet):
                1/0
            print('LIVE')
        except:
            try:
                storeTWT = {'ID':API.postTweet({'MSG':'TESTY TESTER'})}
                self.__gameTweet = storeTWT['ID']
                with open('JSONHelper//activeGame.json','w') as outfile:
                    json.dump(storeTWT, outfile)
                print('NEW')
            except:
                ### Tweet already exists so you will need to kill it
                print('MANUALLY DELETE PREVIOUS TWEET BEFORE LAUNCHING...')
                self.kill()
                
        self.__sinceID = self.__gameTweet + 1
        
        while self.__active:
            
            new = API.getRecentMention(self.__sinceID)
            
            list(map(lambda x: self.handle(x),reversed(new)))
            
            time.sleep(self.__intMain)
            heartbeat()
            self.kill()
    def handle(
            self,
            payload
        ):
        twtJSON = {
            'text':payload._json['text'].replace(f'@{self.__un}','').replace(' ',''),
            'id':payload._json['id'],
            'rid':payload._json['in_reply_to_status_id'],
            '@':'@'+payload._json['user']['screen_name']
            }
        self.__sinceID = twtJSON['id'] + 1
        print(twtJSON)
        
        
            
        
    
    
        
        
        
        

if __name__ == '__main__':
    twtGame()
    
    







