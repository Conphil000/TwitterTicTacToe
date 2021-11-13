# -*- coding: utf-8 -*-
"""
Created on Sun Jun  6 11:02:39 2021

@author: Conor
"""

import numpy as np
import random

class game:
    _shared_state = {}
    def __init__(
            self,
        ):
        self.__dict__ = self._shared_state
        self.__resetGame()
    def __resetGame(
            self,
        ):
        self.__player = []
        self.__computer = []
        self.__board = '123456789'
    def makeMove(
            self,
            move,
        ):
        if isinstance(move, (str,int)):
            move = str(move)
            if len(move) == 1:
                if (str(move) in self.__board):
                    self.__board = self.__board.replace(move,'')
                    self.__player.append(move)
                    winner = self._checkWinner()
                    if winner != None:
                        if winner == 'Tied':
                            print('We Tied')
                            return False
                        print(f'Player Wins {winner}')
                        return False
                    else:
                        self.__computerMove()
                        winner = self._checkWinner()
                        if winner != None:
                            if winner == 'Tied':
                                print('We Tied')
                                return False
                            print(f'Player Wins {winner}')
                            return False
                    return True
                else:
                    print('Move {} not found.'.format(str(move)))
                    return False
            else: 
                raise ValueError('No reason for the length of the move to be anything except 1.')
        else:
            raise ValueError('No reason for the move to be anything but int or str.')
    def _currentMoves(
            self,
        ):
        return self.__board
    def _checkWinner(
            self,
        ):
        board = self._currentBoard()
        for i in range(3): 
            row = list(set(board[i*3:(i+1)*3]))
            if len(row) == 1: # Check if Horizontal Winner
                return 'Horizontally'
            row = list(set(board[i]+board[i+3]+board[i+6]))
            if len(row) == 1: # Check if Verical Winner
                return 'Vertically'
        d1 = list(set(board[0]+board[4]+board[8])) # Check First Diagonal
        d2 = list(set(board[2]+board[4]+board[6])) # Check Second Diagonal
        if (len(d1) == 1) or (len(d2) == 1):
            return 'Diagonally'
        if len(self._currentMoves()) == 0:
            return 'Tied'
        return None
        
    def _currentBoard(
            self,
        ):
        board = '123456789'
        for i in self.__player:
            board = board.replace(i,self.__playerCharacter)
        for i in self.__computer:
            board = board.replace(i,self.__computerCharacter)
        return board
    def getBoardString(
            self,
        ):
        string = []
        board = self._currentBoard()
        for i in range(3):
            string.append(' | '.join([i for i in board[i*3:(i+1)*3]]))
            if i != 2:
                string.append('- + - + -')
        return '\n'.join(string)
    def __computerMove(
            self,
        ):
        
        choice = random.choice(self._currentMoves())
        self.__computer.append(choice)
    

class player(game):
    """class for keeping track of player stats"""
    def __init__(
            self,
        ):
        self.__playerCharacter = 'X'
        self.__computerCharacter = 'O'
        self.__score = [0,0,0]
        game.__init__(self)
    def currentScore(
            self,
        ):
        return self.__score
    def startGame(
            self,
        ):
        print('Starting a new game for ')
        pass
    def updateCharacter(
            self,
            newCharacter,
            player = True
        ):
        if isinstance(newCharacter,(str)):
            if len(newCharacter) == 1:
                if player:
                    self.__playerCharacter = newCharacter
                else:
                    self.__computerCharacter = newCharacter
            else:
                return ValueError('The length of the newCharacter must be 1.')
        else:
            return ValueError('You must change to a string.')


if __name__ == '__main__':
    countWins = {}
    tweet = {'id':1234,'str':'3',}
    players = {}
    players[tweet['id']] = player()
    
    for i in range(100):
        
        # print(players[tweet['id']].getBoardString())
        while players[tweet['id']].makeMove(random.choice(players[tweet['id']]._currentMoves())):
            print('turn')
        # print(players[tweet['id']].getBoardString())
        players[tweet['id']].makeMove(random.choice(players[tweet['id']]._currentMoves()))
        print(players[tweet['id']].getBoardString())
        
        if players[tweet['id']].checkWinner() in countWins:
            countWins[players[tweet['id']].checkWinner()] += 1
        else:
            countWins[players[tweet['id']].checkWinner()] = 1
        

   
# class Parent(object): #This is a Borg class
#     __shared_state = {}

#     def __init__(self):
#         self.__dict__ = self.__shared_state
#         self.valueA = 5


# class Child(Parent):
#     def __init__(self):
#         Parent.__init__(self)
#         self.valueB = 10

#     def Calculate(self):
#         self.result = self.valueB + self.valueA
#         print(self.result)


# class MainProgram():
#     def __init__(self):
#         self.parent = Parent()
#         self.child = Child()

#         self.parent.valueA = 8

#         self.child.Calculate()

# foobar=MainProgram()




   # np = player(tweet['id'])
   # np.startGame()
    
# 1/0


# import itertools

# class twtPlayer:
#     player = 'X'
#     computer = 'O'
#     board = '1 |  2  | 3\n- + - + -\n4 |  5  | 6\n- + - + -\n7 |  8  | 9'
#     def __init__(
#             self,
#         ):

#         self.__score = [0,0,0]
#         self.resetGame()
        
#     def resetGame(
#             self
#         ):
#         self.__availableMoves = [1,2,3,
#                                  4,5,6,
#                                  7,8,9]
#         self.__playerMoves = []
#         self.__computerMoves = []
        
#         def newDifficulty(score):
#             if score[0] == score[1]:
#                 return 0.30
#             if score[0] > score[1]:
#                 return 0.75
#             if score[1] > score[0]:
#                 return 0.10
#             return 0.4
        
#         self.__diff = newDifficulty(self.__score)
            
#     def checkRID(
#             self,
#             RID
#         ):
#         '''
#         Check if the player responded to the correct tweet
#         :RID: in_reply_to_tweet of json in question...
#         '''
#         if RID == self.__RID:
#             return True
#         return False
#     def updateRID(
#             self,
#             RID
#         ):
#         '''
#         If the player made a valid move update the RID to look for
#         :RID: id of response to last move
#         '''
#         self.__RID = RID
#     def checkWin(
#             self,
#             moves
#         ):
#         """
#         Check to see if someone has a winning hand

#         :moves: What moves has the player made in the current game
#         """
#         wins = ['123','456','789','147','258','369','159','357']
#         winDef = {'123':'horizontal','456':'horizontal','789':'horizontal','147':'vertical','258':'vertical','369':'vertical','159':'diagnonal','357':'diagnonal'}
#         # See if any combination of the moves provided matches a win.
#         ordered_moves = [i for i in ['1','2','3','4','5','6','7','8','9'] if i in moves]
#         for i in itertools.combinations(ordered_moves,3):
#             if ''.join(i) in wins:
#                 return [True,winDef[''.join(i)]]

#         # If no winner and no moves left then tie
#         if len(self.availableMoves) == 0:
#             return 'tie'

#         # No winner
#         return [False,None]