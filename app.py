# -*- coding: utf-8 -*-
"""
Created on Mon May 31 12:25:02 2021

@author: Conor

Bot system that listens for responses
"""


from importlib import reload

import json
import pickle

import apiClass
reload(apiClass)
from apiClass import twtAPI

API = twtAPI()

with open('keys.json') as json_file:
    keys = json.load(json_file)

# Initialize API by providing the needed keys.

API.setKeys(keys)

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
        
        
    def mainLoop(
            self,
        ):
        
        
        
        

if __name__ == '__main__':
    test = twtGame()
    
    







