# Pygame Chess Game

This is a Player vs Player chess game created using Pygame. It allows two players to play a game of chess on the same computer.

# Installation

To install and run this game, you will need to follow these steps:

Clone this repository to your local machine by running the command git clone https://github.com/sahilsingh2002/Chess-Project.git in your terminal.
Install the Pygame library by running the command **pip install pygame**.
Navigate to the **src** directory on your local machine.
Run the command python **main.py** to start the game.

# How to Play

To play the game, follow these instructions:

The game starts with the white pieces on the bottom and the black pieces on the top.
Players take turns moving their pieces by selecting a piece and then selecting a valid move on the board.
The objective of the game is to checkmate the opponent's king.
If a player's king is in check, they must move their king out of check or block the attack with another piece.
The game ends when one player's king is checkmated, or if the game is a draw.

# Features

This chess game includes the following features:

* A graphical user interface built using Pygame.
* Legal move validation, including en passant, castling, and promotion.
* A turn-based system that alternates between players.
* A highlight of possible moves for a selected piece.
* Changing themes using key **t**.
* Restarting Game using key **r**.

# Code Structure

This game is built using object-oriented programming principles in Python. The main.py file contains the main game loop and handles user input. The board.py file contains the logic for the chess board and pieces. The gui.py file contains the Pygame code for drawing the board and pieces on the screen.

# Acknowledgments

This game was created using the Pygame library and was inspired by other open-source chess games on Github.

# Future Development

In the future, we plan to add the following features to this game:

An AI opponent to play against.
Online multiplayer capabilities.
A database to store game histories and player statistics.
