from random import choice

class ReversiGame:
    '''
    This object stores the current state of an Reversi/Othello board --
    the placement of pieces, the size of the board, and the current
    player.

    Attributes:
    self.height: Vertical size of the board. Always even.
    self.width: Horizontal size of board. Always even.
    self.board: The board, *FROM THE PERSPECTIVE OF THE CURRENT PLAYER.*
        1 means current player's piece, -1 means enemy player's piece,
        0 means empty space.
    self.curr_player: The current player. 1 is white, -1 is black.
    self.move_dict: Keys are (x,y) tuples for every square on the board.
        move_dict[(x,y)] is a list of (i,j) tuples that would be flipped if
        the current player played at (x,y). Empty iff (x,y) is an invalid move.
    self.possible_moves: List of (x,y) tuples with nonempty value in move_dict.
        These are the squares where the current player can play.

    '''
    def __init__(self, height, width):
        self.height = height
        self.width = width
        if self.height % 2 or self.width % 2:
            raise ValueError('Board dimensions must be even.')
        self.board=[[0 for i in range(self.width)] for j in range(self.height)]

        #Place the initial four pieces
        self.board[self.height//2-1][self.width//2-1]=1
        self.board[self.height//2][self.width//2-1]=-1
        self.board[self.height//2-1][self.width//2]=-1
        self.board[self.height//2][self.width//2]=1

        self.curr_player = 1
        self.move_dict = {(x,y):set() for x in range(self.height)
            for y in range(self.width)}
        self.possible_moves = []
        self.update_move_dict()

    def update_move_dict(self):
        '''
        Loop through all squares in the board, checking which pieces would get
        flipped if the current player played there. Updates both move_dict and
        possible_moves.

        '''
        self.move_dict={(x,y):set() for x in range(self.height)
            for y in range(self.width)}
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
            (0, 1), (1, -1), (1, 0), (1, 1)]
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j]==0:
                    for h,v in directions:
                        flipped = set()
                        cursor_i=i+h
                        cursor_j=j+v
                        if (    cursor_i<0 or
                                cursor_i>self.height-1 or
                                cursor_j<0 or
                                cursor_j>self.width-1
                        ):
                            continue #Stop if we'd go off the board
                        while self.board[cursor_i][cursor_j]==-1:
                            if (
                                    cursor_i+h<0 or
                                    cursor_i+h>self.height-1 or
                                    cursor_j+v<0 or
                                    cursor_j+v>self.width-1
                            ):
                                break #stop if we'd go off the board
                            else:
                                flipped.add((cursor_i, cursor_j))
                                cursor_i += h
                                cursor_j += v

                        if self.board[cursor_i][cursor_j] == 1:
                            #if we've got ox...xo, we're done, flip enemies
                            self.move_dict[(i,j)].update(flipped)
        self.possible_moves = [x for x in self.move_dict.keys()
            if len(self.move_dict[x])!=0]

    def print_board(self):
        '''
        Print the board in a non-fancy way. No line/column numbers,
        no cool unicode shenanigans.

        '''
        for i,x in enumerate(self.board):
            out=[]
            for j,y in enumerate(x):
                if y==1:
                    out.append('o')
                elif y==-1:
                    out.append('x')
                elif y==0 and len(self.move_dict[(i,j)])!=0:
                    out.append('?')
                else:
                    out.append('.')
            print(''.join(out))

    def fancy_print(self):
        '''
        Print the board with nice Unicode formatting, and line and column
        markers.
        Note that in a white-on-black environment, the first player will
        be the 'black' pieces.
        '''
        if self.curr_player==-1:
            self.flip_board()
        alpha=u'a b c d e f g h i j k l m n o p q r s t u v w x y z '
        print('   '+alpha[:2*self.width])
        for i,x in enumerate(self.board):
            if i<10:
                out=[u' ',str(i), u' ']
            else:
                out=[str(i),u' ']
            for j,y in enumerate(x):
                if y==1:
                    out.append(u'\u25cb ')
                elif y==-1:
                    out.append(u'\u25cf ')
                elif y==0 and len(self.move_dict[(i,j)])!=0:
                    out.append(u'\u2217 ')
                else:
                    out.append(u'\u00b7 ')
            print(''.join(out))
        if self.curr_player == -1:
            self.flip_board()

    def make_move(self, i,j):
        '''
        If (i,j) is a valid move, the current player makes that move.
        This updates the board as well as move_dict and possible_moves,
        and changes the current player.
        If (i,j) is not valid, raise an exception.
        '''
        if i==None and j == None:
            self.flip_board()
            self.curr_player *= -1
            return
        if i<0 or i>self.height-1 or j<0 or j>self.width-1:
            raise IndexError('Coordinates out of bounds')
        if len(self.move_dict[(i,j)])==0:
            raise ValueError('Not a valid move')
        self.board[i][j]=1
        for x,y in self.move_dict[(i,j)]:
            self.board[x][y] = 1
        self.flip_board()
        self.update_move_dict()
        self.curr_player *= -1

    def flip_board(self):
        '''
        Just change every value on the board to its opposite value.
        Don't use this function on its own.
        '''
        self.board=[[-i for i in j] for j in self.board]

    def check_winner(self):
        '''
        Check if someone has won, and whom.
        Returns (False,0) if no winner yet.
        Returns (True, 1) if first player win
        Returns (True, -1) if second player win
        Returns (True, 0) if game is a draw
        '''
        winner = 0
        opp_out_of_moves = False
        if len(self.possible_moves) == 0:
            curr_out_of_moves = True
            self.flip_board()
            self.update_move_dict()
            if len(self.possible_moves) == 0:
                opp_out_of_moves = True
            self.flip_board()
            self.update_move_dict()
        if opp_out_of_moves:
            s = sum([sum(x) for x in self.board])
            if s>0:
                return (True, self.curr_player)
            elif s<0:
                return (True, -self.curr_player)
            else:
                return (True, 0)
        return (False, 0)

alphabet='abcdefghijklmnopqrstuvwxyz'

def play_game(size_i, size_j, two_players = False):
    '''
    This is a testing function. play_game(i,j) throws you into a game against
    a very crude AI that just takes random moves, on a size (i,j) board.
    if two_players=True, instead alternate between players.
    '''
    hmoves = {x:y for y,x in enumerate(alphabet[:size_i])}
    vmoves = {str(k):k for k in range(size_j)}
    testgame = ReversiGame(size_i, size_j)

    while True:
        print('\033c')
        testgame.fancy_print()
        print('\n')
        good_flag = False

        done, who_won = testgame.check_winner()
        if done:
            print(u'?\u25cb\u25cf'[who_won], 'wins!')
            return

        if testgame.curr_player==1:
            pmarker = u'\u25cb'
        else:
            pmarker = u'\u25cf'

        while not good_flag:
            in_move = input(pmarker + " 's Move: ")
            if in_move == 'pass':
                out_move=(None, None)
                good_flag = True
            elif in_move == 'quit':
                return
            elif in_move == '':
                continue
            else:
                if (in_move[-1] in vmoves) and (in_move[:-1] in hmoves):
                    out_move=(vmoves[in_move[-1]], hmoves[in_move[:-1]])
                    if out_move in testgame.possible_moves:
                        good_flag = True

        testgame.make_move(*out_move)
        if not two_players:
            if len(testgame.possible_moves) == 0:
                testgame.make_move(None, None)
            else:
                testgame.make_move(*choice(testgame.possible_moves))
