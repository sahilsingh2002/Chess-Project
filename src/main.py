import pygame  # needed to make game
import sys  # needed to manipulate various functions and variable in different parts of python runtime environment

from const import *  # Importing const.py
from game import Game  # importing this for colors and board
from square import Square
from move import Move

class Main:
    def __init__(self):
        pygame.init()  # initializing pygame
        # making a screen of width and height given
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')  # caption set to chess
        self.game = Game()
 
    def mainloop(self):
        # setting pygame file
        screen = self.screen
        game = self.game
        dragger = self.game.dragger
        board = self.game.board
        # added shortcuts because of lots of using

        while True:
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_hover(screen)
            game.show_pieces(screen)
            if dragger.dragging:  # piece dragging
                dragger.update_blit(screen)

            for event in pygame.event.get():  # all events coded here
                # making pieces able to be dragged

                # click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)
                    # print(event.pos)   #position of mouse clicked
                    clicked_row = dragger.mouseY//SQSIZE  # rows affected by y cord
                    clicked_col = dragger.mouseX//SQSIZE  # cols affected by x cord

                    # print(dragger.mouseY,clicked_row)
                    # print(dragger.mouseX,clicked_col)
                    # give values of row and col clicked

                    # finding if a place clicked has a piece
                    if board.squares[clicked_row][clicked_col].has_piece():
                        # giving variable to piece
                        piece = board.squares[clicked_row][clicked_col].piece
                        
                        #valid piece?
                        if piece.color==game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col)
                            # saving initial position in case we do any illegal it goes back
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)  # dragging

                            # show methods
                            game.show_bg(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)

                # mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    motion_row=event.pos[1]//SQSIZE
                    motion_col=event.pos[0]//SQSIZE
                    game.set_hover(motion_row,motion_col)
                    
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)  # updating mouse

                        # show methods
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_hover(screen)
                        game.show_pieces(screen)
                        dragger.update_blit(screen)  # updating the piece blit

                # mouse release
                elif event.type == pygame.MOUSEBUTTONUP:
                    
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        
                        released_row=dragger.mouseY//SQSIZE
                        released_col=dragger.mouseX//SQSIZE
                        
                        #create possible move
                        initial =Square(dragger.initial_row,dragger.initial_col)
                        final =Square(released_row,released_col)
                        move=Move(initial,final)
                        
                        # if valid move
                        if board.valid_move(dragger.piece,move):
                            board.move(dragger.piece,move)
                            
                            # Show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen) 
                            
                            #next turn
                            game.next_turn()
                        
                    
                    dragger.undrag_piece()

                # quitting
                elif event.type == pygame.QUIT:  # if click on x button
                    pygame.quit()
                    sys.exit()
                    # game quits
                    # screen is made now
            pygame.display.update()  # updates display


main = Main()  # calls init
main.mainloop()  # calling mainloop
