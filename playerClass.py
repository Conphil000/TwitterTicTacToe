# -*- coding: utf-8 -*-
"""
Created on Sun Jun  6 11:02:39 2021

@author: Conor
"""


from dataclasses import dataclass, field
import random
        
@dataclass
class game:
    __board: str = field(default = '123456789')
    __player: list = field(default_factory=lambda: [])
    __computer: list = field(default_factory=lambda: [])
    __turn: bool = True
    def makeMove(
            self,
            move,
        ):
        if isinstance(move, (str,int)):
            move = str(move)
            if len(move) == 1:
                if (str(move) in self.__board):
                    self.__board = self.__board.replace(move,'')
                    self._flipTurn()
                    if self.__turn:
                        self.__computer.append(move)
                    else:
                        self.__player.append(move)
                        self._computerMove()
                    
                    return True
                else:
                    print('Move {} not found.'.format(str(move)))
                    return False
            else: 
                raise ValueError('No reason for the length of the move to be anything except 1.')
        else:
            raise ValueError('No reason for the move to be anything but int or str.')
    def getBoard(
            self,
        ):
        return self.__board
    def getPlayerCharacter(
            self,
        ):
        return player.playerCharacter
    def getComputerCharacter(
            self,
        ):
        return player.computerCharacter
    def getBoardString(
            self,
        ):
        pass
    def currentTurn(
            self,
        ):
        # True, Players turn
        # False, Computers turn
        return self.__turn
    def _computerMove(
            self,
        ):
        if self.__turn == False:
            self.makeMove(random.choice(self.__board.replace()))
        else:
            print("ERROR: Not the computer's turn.")
    def _flipTurn(
            self,
        ):
        self.__turn = not self.__turn

@dataclass
class player:
    """class for keeping track of player stats"""
    playerCharacter: str = field(default = 'X')
    computerCharacter: str = field(default = 'O')
    score: list = field(default_factory=lambda: [0,0])
    def __init__(
            self,
        ):
        self.Game = game()
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
                    self.playerCharacter = newCharacter
                else:
                    self.computerCharacter = newCharacter
            else:
                return ValueError('The length of the newCharacter must be 1.')
        else:
            return ValueError('You must change to a string.')

if __name__ == '__main__':
           
   tweet = {'id':1234,'str':'3',}
   players = {}
   players[tweet['id']] = player()
   
   print(players[tweet['id']].Game.getComputerCharacter())
   newPlayer.updateCharacter('Z')
   print(players[tweet['id']].Game.getComputerCharacter())

   for i in range(3):
       newGame.makeMove(random.choice(newGame.getBoard()))
       
   board = newGame.returnBoard()

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