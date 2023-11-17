import sys
import heapq


state_cache = {}


class Board:
    def __init__(self, board, parent = None, score = None):
        self.str = board
        self.children = []
        if parent is None:
            self.parent = None
            self.height = 0
        else:
            self.parent = parent
            self.height = self.parent.height + 1
        self.red = colour_positions('r',self.str)
        self.black = colour_positions('b',self.str)
        s = ""
        for lst in self.str:
            for char in lst:
                s = s + char
        self.stri = s
        if self.height % 2 == 0:
            self.turn = 'r'
        else:
            self.turn = 'b'
        self.children = []
        if score is None:
            self.score_for_red = minimax(self.stri, self)
        else:
            self.score_for_red = score


def colour_positions(colour, board_s):
    colour_pos = []
    i = 0
    j = 0
    for line in board_s:
        for char in line:
            if char == colour:
                colour_pos.append((i,j,0))
            elif char.lower() == colour:
                colour_pos.append((i,j,1))
            j = j + 1
        i = i + 1
        j = 0
    return colour_pos


def main(input, output):
    input_file = open(input)
    initial_board = [[],[],[],[],[],[],[],[]]
    i = 0
    for line in input_file:
        for char in line:
            if char != '\n':
                initial_board[i].append(char)
        i = i + 1
    input_file.close()
    initial_board = Board(initial_board)
    visited = [initial_board]
    next_board = initial_board
    depth = 8
    while visited != []:
        if next_board.height <= depth and next_board.red != [] and next_board.black != []:
            if next_board.height%2== 0:
                potential_next_moves = successors('r', next_board)
            else:
                potential_next_moves = successors('b', next_board)
            if potential_next_moves != []:
                score_d = {}
                score_l = []
                for move in potential_next_moves:
                    if move is not None:
                        visited.append(move)
                        score_l.append(move.score_for_red)
                        if move.score_for_red not in score_d:
                            score_d[move.score_for_red] = []
                        score_d[move.score_for_red].append(move)
                heapq._heapify_max(score_l)
                while score_l != []:
                    next_board.children.append(score_d[heapq._heappop_max(score_l)].pop(0))
        next_board = visited.pop()  
    score, best_board = alphabeta(initial_board, -999999999, 999999999, depth) 
    output = open(output, 'w')
    i = 0
    for row in best_board.str:
        for item in row:
            output.write(item)
        if i < 7:
            output.write('\n')
        i = i + 1
    output.close()


def minimax(board_s, board):
    red_count = board_s.count('r') + 2*board_s.count('R') 
    black_count = board_s.count('b') + 2*board_s.count('B')
    if red_count == 0:
        return -1000 + board.height
    if black_count == 0:
        return 1000 - board.height
    red_x = [-1,-1]
    red_y = [1,-1]
    black_x = [1,1]
    black_y = [1,-1]
    for coord in board.red:
        opp = ['b', 'B']
        king = 'B'
        red_x = [-1,-1]
        red_y = [1,-1]
        red_count += safe(board, coord[0], coord[1], red_x, red_y, opp, king)
    for coord in board.black:
        opp = ['r', 'R']
        king = 'R'
        black_x = [1,1]
        black_y = [1,-1]
        black_count += safe(board, coord[0], coord[1], black_x, black_y, opp, king)
    return red_count - black_count


def safe(board, x,y, moves_x, moves_y, opp, king):
    for i in range(len(moves_x)):
        if 8 > x + moves_x[i] >= 0 and 8 > y + moves_y[i] >= 0 and 8 > x - moves_x[i] >= 0 and 8 > y - moves_y[i] >= 0:
            if board.str[x + moves_x[i]][y + moves_y[i]] in opp and board.str[x - moves_x[i]][y - moves_y[i]] == '.':
                return 0
        if 8 > x - moves_x[i] >= 0 and 8 > y + moves_y[i] >= 0 and 8 > x + moves_x[i] >= 0 and 8 > y - moves_y[i] >= 0:
            if board.str[x - moves_x[i]][y + moves_y[i]] == king and board.str[x + moves_x[i]][y - moves_y[i]] == '.':
                return 0    
    return 1
    
    
def alphabeta(board, alpha, beta, depth):
    if board.height == depth:
        return board.score_for_red, board
    if board.children == []:
        if board.turn == 'r':
            return -1000 + board.height, board
        else:
            return 1000 - board.height, board
    best_move = board.children[0]
    if board.turn == 'r':
        value = -999999999
    else:
        value = 999999999
    for move in board.children:
        nxt_val, nxt_move = alphabeta(move, alpha, beta, depth)
        if board.turn == 'r':
            if value < nxt_val: 
                value, best_move = nxt_val, move
            if value >= beta: 
                return best_move.score_for_red, best_move
            alpha = max(alpha, value)
        else:
            if value > nxt_val: 
                value, best_move = nxt_val, move
            if value <= alpha: 
                return best_move.score_for_red, best_move
            beta = min(beta, value)
    return value, best_move


def successors(colour, board): #make sure colour is case sensitive, board is board
    moves = []
    if board.stri  + board.turn in state_cache:
        for child in state_cache[board.stri  + board.turn]:
            c = Board(child.str, board, child.score_for_red)
            moves.append(c)
        return moves   
    new_board = [[],[],[],[],[],[],[],[]]    
    captures = []
    if colour == 'r':
        opp = ['b','B']
        coords = board.red
    else:      
        opp = ['r','R']
        coords = board.black
    for i in range(0, 8):
        for j in range(0, 8):
            new_board[i].append(board.str[i][j])
    for coord in coords:
        c = board.str[coord[0]][coord[1]]
        if c == 'r':
            pos_x = [-1,-1]
            pos_y = [1,-1]
        elif c == 'R':
            pos_x = [-1,-1,1,1]
            pos_y = [1,-1,1,-1]
        elif c == 'b':
            pos_x = [1,1]
            pos_y = [1,-1]
        elif c == 'B':
            pos_x = [1,1,-1,-1]
            pos_y = [1,-1,1,-1]
        for i in range(0, len(pos_x)):
            board_t = find_move(board, pos_x[i], pos_y[i], new_board, coord, opp, pos_x, pos_y)
            if board_t[0] is not None and board_t[1] == 0:
                moves.append(board_t[0])
            elif board_t[0] is not None and board_t[1] == 1:
                captures.append(board_t[0])
    if captures != []:
        state_cache[board.stri + board.turn] = captures
        return captures
    state_cache[board.stri + board.turn] = moves
    return moves


def find_move(board, x, y, new_board, coord, opp, posx, posy):
    new_board = [[],[],[],[],[],[],[],[]]
    for i in range(0, 8):
        for j in range(0, 8):
            new_board[i].append(board.str[i][j])
    pos_x = coord[0]
    pos_y = coord[1]
    c = new_board[pos_x][pos_y]
    if pos_x + x < 0 or pos_x + x > 7 or  pos_y + y < 0 or pos_y + y > 7:
        return (None, 0)
    elif board.str[pos_x + x][pos_y + y] == '.':
        new_board[pos_x][pos_y] = '.'
        if pos_x + x == 0 and c == 'r':
            new_board[pos_x + x][pos_y + y] = 'R'
        elif pos_x + x == 7 and c == 'b':
            new_board[pos_x + x][pos_y + y] = 'B'
        else:
            new_board[pos_x + x][pos_y + y] = c
        return (Board(new_board, board),0)
    elif pos_x + 2*x < 0 or pos_x + 2*x > 7 or  pos_y + 2*y < 0 or pos_y + 2*y > 7:
        return (None, 0)
    elif board.str[pos_x + x][pos_y + y] in opp and new_board[pos_x + 2*x][pos_y + 2*y] == '.':
        if pos_x + 2*x == 0 and c == 'r':
            new_board[pos_x + 2*x][pos_y + 2*y] = 'R'
        elif pos_x + 2*x == 7 and c == 'b':
            new_board[pos_x + 2*x][pos_y + 2*y] = 'B'
        else:
            new_board[pos_x + 2*x][pos_y + 2*y] = c
        new_board[pos_x][pos_y] = '.'
        new_board[pos_x + x][pos_y + y] = '.'
        new_board = Board(new_board, board)
        new_board = double_jump(new_board, opp, pos_x + 2*x, pos_y + 2*y, posx, posy, board)
        return (new_board, 1)
    return (None, 0)


def double_jump(board, opp, pos_x, pos_y, x, y, og_board):
    new_board = [[],[],[],[],[],[],[],[]]
    for i in range(0, 8):
        for j in range(0, 8):
            new_board[i].append(board.str[i][j])
    new_board = Board(new_board, og_board)
    for i in range(0, len(x)):
        if 7 >= pos_x + 2*x[i] >= 0 and 7 >= pos_y + 2*y[i] >= 0 and board.str[pos_x + x[i]][pos_y + y[i]] in opp and new_board.str[pos_x + 2*x[i]][pos_y + 2*y[i]] == '.':
            c = board.str[pos_x][pos_y]
            new_board.str[pos_x][pos_y] = '.'
            new_board.str[pos_x + x[i]][pos_y + y[i]] = '.'
            if pos_x + 2*x[i] == 0 and c == 'r':
                new_board.str[pos_x + 2*x[i]][pos_y + 2*y[i]] = 'R'
            elif pos_x + 2*x[i] == 7 and c == 'b':
                new_board.str[pos_x + 2*x[i]][pos_y + 2*y[i]] = 'B'
            else:
                new_board.str[pos_x + 2*x[i]][pos_y + 2*y[i]] = c            
            new_board = double_jump(new_board, opp, pos_x + 2*x[i], pos_y + 2*y[i], x, y, og_board)
    return new_board


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])