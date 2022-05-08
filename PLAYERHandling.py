# -*- coding: utf-8 -*-
"""
Created on Sat May  7 12:16:50 2022

@author: Conor
"""
import itertools

class PLAYER:
    def __init__(self, id, screen_name):
        self.__id = id,
        self.__screen_name = screen_name
        self.__player_char = 'X'
        self.__computer_char = 'O'
        # [# Games, # Wins, # Ties]
        self.__score = [0,0,0]
        self.__difficulty = 0.5
        self.reset_board()
        
    def update_screen_name(self,api):
        # someone could change their screen_name mid game :O
        return NotImplementedError
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
    def reset_board(self,):
        self.__board = ''.join([str(i) for i in range(1,10)])
        self.__player_moves = []
        self.__computer_moves = []  
        self._reset_age()
    def _update_difficulty(self,delta):
        self.__difficulty += delta
        if self.__difficulty > 1:
            self.__difficulty = 1
        if self.__difficulty < 0:
            self.__difficulty = 0
    def update_player_char(self, char):
        self.__player_char = char
    def available_moves(self,):
        return [int(i) for i in self.__board]
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
        print(self.check_win(self.__player_moves))
    def computer_move(self,move):
        self._make_move(move)
        self.__computer_moves.append(str(move))
        print(self.check_win(self.__computer_moves))
    def get_old(self,):
        self.__age_last_valid_move += 1
    def current_age(self,):
        return self.__age_last_valid_move
    def _reset_age(self,):
        self.__age_last_valid_move = 0
    # Where should check win be?
    def set_correct_response_id(self,nid):
        self.__looking_for = nid
    def get_correct_response_id(self,):
        return self.__looking_for
    
    @staticmethod
    def check_win(moves):
        wins = {'123':'horizontal','456':'horizontal','789':'horizontal','147':'vertical','258':'vertical','369':'vertical','159':'diagnonal','357':'diagnonal'}
        ordered_moves = [str(i) for i in list(range(1,10)) if str(i) in moves]
        
        for i in itertools.combinations(ordered_moves,3):
            pos = ''.join(i)
            if wins.get(pos,None) != None:
                return [True,wins[pos]]
        return [False,None]
        
if __name__ == '__main__':
    players = {'123':PLAYER(123,'SOME_BIG_NERD')}
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
    players['123'].reset_board()
    print(players['123'].current_board_str())
    print('age:',players['123'].current_age())
    
    
