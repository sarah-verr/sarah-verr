import sys
import heapq
sys.setrecursionlimit(50000)

class State: #Creating a State object
    def __init__(self, board, parent = None):
        self.board = board
        self.pieces = self.set_piece()
        if parent is None:
            self.parent = None
            self.g = 0
        else:
            self.parent = parent  
            self.g = self.parent.g + 1
        self.h = manhattan_distance(self.pieces['big_block'][0], self.pieces['big_block'][1], 3,1)
        self.f = self.g + self.h
        self.string = self.string_converter()
        self.h2 = advanced(self.pieces['big_block'][0], self.pieces['big_block'][1], 3,1, self.board)
        self.f2 = self.h2 + self.g

    def string_converter(self):
        v = []
        h = []
        name = {'v1','v2','v3','v4','v5'}
        little = {'s1','s2','s3','s4'}
        board = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        i = 0
        j = 0
        while i < 5:
            while j < 4:
                board[i][j] = self.board[i][j]
                j += 1
            i+=1
            j = 0
        for item in name:
            if self.pieces[item][4] == 1:
                h.append(item)
            else:
                v.append(item)
        for piece in v:
            x = self.pieces[piece][0]
            y = self.pieces[piece][1]
            board[x][y] = 3
            board[x+1][y] = 3
        for piece in h:
            x = self.pieces[piece][0]
            y = self.pieces[piece][1]
            board[x][y] = 2
            board[x][y+1] = 2
        for piece in little:
            x = self.pieces[piece][0]
            y = self.pieces[piece][1]
            board[x][y] = 4        
        s = ''
        for lst in board:
            for item in lst:
                s = s + str(item)
        return s

    #creating a dictionary that uses a pieces title  and points to their position, number used in input and number that will be used for output
    def set_piece(self): 
        horv = [2,3,4,5,6]
        d = {}
        d['big_block'] = self.find(1,1)
        d['v1'], horv = self.find_v(horv)
        d['v2'], horv = self.find_v(horv)
        d['v3'], horv = self.find_v(horv)
        d['v4'], horv = self.find_v(horv)
        d['v5'], horv = self.find_v(horv)
        d['s1'] = self.find(7,4)
        d['s2'] = self.find_next(7,4, 1)
        d['s3'] = self.find_next(7,4, 2)
        d['s4'] = self.find_next(7,4, 3)
        d['b1'] = self.find(0,0)
        d['b2'] = self.find_next(0,0, 1)
        return d

    #finds a piece in the board   
    def find(self, num, num2):
        for r in range(0,5):
            for c in range(0,4):
                if self.board[r][c] == num:
                    return (r,c,num2,num,0)
    
    #finds a piece in the board if there is more than one piece with the same number (eg. blanks)
    def find_next(self, num, num2, cap):
        i = 0
        for r in range(0,5):
            for c in range(0,4):
                if self.board[r][c] == num:
                    if cap == i:
                        return (r,c,num2,num,0)
                    i += 1

    #determines if 2x1 pieces are horizontal or vertical and finds all 2x1 pieces
    def find_v(self, horv):
        for i in horv:
            for r in range(0,4):
               for c in range(0,4):
                    if self.board[r][c] == i and self.board[r + 1][c] == i:
                        horv.remove(i)
                        return (r,c,3,i,0), horv 
        for i in horv:
            for r in range(0,5):
               for c in range(0,3):
                    if self.board[r][c] == i and self.board[r][c + 1] == i:
                        horv.remove(i)
                        return (r,c,2,i,1), horv
        return (r,c,3,i,1), horv

# Running A* search using manhattan heuristic
def main(input_f, DFS_output_f, A_output_f):
    input_file = open(input_f)
    initial_board = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    i = 0
    j = 0
    for line in input_file:
        for char in line:
            if char != '\n':
                initial_board[i][j] = int(char)
                j += 1
        i += 1
        j = 0
    input_file.close()
    #A* 1
    initial_state = State(initial_board)
    priorityheap = [initial_state.f]
    visited_states = {}
    visited_states[initial_state] = ([],)
    visited_states[initial_state.string] = None
    connection = {}
    connection[initial_state.f] = [initial_state]
    winning_state = initial_state
    while goal(winning_state) is False:
        winning_state = connection[heapq.heappop(priorityheap)].pop(0)
        winning_state = find_solution(winning_state, visited_states, connection, priorityheap)
    all_states = [winning_state.string]
    get_cost(winning_state, all_states)
    cost = len(all_states) - 1
    i = cost
    output = open(A_output_f, 'w')
    output.write('Cost of the solution: ' + str(cost) + '\n')
    while i >= 0:
        s = all_states[i]
        output.write('\n')
        output.write(s[0:4])
        output.write('\n')
        output.write(s[4:8])
        output.write('\n')
        output.write(s[8:12])
        output.write('\n')
        output.write(s[12:16])
        output.write('\n')
        output.write(s[16:20])
        output.write('\n')
        i = i -1
    output.close()
    for state in all_states:
        del state
    del all_states
    del winning_state
    del connection
    del visited_states
    del priorityheap

# Running A* search using advanced heuristic
def main_2(input_f):
    input_file = open(input_f)
    initial_board = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    i = 0
    j = 0
    for line in input_file:
        for char in line:
            if char != '\n':
                initial_board[i][j] = int(char)
                j += 1
        i += 1
        j = 0
    input_file.close()
    #A*2  
    first_state = State(initial_board)
    pheap = [first_state.f2]
    visited_s = {}
    visited_s[first_state] = ([],)
    visited_s[first_state.string] = None
    conn = {}
    conn[first_state.f2] = [first_state]
    goal_state = first_state
    while goal(goal_state) is False and pheap != []:
        goal_state = conn[heapq.heappop(pheap)].pop(0)
        goal_state = find_solution2(goal_state, visited_s, conn, pheap)

# Running DFS search
def main2(input_f, DFS_output_f, A_output_f):
    input_file = open(input_f)
    initial_board = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    i = 0
    j = 0
    for line in input_file:
        for char in line:
            if char != '\n':
                initial_board[i][j] = int(char)
                j += 1
        i += 1
        j = 0
    input_file.close()
    #DFS
    starting_state = State(initial_board)
    visited = {}
    visited[starting_state.string] = None
    states_queue = [starting_state]
    final_state = states_queue.pop()
    while goal(final_state) is False:
        final_state, states_queue, visited = DFS(final_state, states_queue, visited)
        final_state = states_queue.pop()
    DFS_states = [final_state.string]
    get_cost(final_state, DFS_states)
    cost = len(DFS_states) - 1
    i = cost
    output = open(DFS_output_f, 'w')
    output.write('Cost of the solution: ' + str(cost) + '\n')
    while i >= 0:
        s = DFS_states[i]
        output.write('\n')
        output.write(s[0:4])
        output.write('\n')
        output.write(s[4:8])
        output.write('\n')
        output.write(s[8:12])
        output.write('\n')
        output.write(s[12:16])
        output.write('\n')
        output.write(s[16:20])
        output.write('\n')
        i = i -1
    output.close()

#DFS algorithm
def DFS(parent_state, lst, visited):
    children_states = find_moves(parent_state)
    for child in children_states:
        if child.string not in visited:
            visited[child.string] = None
            lst.append(child)   
    return parent_state, lst, visited 

#Get cost of solution as well as create a list from goal state to initial state
def get_cost(state, all_states):
    if state.parent is not None:
        all_states.append(state.parent.string)
        get_cost(state.parent, all_states)

#manhattan heuristic solver
def find_solution(parent_state, visited_states, connection, priorityheap):
    children_states = find_moves(parent_state)
    for child in children_states:
        if child.string not in visited_states:
            visited_states[child] = ([],parent_state)
            visited_states[child.string] = ([],)
            visited_states[parent_state][0].append(child)
            heapq.heappush(priorityheap, child.f)
            if child.f not in connection:
                connection[child.f] = []
            connection[child.f].append(child)       
    return parent_state

#advanced heuristic solver
def find_solution2(parent_state, visited_s, connection, priorityheap):
    children_states = find_moves(parent_state)
    for child in children_states:
        if child.string not in visited_s:
            visited_s[child] = ([],parent_state)
            visited_s[child.string] = ([],)
            visited_s[parent_state][0].append(child)
            heapq.heappush(priorityheap, child.f2)
            if child.f2 not in connection:
                connection[child.f2] = []
            connection[child.f2].append(child)       
    return parent_state

#manhattan heuristic calcularor
def manhattan_distance(sx, sy, gx, gy): #works
    return abs(sx-gx) + abs(sy-gy)

#Advanced heuristic calculator
def advanced(sx, sy, gx, gy, board):
    count = manhattan_distance(sx, sy, gx, gy)
    blanks = 0
    if sx-1 >= 0 and sy + 1 <= 3: 
        if board[sx - 1][sy] != 0 and board[sx - 1][sy + 1] != 0:  
            blanks += 1
    else:
        blanks += 1
    if sx + 2 <= 4 and sy + 1 <= 3:
        if board[sx + 2][sy + 1] != 0 and board[sx + 2][sy] != 0:
            blanks += 1
    else:
        blanks += 1
    if sx+1 >= 0 and sy - 1 <= 3: 
        if board[sx + 1][sy - 1] != 0 and board[sx][sy - 1] != 0:  
            blanks += 1
    else:
        blanks += 1
    if sx + 1 <= 4 and sy + 2 <= 3:
        if board[sx][sy + 2] != 0 and board[sx + 1][sy + 2] != 0:
            blanks += 1
    else:
        blanks += 1
    count = count + blanks//4
    return count

#is the board in a goal state, returns True if it is, False otherwise
def goal(board): 
    if board.board[3][1] == 1 and board.board[4][2] == 1:
        return True #yay goal state
    return False
    
#finds valid moves and returns a list of all valid moves avaible from current state
def find_moves(board): 
    b1 = board.pieces['b1']
    b2 = board.pieces['b2']
    moves = []
    blank = [b1,b1,b1,b1,b2,b2,b2,b2]
    x_val = [0,0,1,-1,0,0,1,-1]
    y_val = [1,-1,0,0,-1,1,0,0]
    for i in range(0,8):
        move = check(board, blank[i], x_val[i], y_val[i])
        if move is not None and move.board != board.board and move != board: 
            moves.append(move)
    return moves

#Checks if a specific move is valid, returns the next state if the move is valid, or None if move is invalid
def check(board, blank, x, y): #works
    if blank[0] == 0 and x == -1:
        return None
    if blank[0] == 4 and x == 1:
        return None
    if blank[1] == 0 and y == -1:
        return None
    if blank[1] == 3 and y == 1:
        return None
    val = board.board[blank[0] + x][blank[1] + y]
    u_b = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    for r in range(0,5):
        for c in range(0,4):
            u_b[r][c] = board.board[r][c]
    if val == 0:
        return None
    elif val == 7:
        u_b[blank[0]+x][blank[1]+y] = 0
        u_b[blank[0]][blank[1]] = 7
        updated_board = State(u_b, board)
        return updated_board
    elif val == 1:
        if 4 >= blank[0] + y >=0 and 3 >= blank[1] + x >=0 and board.board[blank[0] + y][blank[1] + x] == 0:
            if 4 >= blank[0] + y+x >=0 and 3 >= blank[1] + y + x >=0 and board.board[blank[0] + y + x][blank[1] + x + y] == 1:
                u_b[blank[0]+y][blank[1]+x] = 1
                u_b[blank[0]][blank[1]] = 1
                u_b[blank[0]+x+x][blank[1]+y+y] = 0
                u_b[blank[0]+x+y+x][blank[1]+x+y+y] = 0
                updated_board = State(u_b, board)
                return updated_board
            return None
        return None
    elif (3 >= blank[1] + y + 1 >= 0 and board.board[blank[0] + x][blank[1] + y + 1] == val) or (3 >= blank[1] + y - 1 >= 0 and board.board[blank[0] + x][blank[1] + y - 1] == val):
        if x == 0:
            u_b[blank[0]][blank[1] + y + y] = 0
            u_b[blank[0]][blank[1]] = val
            updated_board = State(u_b, board)
            return updated_board
        elif 3 >= blank[1] + 1 >= 0 and board.board[blank[0]][blank[1] + 1] == 0:
            if board.board[blank[0] + x][blank[1] + 1] == val:
                u_b[blank[0]+x][blank[1]] = 0
                u_b[blank[0]+ x][blank[1]+ 1] = 0
                u_b[blank[0]][blank[1]] = val
                u_b[blank[0]][blank[1] + 1] = val
                updated_board = State(u_b, board)
                return updated_board
            return None
        return None
    #must be verticle
    else:
        if y == 0:
            u_b[blank[0] + x + x][blank[1]] = 0
            u_b[blank[0]][blank[1]] = val
            updated_board = State(u_b, board)
            return updated_board
        elif 4 >= blank[0] + 1 >= 0 and board.board[blank[0] + 1][blank[1]] == 0: #blank 
            if board.board[blank[0] + 1][blank[1] + y] == val:
                u_b[blank[0]][blank[1] + y] = 0
                u_b[blank[0] + 1][blank[1] + y] = 0
                u_b[blank[0]][blank[1]] = val
                u_b[blank[0] + 1][blank[1] ] = val
                updated_board = State(u_b, board)
                return updated_board
    return None
    

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3]) #A* search manhattan heuristic
    main2(sys.argv[1], sys.argv[2], sys.argv[3]) #DFS search