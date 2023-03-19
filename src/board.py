from const import *
from square import Square
from piece import *
from move import Move


class Board:
    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self.last_move=None
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def move (self,piece,move):
        initial=move.initial
        final=move.final
        
        #console board move update
        self.squares[initial.row][initial.col].piece=None
        self.squares[final.row][final.col].piece=piece
        
        #move
        piece.moved=True
        
        #clear valid moves
        piece.clear_moves()
        
        #set last move
        self.last_move=move
    
    def valid_move(self,piece,move):
        return move in piece.move
    
    def calc_moves(self, piece, row, col):
        '''
        calculate all the possible (valid) moves of a specific piecce on a specific position
        '''

        def knight_moves():
            # 8 possible moves
            possible_moves = [
                (row-2, col+1),     # two rows up one col right
                (row-2, col-1),     # two up one left
                (row-1, col+2),     # one up two right
                (row-1, col-2),     # one up two left
                (row+2, col-1),     # two down on left
                (row+2, col+1),     # two down one right
                (row+1, col-2),     # one down two left
                (row+1, col+2),     # one down two right
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        # create squares of the new move
                        initial = Square(row, col)
                        final = Square(possible_move_row,
                                       possible_move_col)  # piece=piece
                        # create new move
                        move = Move(initial, final)
                        # append new valid move
                        piece.add_move(move)

        def pawn_moves():
            # steps
            steps = 1 if piece.moved else 2

            # vertical moves
            start = row+piece.dir
            end = row+(piece.dir*(1+steps))
            for move_row in range(start, end, piece.dir):
                if Square.in_range(move_row):
                    if self.squares[move_row][col].isempty():

                        # create initial and final move squares
                        initial = Square(row, col)
                        final = Square(move_row, col)

                        # create new move
                        move = Move(initial, final)

                        # append the move
                        piece.add_move(move)

                    # blocked
                    else:
                        break

                # not in range
                else:
                    break

            # diagonal moves
            possible_move_row = row+piece.dir
            possible_move_cols = [col-1, col+1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        # create initial and final move squares
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        # create new move
                        move = Move(initial, final)
                        # append new move
                        piece.add_move(move)

        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row+row_incr
                possible_move_col = col+col_incr

                # create squares of possible new move
                initial = Square(row, col)
                final = Square(possible_move_row, possible_move_col)
                
                # create a possible new move
                move = Move(initial, final)

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        initial=Square(row,col)
                        final=Square(possible_move_row,possible_move_col)
                        move=Move(initial,final)
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            # empty
                            # append new move
                            piece.add_move(move)

                        # has enemy piece = add move+break
                        if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color): 
                            # append new move
                            piece.add_move(move)
                            break
                        
                        #has team piece  = break
                        
                        if self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color): 
                            break
                        
                    else:
                        break        
                    #incrementing incrs
                    possible_move_row,possible_move_col=possible_move_row+row_incr,possible_move_col+col_incr

        def king_moves():
            adjs=[(row-1,col+0), #up
                  (row-1,col+1), #upright
                  (row+0,col+1), #right
                  (row+1,col+1), #downright
                  (row+1,col+0), #down
                  (row+1,col-1), #downleft
                  (row+0,col-1), #left
                  (row-1,col-1), #upleft 
              ]
            #normal moves
            for possible_move in adjs:
                possible_move_row,possible_move_col=possible_move
                if Square.in_range(possible_move_row,possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        #create squares of the new move
                        initial = Square(row, col)
                        final = Square(possible_move_row,
                                       possible_move_col)  # piece=piece
                        # create new move
                        move = Move(initial, final)
                        # append new valid move
                        piece.add_move(move)
                        
            #castling moves
            
                        
            
        if isinstance(piece, Pawn):
            pawn_moves()

        elif isinstance(piece, Knight):
            knight_moves()

        elif isinstance(piece, Bishop):
            straightline_moves([
                (-1, 1),  # upright
                (-1, -1),  # up left
                (1, 1),  # down right
                (1, -1)  # down left
            ])

        elif isinstance(piece, Rook):
            straightline_moves([
                (-1, 0),  # up
                (0, 1),  # right
                (1, 0),  # down
                (0, -1)  # left
            ])

        elif isinstance(piece, Queen):
            straightline_moves([
                (-1, 1),    # upright
                (-1, -1),   # up left
                (1, 1),     # down right
                (1, -1),     # down left
                (-1, 0),    # up
                (0, 1),     # right
                (1, 0),     # down
                (0, -1)     # left
            ])

        elif isinstance(piece, King):
            king_moves()

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):  # these are private methods

        row_pawn, row_other = (6, 7) if color == 'white' else (
            1, 0)  # white are at bottom

        # all pawns creating
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))
        

        # rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))
        

        # queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))
        

        # king
        self.squares[row_other][4] = Square(row_other, 4, King(color))
        
