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

functionServer = {
    'respond':'dbo.response'
    }  


def funcReport(func):
    '''Decorator that reports the execution time and how tweet was handled.'''
  
    def wrap(*args, **kwargs):

        inputs = args[1]
        
        start = time.time()
        try:
            result = func(*args, **kwargs)
        except:
            result = 'error'
            
        end = time.time()
        
        sqlServer = functionServer.get(func.__name__,'unhandled')
        
        
        file_object = open(r'SQLHelper//sql.txt','a')
        file_object.write(str({'sqlTable':sqlServer,'Function':func.__name__,'data':{'Inputs':inputs,'Output':result,'Time':(end-start)}})+'\n')
        file_object.close()
        
        return result
    return wrap

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
        
        self.__players = {}
        
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
                ### If tweet no longer exists, force exception
                1/0
            try:
                with open('JSONHelper//lastHandled.json') as json_file:
                    self.__sinceID = json.load(json_file)['SID']
            except:
                self.__sinceID = API.getLastPost() + 1
                
            print('LIVE')
        except:
            try:
                storeTWT = {'ID':API.postTweet({'MSG':'TESTY TESTER'})}
                self.__gameTweet = storeTWT['ID']
                with open('JSONHelper//activeGame.json','w') as outfile:
                    json.dump(storeTWT, outfile)
                self.__sinceID = self.__gameTweet + 1
                print('NEW')
            except:
                ### Tweet already exists so you will need to kill it
                print('MANUALLY DELETE PREVIOUS TWEET BEFORE LAUNCHING...')
                self.kill()
                
        while self.__active:
            
            new = API.getRecentMention(self.__sinceID)
            
            list(map(lambda x: self.handle(x),reversed(new)))
            
            lastID = {'SID':self.__sinceID}
            
            with open('JSONHelper//lastHandled.json','w') as outfile:
                json.dump(lastID, outfile)
            
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
        try:    
            response = self.respond(twtJSON)
        except:
            pass
        
    @funcReport
    def respond(
            self,
            payload
        ):
        if payload['rid'] == self.__gameTweet and self.__players.get(payload['@'],True)==True:
            pass
        elif payload['rid']:
            pass
            
        return {'Decision':'GOOD'}


if __name__ == '__main__':
    twtGame()
    
    







