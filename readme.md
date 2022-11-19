# Sudoku

This project solves sudoku boards using backtracking and the AC3 algorithm. Solution is displayed using Flask.

## To start the flask server:

### Bash

`$ export FLASK_APP=puzzle`

`$ flask run`

### CMD

`> set FLASK_APP=puzzle`

`> flask run`

### Powershell

`> $env:FLASK_APP = "puzzle"`

`> flask run`

## Solve a puzzle

Go to: `localhost:5000/puzzle/<input puzzle here>`in your browser

Please input the puzzle in the following format (puzzles are assumed to be 9x9):

Empty cell: nil

Filled cell: numeral 1-9

e.g.,

((nil nil nil nil nil 6 nil 8 nil)
(3 nil nil nil nil 2 7 nil nil)
(7 nil 5 1 nil nil 6 nil nil)
(nil nil 9 4 nil nil nil nil nil)
(nil 8 nil nil 9 nil nil 2 nil)
(nil nil nil nil nil 8 3 nil nil)
(nil nil 4 nil nil 7 8 nil 5)
(nil nil 2 8 nil nil nil nil 6)
(nil 5 nil 9 nil nil nil nil nil))
