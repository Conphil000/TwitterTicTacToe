# -*- coding: utf-8 -*-
"""
Created on Sat May  7 12:16:50 2022

@author: Conor
"""
import itertools

def check_win(moves):
    wins = {'123':'horizontal','456':'horizontal','789':'horizontal','147':'vertical','258':'vertical','369':'vertical','159':'diagnonal','357':'diagnonal'}
    ordered_moves = [str(i) for i in list(range(1,10)) if str(i) in moves]
    
    for i in itertools.combinations(ordered_moves,3):
        pos = ''.join(i)
        if wins.get(pos,None) != None:
            return [True,wins[pos]]
    return [False,None]

class twitter_user:
    def __init__(self,uid):
        
        self.__uid = uid
        
        self.__player_char = 'X'
        self.__computer_char = 'O'
        
        self.__score = [0,0,0]
        self.__difficulty = 0.3
        self.__board = []
        self.__age = 0
        
        self.__active = False
    
    def new_game(self,):
        self.__board = ''.join([str(i) for i in range(1,10)])
        self.__player_moves = []
        self.__computer_moves = []  
        self._reset_age()
    def available_moves(self,):
        return [int(i) for i in self.__board]
    # Control Difficulty
    def __update_difficulty(self,delta):
        self.__difficulty += delta
        if self.__difficulty > 1:
            self.__difficulty = 1
        if self.__difficulty < 0:
            self.__difficulty = 0
    # Control Score
    def win(self,):
        self.__score[0] += 1
        self.__score[1] += 1
        self._update_difficulty(0.1)
    def loss(self,):
        self.__score[0] += 1
        self._update_difficulty(-0.1)
    def tie(self,):
        self.__score[0] += 1
        self.__score[2] += 1
        self._update_difficulty(-0.05)
        
    # Control Moves
    def _make_move(
            self,
            move
        ):
        if int(move) in self.available_moves():
            self.__board = self.__board.replace(str(move),'')
        else:
            raise BaseException('Move Not Available')
    def player_move(self,move):
        self._make_move(move)
        self.__player_moves.append(str(move))
        return check_win(self.__player_moves)
    def computer_move(self,move):
        self._make_move(move)
        self.__computer_moves.append(str(move))
        return check_win(self.__computer_moves)
    # Control Age
    def _reset_age(self,):
        self.__age_last_valid_move = 0
    def get_old(self,):
        self.__age_last_valid_move += 1
    def current_age(self,):
        return self.__age_last_valid_move
    # Show Board
    def current_board_str(self,):
        scroll = 0
        groups = []
        c_board = ''.join([str(i) for i in range(1,10)])
        for i in self.__player_moves:
            c_board = c_board.replace(i,self.__player_char)
        for i in self.__computer_moves:
            c_board = c_board.replace(i,self.__computer_char)
        for i in [3,6,9]:
            slicer = c_board[scroll:i]
            groups.append(f'{slicer[0]} |  {slicer[1]}  | {slicer[2]}')
            scroll += 3
            
        return '\n- + - + -\n'.join(groups)
    # data for game
    def set_correct_response_id(self,nid):
        self.__looking_for = nid
    def get_correct_response_id(self,):
        return self.__looking_for
    def flip_active(self,):
        return False if self.__active == True else True
   
if __name__ == '__main__':
    players = {'123':twitter_user(123)}
    players['123'].new_game()
    players['123'].available_moves()
    players['123'].player_move(1)
    players['123'].computer_move(3)
    players['123'].computer_move(6)
    players['123'].computer_move(9)
    print(players['123'].current_board_str())

    print('age:',players['123'].current_age())
    players['123'].get_old()
    players['123'].get_old()
    print('age:',players['123'].current_age())
    players['123'].new_game()
    print(players['123'].current_board_str())
    print('age:',players['123'].current_age())
    
    
