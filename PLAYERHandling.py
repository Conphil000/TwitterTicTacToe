# -*- coding: utf-8 -*-
"""
Created on Sat May  7 12:16:50 2022

@author: Conor
"""

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
        print(c_board)
        for i in self.__player_moves:
            c_board = c_board.replace(i,self.__player_char)
        for i in self.__computer_moves:
            c_board = c_board.replace(i,self.__computer_char)
        print(c_board)
        for i in [3,6,9]:
            slicer = c_board[scroll:i]
            groups.append(f'{slicer[0]} |  {slicer[1]}  | {slicer[2]}')
            scroll += 3
            if i < 9:
                groups.append('- + - + -')
            
        return '\n'.join(groups)
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
    def computer_move(self,move):
        self._make_move(move)
        self.__computer_moves.append(str(move))
    def current_moves(self,):
        print('computer:',self.__computer_moves)
        print('player:',self.__player_moves)
    
if __name__ == '__main__':
    players = {'123':PLAYER(123,'SOME_BIG_NERD')}
    players['123'].available_moves()
    print(players['123'].current_board_str())
    players['123'].player_move(1)
    players['123'].computer_move(3)
    players['123'].computer_move(6)
    players['123'].computer_move(9)
    print(players['123'].current_board_str())
    players['123'].current_moves()