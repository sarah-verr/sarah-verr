import sys


class State:

    def __init__(self, board):
        self.board = board
        self.boats = self.boat_counter()
        self.boat_val = [0, 0, 0, 0]
        for key in self.boats:
            if self.boats[key]-1 < len(self.boat_val):
                self.boat_val[self.boats[key]-1] += 1
            else:
                self.boat_val[0] += 100
        self.unassigned, self.available = [], []
        self.string = ''
        self.unassigned_row, self.unassigned_col = [], []
        self.boat_row, self.boat_col = [], []
        for i in range(len(self.board)):
            self.boat_row.append(0)
            self.unassigned_row.append(0)
            self.available.append([])
            for j in range(len(self.board)):
                if i == 0:
                    self.boat_col.append(0)
                    self.unassigned_col.append(0)
                self.string += str(self.board[i][j])
                if self.board[i][j] == 0:
                    self.unassigned_col[j] += 1
                    self.unassigned_row[i] += 1
                    self.unassigned.append((i, j))
                    self.available[i].append([1, 2])
                else:
                    self.available[i].append([])
                    if self.board[i][j] == 2:
                        self.boat_row[i] += 1
                        self.boat_col[j] += 1

    def boat_counter(self):
        locations = {}
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] == 2:
                    k, n = 0, 0
                    while i - k - 1 >= 0 and self.board[i - k - 1][j] == 2:
                        k += 1
                    while j - n - 1 >= 0 and self.board[i][j - n - 1] == 2:
                        n += 1
                    if k == 0 and n == 0:
                        locations[(i, j)] = 1
                    else:
                        locations[(i - k, j - n)] += 1
        return locations


def main(input_f, output):
    input_file = open(input_f)
    row_values, col_values, ship_values, boat_locations, initial_board = \
        get_input(input_file)
    state = State(initial_board_setup(row_values, col_values, boat_locations,
                                      initial_board))
    states_queue = [state]
    while not check_all_constraints(state, row_values, col_values, ship_values,
                                    True):
        states_queue = DFS(state, states_queue, row_values, col_values,
                           ship_values)
        state = GAC(states_queue.pop(), row_values, col_values)
    final = state_converter(state.board)
    output = open(output, 'w')
    for row in final:
        for char in row:
            output.write(char)
        output.write('\n')
    output.close()


def GAC(old_state, row_values, col_values):
    curr_state = State(fill_water(row_values, col_values, old_state.boat_row,
                                  old_state.boat_col, old_state.board))
    curr_state = State(preprocessing_row(row_values, curr_state))
    curr_state = State(preprocessing_col(col_values, curr_state))
    while old_state.string != curr_state.string:
        old_state = curr_state
        curr_state = State(
            fill_water(row_values, col_values, old_state.boat_row,
                       old_state.boat_col, old_state.board))
        curr_state = State(preprocessing_row(row_values, curr_state))
        curr_state = State(preprocessing_col(col_values, curr_state))
    return curr_state


def state_converter(board):
    new_board = board_copy(board)
    for i in range(len(new_board)):
        for j in range(len(new_board)):
            if new_board[i][j] == 1:
                new_board[i][j] = 'W'
            else:
                new_board[i][j] = get_value(i, j, board)
    return new_board


def get_value(i, j, board):
    if i - 1 >= 0 and board[i-1][j] == 2:
        if i + 1 < len(board) and board[i + 1][j] == 2:
            return 'M'
        return 'B'
    elif j - 1 >= 0 and board[i][j-1] == 2:
        if j + 1 < len(board) and board[i][j + 1] == 2:
            return 'M'
        return 'R'
    elif i + 1 < len(board) and board[i+1][j] == 2:
        return 'T'
    elif j + 1 < len(board) and board[i][j + 1] == 2:
        return 'L'
    return 'S'


def DFS(parent_state, lst, row_values, col_values, ship_values):
    children_states = FC(parent_state, row_values, col_values, ship_values)
    for child in children_states:
        lst.append(child)
    return lst


def row_col_constraint(val, con, exact):
    for i in range(len(val)):
        if int(val[i]) > int(con[i]):
            return False
        if exact and int(val[i]) != int(con[i]):
            return False
    return True


def check_all_constraints(board, row_values, col_values, ship_values, exact):
    r = row_col_constraint(board.boat_row, row_values, exact)
    c = row_col_constraint(board.boat_col, col_values, exact)
    if exact:
        b = row_col_constraint(board.boat_val, ship_values, exact)
    else:
        b = True
    if r is True and c is True and b is True:
        return True
    return False


def FC(board, row_values, col_values, ship_values):
    potential = []
    if not board.unassigned:
        return potential
    v = board.unassigned.pop()
    for d in board.available[v[0]][v[1]]:
        new_board = board_copy(board.board)
        new_board[v[0]][v[1]] = d
        if check_all_constraints(board, row_values, col_values, ship_values, False):
            new_board = fill_water(row_values, col_values, board.boat_row, board.boat_col, new_board)
            if d == 2:
                new_board = water_round_boat(v[0], v[1], new_board)
            new_state = State(new_board)
            potential.append(new_state)
    return potential


def board_copy(board):
    new = []
    for i in range(len(board)):
        new.append([])
        for item in board[i]:
            new[i].append(item)
    return new


def initial_board_setup(row_values, col_values, boat_locations, initial_board):
    initial_board = fill_initial(row_values, col_values, initial_board)
    for boat in boat_locations:
        initial_board = water_around_boat(boat_locations[boat], boat[0], boat[1], initial_board)
    for boat in boat_locations:
        initial_board = water_around_boat(boat_locations[boat], boat[0], boat[1], initial_board)
    board_01 = []
    i = 0
    for lst in initial_board:
        board_01.append([])
        for val in lst:
            if val == '0':
                board_01[i].append(0)
            elif val == 'W':
                board_01[i].append(1)
            else:
                board_01[i].append(2)
        i += 1
    for i in range(len(board_01)):
        for j in range(len(board_01)):
            if board_01[i][j] == 2:
                board_01 = water_round_boat(i, j, board_01)
    state = GAC(State(board_01), row_values, col_values)
    return state.board


def preprocessing_row(row_values, state):
    board = board_copy(state.board)
    for i in range(len(state.boat_row)):
        if int(row_values[i]) != 0 and int(row_values[i]) == state.unassigned_row[i] + state.boat_row[i]:
            for j in range(len(board)):
                if board[i][j] == 0:
                    board[i][j] = 2
                    board = water_round_boat(i, j, board)
    return board


def preprocessing_col(col_values, state):
    board = board_copy(state.board)
    for i in range(len(state.boat_col)):
        if int(col_values[i]) != 0 and int(col_values[i]) == state.unassigned_col[i] + state.boat_col[i]:
            for j in range(len(state.board)):
                if board[j][i] == 0:
                    board[j][i] = 2
                    board = water_round_boat(j, i, board)
    return board


def fill_water(row_values, col_values, row_curr, col_curr, board):
    i = 0
    for val in row_curr:
        if row_values[i] == '0' or (val - int(row_values[i])) == 0:
            for j in range(len(board)):
                if board[i][j] == 0:
                    board[i][j] = 1
        i += 1
    i = 0
    for val in col_curr:
        if col_values[i] == '0' or val - int(col_values[i]) == 0:
            for j in range(len(board)):
                if board[j][i] == 0:
                    board[j][i] = 1
        i += 1
    return board


def water_round_boat(x, y, board):
    if x - 1 >= 0:
        if board[x - 1][y] == 2:
            if y - 1 >= 0:
                board[x][y - 1] = 1
            if y + 1 < len(board):
                board[x][y + 1] = 1
        if y - 1 >= 0:
            board[x - 1][y - 1] = 1
        if y + 1 < len(board):
            board[x - 1][y + 1] = 1
    if x + 1 < len(board):
        if board[x + 1][y] == 2:
            if y - 1 >= 0:
                board[x][y - 1] = 1
            if y + 1 < len(board):
                board[x][y + 1] = 1
        if y - 1 >= 0:
            board[x + 1][y - 1] = 1
        if y + 1 < len(board):
            board[x + 1][y + 1] = 1
    if y - 1 >= 0 and board[x][y-1] == 2:
        if x - 1 >= 0:
            board[x-1][y] = 1
        if x + 1 < len(board):
            board[x+1][y] = 1
    if y + 1 < len(board) and board[x][y + 1] == 2:
        if x - 1 >= 0:
            board[x-1][y] = 1
        if x + 1 < len(board):
            board[x+1][y] = 1
    return board


def water_around_boat(boat_type, x, y, board):
    if x - 1 >= 0:
        if boat_type != 'B' and boat_type != 'M':
            board[x - 1][y] = 'W'
        elif board[x - 1][y] == '0' and boat_type == 'B':
            board[x - 1][y] = 'X'
        if y - 1 >= 0:
            board[x - 1][y - 1] = 'W'
        if y + 1 < len(board):
            board[x - 1][y + 1] = 'W'
    if x + 1 < len(board):
        if boat_type != 'T' and boat_type != 'M':
            board[x + 1][y] = 'W'
        elif board[x + 1][y] == '0' and boat_type == 'T':
            board[x + 1][y] = 'X'
        if y - 1 >= 0:
            board[x + 1][y - 1] = 'W'
        if y + 1 < len(board):
            board[x + 1][y + 1] = 'W'
    if y - 1 >= 0:
        if boat_type != 'R'and boat_type != 'M':
            board[x][y - 1] = 'W'
        elif board[x][y - 1] == '0' and boat_type == 'R':
            board[x][y - 1] = 'X'
    if y + 1 < len(board):
        if boat_type != 'L' and boat_type != 'M':
            board[x][y + 1] = 'W'
        elif board[x][y + 1] == '0' and boat_type == 'L':
            board[x][y + 1] = 'X'
    if boat_type == 'M':
        if x == 0 or x == len(board) - 1 or board[x - 1][y] == 'W' or board[x + 1][y] == 'W':
            board[x][y-1] = 'X'
            board[x][y+1] = 'X'
        elif y == 0 or y == len(board) - 1 or board[x][y - 1] == 'W' or board[x][y + 1] == 'W':
            board[x-1][y] = 'X'
            board[x+1][y] = 'X'
    return board


def fill_initial(row_values, col_values, board):
    for i in range(len(row_values)):
        if row_values[i] == '0':
            for j in range(len(board)):
                board[i][j] = 'W'
        if col_values[i] == '0':
            for j in range(len(board)):
                board[j][i] = 'W'
    return board


def get_input(input_file):
    row_values = []
    col_values = []
    ship_values = []
    input_file = input_file.readlines()
    for char in input_file[0]:
        if char != '\n':
            row_values.append(char)
    for char in input_file[1]:
        if char != '\n':
            col_values.append(char)
    for char in input_file[2]:
        if char != '\n':
            ship_values.append(char)
    while len(ship_values) < 4:
        ship_values.append('0')
    boat_locations = {}
    i = 3
    j = 0
    initial_board = []
    while i < len(input_file):
        if input_file[i] != '\n':
            initial_board.append([])
            for char in input_file[i]:
                if char != '\n':
                    initial_board[i - 3].append(char)
                    if char != '0' and char != 'W':
                        boat_locations[(i - 3, j)] = char
                    j += 1
        i += 1
        j = 0
    return row_values, col_values, ship_values, boat_locations, initial_board


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
