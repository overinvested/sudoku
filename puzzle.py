from sudoku import generate_boards, backtracking_search, constraints
from flask import Flask, render_template
import re

app = Flask(__name__)

def convert_to_board(input) -> list:
    """
    convert_to_board\n
    Takes input from address bar and creates a board
    @param {str} input: the contents of the address bar
    @return {dict} board: the resulting board
    """
    board = {}
    input = re.sub(r'\(|\)', '', input)
    re.sub(r'%20', ' ', input)
    input = re.sub(r'nil', 'None', input)
    input = [int(x) if x.isdigit() else None for x in input.split()]
    if len(input) > 1:
        k = 0
        for i in range(1,10):
            for j in range(1,10):
                board['C' + str(i) + str(j)] = {}
                board['C' + str(i) + str(j)]['value'] = input[k]
                k += 1
    return board


@app.route('/')
def hello():
    return 'Please enter \'localhost:5000/puzzle\' followed by a puzzle into the address bar.'


@app.route('/puzzle/<input>')
def puzzle(input):
    board = convert_to_board(input)
    assignment = backtracking_search(constraints, board)
    return render_template('sudoku.html', boards = generate_boards(assignment))