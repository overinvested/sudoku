import ast
from copy import deepcopy


with open('sudoku_constraints.py') as constraints_file:
    constraints = ast.literal_eval(constraints_file.read())


def generate_domains(board: dict) -> dict:
    """
    generate_domains\n
    Adds domains to the board
    @param {dict} board: the starting board
    @return {dict} board: the board with domains added
    """

    for cell in board:
        if board[cell]['value']:
            board[cell]['domain'] = [board[cell]['value']]
        else:
            board[cell]['domain'] = [1,2,3,4,5,6,7,8,9]

    return board


def generate_arcs(constraints: dict) -> dict:
    """
    generate_arcs\n
    Creates bidirectional arcs from constraints
    @param {dict} constraints: the problem's constraints
    @return {dict} constraints: the constraints made bidirectional
    """

    keys = list(constraints.keys())

    for key in keys:
        cell1 = key[0]
        cell2 = key[1]
        constraints[(cell2, cell1)] = constraints[(cell1, cell2)]

    return constraints


def generate_assignment(board: dict) -> dict:
    """
    generate_assignment\n
    Creates a running assignment from the starting board
    @param {dict} board: the starting board
    @return {dict} assignment: the assignment corresponding to the starting board
    """

    assignment = {}
    for cell in board:
        if board[cell]['value']:
            assignment[cell] = board[cell]['value']
    return assignment


def generate_boards(assignment: dict) -> list:
    """
    generate_boards\n
    Generates all boards on the way to the solved puzzle
    @param {dict} assignment: the final assignment
    @return {list} boards: a list of boards after each cell assignment
    """

    # all of the cells will be in ascending order for the first assignment
    board = [[' ' for i in range(9)] for j in range(9)]
    boards = []
    keys = list(assignment.keys())
    while keys[0] < keys[1]:
        cell = [int(x) for x in keys[0] if x.isdigit()]
        board[cell[0]-1][cell[1]-1] = assignment[keys[0]]
        del assignment[keys[0]]
        keys = keys[1:]

    # the final cell in the original board would get left out otherwise
    cell = [int(x) for x in keys[0] if x.isdigit()]
    board[cell[0]-1][cell[1]-1] = assignment[keys[0]]
    del assignment[keys[0]]
    keys = keys[1:]

    boards.append(deepcopy(board))


    for key in assignment:
        cell = [int(x) for x in key if x.isdigit()]
        board[cell[0]-1][cell[1]-1] = assignment[key]
        boards.append(deepcopy((board)))

    return boards


def revise(constraints: dict, board: dict, arc: tuple) -> bool:
    """
    revise\n
    Revises the domains of cells in the board based on an arc, returns true if revision was done
    @param {dict} constraints: the set of constraints
    @param {dict} board: the current board
    @param {tuple} arc: the arc we consider
    @return {bool} whether or not a revision was done
    """
    
    revised = False
    for i, value1 in enumerate(board[arc[0]]['domain']):
        possible_values = len(board[arc[1]]['domain'])
        for value2 in board[arc[1]]['domain']:
            try:
                constraints[(arc[0], arc[1])].index([value1,value2])
            except:
                possible_values -= 1
            if possible_values == 0:
                board[arc[0]]['domain'].pop(i)
                revised == True

    return revised


def ac3(constraints: dict, board: dict) -> bool:
    """
    ac3\n
    Maintains arc consistency, returns true there is a solution given the constraints
    @param {dict} constraints: the set of constraints
    @param {dict} board: the current board
    @return {bool} whether or not a solution can be reached
    """

    queue = [arc for arc in generate_arcs(constraints)]
    while queue:
        arc = queue.pop()
        if revise(constraints, board, arc):
            if not board[arc[0]]['domain']:
                return False
            neighbors = [neighbor for neighbor in constraints if neighbor[1] == arc[0]]
            queue = queue + neighbors

    return True


def minimum_remaining_values(board: dict, assignment: dict) -> str:
    """
    minimum_remaining_values\n
    Finds the cell with the minimum number of domain values remaining
    @param {dict} board: the current board
    @param {dict} assignment: the current assignment of cells
    @return {str} min: the cell with the minimum remaining possible domain values
    """

    min = ''
    min_length = 11
    for cell in board:
        if cell in assignment.keys():
            continue
        if len(board[cell]['domain']) < min_length:
            min_length = len(board[cell]['domain'])
            min = cell

    return min


def backtracking_search(constraints: dict, board: dict) -> dict:
    """
    backtracking_search\n
    Wrapper function for the backtracking search, generates starting domains and assignment
    @param {dict} constraints: the set of constraints
    @param {dict} board: the starting board
    @return {dict} bactrack(): the result of the backtracking search
    """

    board = generate_domains(board)
    assignment = generate_assignment(board)
    return backtrack(constraints, board, assignment)


def backtrack(constraints: dict, board: dict, assignment: dict) -> dict:
    """
    backtrack\n
    The backtracking search, finds a solution recursively while being able to return to previous states
    @param {dict} constraints: the set of constraints
    @param {dict} board: the current board
    @param {dict} assignment: the current assignment
    @return {dict} assignment: the final assignment and result of the backtracking search
    """

    if len(assignment) == len(board):
        return assignment
    var = minimum_remaining_values(board, assignment)
    if(ac3(constraints, board)):
        if var:
            for val in board[var]['domain']:
                assignment[var] = val
                temp_board = deepcopy(board)
                temp_board[var]['value'] = val
                temp_board[var]['domain'] = [val]
                result = backtrack(constraints, temp_board, assignment)
                if result:
                    return result
                del assignment[var]
        else:
            return assignment
        
    return None


test1 = {   'C11': {'value': 7}, 'C12': {'value': None}, 'C13': {'value': None}, 'C14': {'value': 4}, 'C15': {'value': None}, 'C16': {'value': None}, 'C17': {'value': None}, 'C18': {'value': 8}, 'C19': {'value': 6},
            'C21': {'value': None}, 'C22': {'value': 5}, 'C23': {'value': 1}, 'C24': {'value': None}, 'C25': {'value': 8}, 'C26': {'value': None}, 'C27': {'value': 4}, 'C28': {'value': None}, 'C29': {'value': None},
            'C31': {'value': None}, 'C32': {'value': 4}, 'C33': {'value': None}, 'C34': {'value': 3}, 'C35': {'value': None}, 'C36': {'value': 7}, 'C37': {'value': None}, 'C38': {'value': 9}, 'C39': {'value': None},
            'C41': {'value': 3}, 'C42': {'value': None}, 'C43': {'value': 9}, 'C44': {'value': None}, 'C45': {'value': None}, 'C46': {'value': 6}, 'C47': {'value': 1}, 'C48': {'value': None}, 'C49': {'value': None},
            'C51': {'value': None}, 'C52': {'value': None}, 'C53': {'value': None}, 'C54': {'value': None}, 'C55': {'value': 2}, 'C56': {'value': None}, 'C57': {'value': None}, 'C58': {'value': None}, 'C59': {'value': None},
            'C61': {'value': None}, 'C62': {'value': None}, 'C63': {'value': 4}, 'C64': {'value': 9}, 'C65': {'value': None}, 'C66': {'value': None}, 'C67': {'value': 7}, 'C68': {'value': None}, 'C69': {'value': 8},
            'C71': {'value': None}, 'C72': {'value': 8}, 'C73': {'value': None}, 'C74': {'value': 1}, 'C75': {'value': None}, 'C76': {'value': 2}, 'C77': {'value': None}, 'C78': {'value': 6}, 'C79': {'value': None},
            'C81': {'value': None}, 'C82': {'value': None}, 'C83': {'value': 6}, 'C84': {'value': None}, 'C85': {'value': 5}, 'C86': {'value': None}, 'C87': {'value': 9}, 'C88': {'value': 1}, 'C89': {'value': None},
            'C91': {'value': 2}, 'C92': {'value': 1}, 'C93': {'value': None}, 'C94': {'value': None}, 'C95': {'value': None}, 'C96': {'value': 3}, 'C97': {'value': None}, 'C98': {'value': None}, 'C99': {'value': 5}
            }

test2 = {   'C11': {'value': 1}, 'C12': {'value': None}, 'C13': {'value': None}, 'C14': {'value': 2}, 'C15': {'value': None}, 'C16': {'value': 3}, 'C17': {'value': 8}, 'C18': {'value': None}, 'C19': {'value': None},
            'C21': {'value': None}, 'C22': {'value': 8}, 'C23': {'value': 2}, 'C24': {'value': None}, 'C25': {'value': 6}, 'C26': {'value': None}, 'C27': {'value': 1}, 'C28': {'value': None}, 'C29': {'value': None},
            'C31': {'value': 7}, 'C32': {'value': None}, 'C33': {'value': None}, 'C34': {'value': None}, 'C35': {'value': None}, 'C36': {'value': 1}, 'C37': {'value': 6}, 'C38': {'value': 4}, 'C39': {'value': None},
            'C41': {'value': 3}, 'C42': {'value': None}, 'C43': {'value': None}, 'C44': {'value': None}, 'C45': {'value': 9}, 'C46': {'value': 5}, 'C47': {'value': None}, 'C48': {'value': 2}, 'C49': {'value': None},
            'C51': {'value': None}, 'C52': {'value': 7}, 'C53': {'value': None}, 'C54': {'value': None}, 'C55': {'value': None}, 'C56': {'value': None}, 'C57': {'value': None}, 'C58': {'value': 1}, 'C59': {'value': None},
            'C61': {'value': None}, 'C62': {'value': 9}, 'C63': {'value': None}, 'C64': {'value': 3}, 'C65': {'value': 1}, 'C66': {'value': None}, 'C67': {'value': None}, 'C68': {'value': None}, 'C69': {'value': 6},
            'C71': {'value': None}, 'C72': {'value': 5}, 'C73': {'value': 3}, 'C74': {'value': 6}, 'C75': {'value': None}, 'C76': {'value': None}, 'C77': {'value': None}, 'C78': {'value': None}, 'C79': {'value': 1},
            'C81': {'value': None}, 'C82': {'value': None}, 'C83': {'value': 7}, 'C84': {'value': None}, 'C85': {'value': 2}, 'C86': {'value': None}, 'C87': {'value': 3}, 'C88': {'value': 9}, 'C89': {'value': None},
            'C91': {'value': None}, 'C92': {'value': None}, 'C93': {'value': 4}, 'C94': {'value': 1}, 'C95': {'value': None}, 'C96': {'value': 9}, 'C97': {'value': None}, 'C98': {'value': None}, 'C99': {'value': 5}
            }


# Sanity Checks
four_by_four_constraints = {('C11','C12'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C11','C13'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C11','C14'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C11','C21'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C11','C31'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C11','C41'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C11','C22'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C21','C22'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C21','C23'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C21','C24'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C21','C31'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C21','C41'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C31','C32'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C31','C33'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C31','C34'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C31','C41'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C31','C42'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C41','C42'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C41','C43'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C41','C44'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C12','C13'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C12','C14'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C12','C22'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C12','C21'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C12','C32'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C12','C42'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C22','C23'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C22','C24'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C22','C32'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C22','C42'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C32','C33'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C32','C41'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C32','C34'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C32','C42'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C42','C43'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C42','C44'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C13','C14'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C13','C23'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C13','C33'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C13','C43'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C13','C24'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C23','C24'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C23','C33'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C23','C43'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C33','C34'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C33','C43'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C33','C44'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C43','C44'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C14','C23'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C14','C24'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C14','C34'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C14','C44'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C24','C34'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C24','C44'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C34','C44'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            ('C34','C43'):[[1,2],[1,3],[1,4],[2,1],[2,3],[2,4],[3,1],[3,2],[3,4],[4,1],[4,2],[4,3]],
            }

four_by_four = {'C11': {'value': 1}, 'C12': {'value': None}, 'C13': {'value': None}, 'C14': {'value': None},
                'C21': {'value': None}, 'C22': {'value': 2}, 'C23': {'value': None}, 'C24': {'value': None},
                'C31': {'value': None}, 'C32': {'value': None}, 'C33': {'value': 3}, 'C34': {'value': None},
                'C41': {'value': None}, 'C42': {'value': None}, 'C43': {'value': None}, 'C44': {'value': 4}
                }
