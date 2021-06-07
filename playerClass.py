# -*- coding: utf-8 -*-
"""
Created on Sun Jun  6 11:02:39 2021

@author: Conor
"""
import itertools

class twtPlayer:
    player = 'X'
    computer = 'O'
    board = '1 |  2  | 3\n- + - + -\n4 |  5  | 6\n- + - + -\n7 |  8  | 9'
    def __init__(
            self,
        ):

        self.__score = [0,0,0]
        self.resetGame()
        
    def resetGame(
            self
        ):
        self.__availableMoves = [1,2,3,
                                 4,5,6,
                                 7,8,9]
        self.__playerMoves = []
        self.__computerMoves = []
        
        def newDifficulty(score):
            if score[0] == score[1]:
                return 0.30
            if score[0] > score[1]:
                return 0.75
            if score[1] > score[0]:
                return 0.10
            return 0.4
        
        self.__diff = newDifficulty(self.__score)
            
    def checkRID(
            self,
            RID
        ):
        '''
        Check if the player responded to the correct tweet
        :RID: in_reply_to_tweet of json in question...
        '''
        if RID == self.__RID:
            return True
        return False
    def updateRID(
            self,
            RID
        ):
        '''
        If the player made a valid move update the RID to look for
        :RID: id of response to last move
        '''
        self.__RID = RID
    def checkWin(
            self,
            moves
        ):
        """
        Check to see if someone has a winning hand

        :moves: What moves has the player made in the current game
        """
        wins = ['123','456','789','147','258','369','159','357']
        winDef = {'123':'horizontal','456':'horizontal','789':'horizontal','147':'vertical','258':'vertical','369':'vertical','159':'diagnonal','357':'diagnonal'}
        # See if any combination of the moves provided matches a win.
        ordered_moves = [i for i in ['1','2','3','4','5','6','7','8','9'] if i in moves]
        for i in itertools.combinations(ordered_moves,3):
            if ''.join(i) in wins:
                return [True,winDef[''.join(i)]]

        # If no winner and no moves left then tie
        if len(self.availableMoves) == 0:
            return 'tie'

        # No winner
        return [False,None]