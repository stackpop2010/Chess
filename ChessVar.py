# Name: Patricia Stackpole
# GitHub Username: Stackpop2010
# Date: 14MAR2024
# Description: "Hunter Falcon" Chess variant game. This game does not include check, checkmate, promoting pawns, or en
# pasant capture. Game includes "Hunter" and "Falcon" fairy pieces. Approach is to use one class to save memory.

class ChessVar:
    """
    Creates class with methods to play our chess variation (Hunter-Falcon). This will not take user inputs, but
    arguments passed into methods. WIll check for illegal moves, track the player's turn, and game state. Game ends with
    capture of the king. No check or checkmate status will be used.
    """

    def __init__(self):
        """
        Initializes the chess game. Does not take arguments. Initializes game state to unfinished. Sets up the board to
        default state with reserve fairy pieces. Sets white_turn to True
        """
        self._game_state = "UNFINISHED"  # neither player has won yet
        self._white_turn = True  #white goes first in standard chess
        self._black_turn = False
        self._spaces = {'a1': 'wr1', 'a2': 'wp1', 'a3': None, 'a4': None, 'a5': None, 'a6': None, 'a7': 'bp1',
                        'a8': 'br1',
                        'b1': 'wn1', 'b2': 'wp2', 'b3': None, 'b4': None, 'b5': None, 'b6': None, 'b7': 'bp2',
                        'b8': 'bn2',
                        'c1': 'wb1', 'c2': 'wp3', 'c3': None, 'c4': None, 'c5': None, 'c6': None, 'c7': 'bp3',
                        'c8': 'bb1',
                        'd1': 'wq', 'd2': 'wp4', 'd3': None, 'd4': None, 'd5': None, 'd6': None, 'd7': 'bp4',
                        'd8': 'bq',
                        'e1': 'wk', 'e2': 'wp5', 'e3': None, 'e4': None, 'e5': None, 'e6': None, 'e7': 'bp5',
                        'e8': 'bk',
                        'f1': 'wb2', 'f2': 'wp6', 'f3': None, 'f4': None, 'f5': None, 'f6': None, 'f7': 'bp6',
                        'f8': 'bb2',
                        'g1': 'wn2', 'g2': 'wp7', 'g3': None, 'g4': None, 'g5': None, 'g6': None, 'g7': 'bp7',
                        'g8': 'bn2',
                        'h1': 'wr2', 'h2': 'wp8', 'h3': None, 'h4': None, 'h5': None, 'h6': None, 'h7': 'bp8',
                        'h8': 'br2'}

        self._pawns = {"wp1": 0, "wp2": 0, "wp3": 0, "wp4": 0, "wp5": 0, "wp6": 0, "wp7": 0, "wp8": 0,
                       "bp1": 0, "bp2": 0, "bp3": 0, "bp4": 0, "bp5": 0, "bp6": 0, "bp7": 0, "bp8": 0}

        self._white_set = ["wr1", "wn1", "wb1", "wq", "wk", "wb2", "wn2", "wr2", "wp1", "wp2", "wp3", "wp4", "wp5",
                           "wp6", "wp7", "wp8", "wh", "wf"]

        self._black_set = ["br1", "bn1", "bb1", "bq", "bk", "bb2", "bn2", "br2", "bp1", "bp2", "bp3", "bp4", "bp5",
                           "bp6", "bp7", "bp8", "bh", "bf"]

        self._white_fairy = 2
        self._black_fairy = 2
        self._fairy_pieces = ["bh", "bf", "wh", "wf"]
        # used to track captured queens, bishops, knights, and rooks only, called in enter_fairy_piece()
        self._captured_black_pieces = []
        self._captured_white_pieces = []

    def get_game_state(self):
        """
        Takes no arguments, simply returns the game state. Will be used in other functions to see if the game is over.
        """
        return self._game_state

    def set_game_state(self, winner):
        """
        Will be used to change the game state if a king is captured. The only valid inputs here should be "black" and
        "white."
        """
        if winner.upper() == "BLACK":
            self._game_state = "BLACK_WON"
        if winner.upper() == "WHITE":
            self._game_state = "WHITE_WON"

    def make_move(self, start_space, end_space):
        """
        There is a lot going on in this function. This will allow the "player" to make a move. It will need to do the
        following a) check if the game state is "UNFINISHED", and if spots are on the board, and start spot is
        not the same as end spot b) verify the player is the owner of the piece c) make sure the move is legal d) ensure
        there are no collisions or obstructing pieces and finally e) to update the state of the board after all the
        preceding conditions have been met. Then, f) we check if any piece has been captured and g) if the win
        conditions have been met We will use the h) "set_game_state()" function if needed and change if someone has one
        i) update who's turn it is

        """

        #print(start_space,"to", end_space) #used for testing only

        start_space = start_space.lower()  #in case someone inputs "A2" or similar
        end_space = end_space.lower()

        #requirment a from docstring, is the game still going?
        if self.get_game_state() != "UNFINISHED":
            return False  #can't keep playing when the game is already won!

        #requirement a from above, ensures the space is actually on the board
        if start_space.lower() not in self._spaces or end_space.lower() not in self._spaces:
            return False

        # requirement a from above, ensures the start and end space are not the same
        if start_space == end_space:
            return False

        if self._spaces[start_space] is None:  #can't move a piece that doesn't exist
            return False


        #requirment b from docstring, is it the turn of the player trying to move?
        #should also return false if there is no piece in the starting space because
        # "None" shouldn't be in the set of pieces
        if self._white_turn == True and self._spaces[start_space] in self._black_set:
            return False
        if self._black_turn == True and self._spaces[start_space] in self._white_set:
            return False
        if self._white_turn == True and self._spaces[start_space] in self._white_set:
            pass
        if self._black_turn == True and self._spaces[start_space] in self._black_set:
            pass

        piece = self._spaces[start_space]
        #requirments c and d from docstring
        if self.legal_check(piece, start_space, end_space) == False:
            return False
        else:
            pass

        # requirment f from docstring, use this to check for captured spots, returns "None" if empty spot on board
        captured = self._spaces[end_space]

        #requirment e from docstring, updates the board
        piece = self._spaces[start_space]
        self.update_board(captured, piece, start_space, end_space)

        #requirements g and h from above
        if "bk" not in self._black_set:
            self.set_game_state("WHITE")

        if "wk" not in self._white_set:
            self.set_game_state("BLACK")

        #requirement i from doc string, update the player turn
        if self._white_turn == True:
            self._white_turn = False
            self._black_turn = True
        else:
            self._white_turn = True
            self._black_turn = False

        #self.print_board()
        return True


    def capture_pieces(self, captured):
        """
        removes a piece from play if captured
        """

        fairy_caps = ["wq", "bq", "wr1", "wr2", "wb1", "wb2", "br1", "br2", "bb1", "bb2", "wn1", "wn2", "bn1","bn2"]

        if captured not in self._white_set and captured not in self._black_set:
            return False

        if captured in self._white_set:
            self._white_set.remove(captured)
            if captured in fairy_caps:
                self._captured_white_pieces.append(captured)

        if captured in self._black_set:
            self._black_set.remove(captured)
            if captured in fairy_caps:
                self._captured_black_pieces.append(captured)

    def update_board(self, capture, piece, init_pos, new_pos):
        """
        used to move pieces on board or remove from board.
        """

        if capture is None and self._spaces[new_pos] is None and piece in self._fairy_pieces:
            self._spaces[new_pos] = piece

        if capture is None and self._spaces[new_pos] is None:
            self._spaces[init_pos] = None
            self._spaces[new_pos] = piece

        if capture != None:
            self._spaces[init_pos] = None
            captured = self._spaces[new_pos]
            self.capture_pieces(captured)
            self._spaces[new_pos] = piece

    def legal_check(self, piece, start_space, end_space):

        """
        Checks if your moves are legal for a given piece will return "False" to make_move if an invalid move is made
        pieces may not move off the board does not account for capture, this is done in a different function
        only makes sure it's not moving to an illegal capture

        """
        #makes sure player isn't capturing their own piece
        if self._spaces[end_space] is None:
            pass  #no capture at all happening
        if self._spaces[start_space] in self._white_set and self._spaces[end_space] in self._white_set:
            return False  #illegal capture of own piece, don't need to keep going
        if self._spaces[start_space] in self._black_set and self._spaces[end_space] in self._black_set:
            return False  #illegal capture of own piece, don't need to keep going

        # the built in ord() function will be used to convert the spaces from chess notation to ordinals so it is
        # easier to calculate moves
        start_row = (ord(start_space[1]) - ord('a'))
        start_col = (ord(start_space[0]) - ord('1'))
        end_row = (ord(end_space[1]) - ord('a'))
        end_col = (ord(end_space[0]) - ord('1'))

        #claculate the differences using ords from above
        row_mvmt =abs(start_row-end_row)
        col_mvmt =abs(start_col-end_col)

        # Calculate the row and column movement directions, but only if they move, will be used later
        if row_mvmt != 0:
            row_direction = abs(end_row - start_row) // abs(end_row - start_row)
        if col_mvmt != 0:
            col_direction = abs(end_col - start_col) // abs(end_col - start_col)

        #converts our board dictionary to ordinals so that they can be checked using ord() functions
        ord_board = {}
        for space, entry in self._spaces.items():
            if entry is not None:
                ord_col = (ord(space[0]) - ord('1'))
                ord_row = (ord(space[1]) - ord('a'))

                temp_key = (ord_col, ord_row)
                ord_board[temp_key] = entry

            if entry is None:
                ord_col = (ord(space[0]) - ord('1'))
                ord_row = (ord(space[1]) - ord('a'))

                temp_key = (ord_col, ord_row)
                ord_board[temp_key] = entry

        #king check
        if piece == "bk" or piece == "wk":
            if col_mvmt <= 1 and row_mvmt <=1:
                return True
            return False

        #queen check
        if piece == "wq" or piece == "bq":
            #moves any direction, any space
            if abs(row_mvmt) != abs(col_mvmt) and (abs(row_mvmt) >= 1 and abs(col_mvmt) >=1):
                return False
            if self.check_obstructions(start_space, end_space) == False:
                return False
            return True

        #check pawns
        if piece in self._pawns:
            if "1" in start_space or "8" in start_space:
                return False  #pawn can't move or be promoted
            if piece in self._white_set and start_row > end_row:
                return False  #prevent backwards movement
            if piece in self._black_set and start_row < end_row:
                return False  #prevent backwards movement
            if row_mvmt == 0 and col_mvmt != 0:  #can't move to the side
                return False

            #may move two spots on first turn, or diagonal capture
            if self._pawns[piece] == 0:
                if row_mvmt > 2:
                    return False
                if col_mvmt== 1 and row_mvmt == 1 and self._spaces[end_space] is not None:
                    return True  #this is a diagonal capture, we already checked if capture is legal
                if col_mvmt == 1 and row_mvmt == 1 and self._spaces[end_space] is None:
                    return False  #diagnol moves only legal for capture
                if (row_mvmt == 1 or row_mvmt == 2) and self._spaces[end_space] is None:
                    return True
                if (row_mvmt == 1 or row_mvmt == 2) and self._spaces[end_space] is not None:
                    return False
                if self.check_obstructions(start_space, end_space) == False:
                    return False
                #add a 1 to the pawn dictionary key pair so that it can't move multiple spaces again
                self._pawns[piece] = 1
                return True

            if self._pawns[piece] != 0:
                if row_mvmt > 1:
                    return False

                if col_mvmt == 1 and row_mvmt == 1 and self._spaces[end_space] is None:
                    return False  #diagnol moves only legal for capture
                elif col_mvmt == 1 and row_mvmt == 1 and self._spaces[end_space] is not None:
                    return True #this is a diagonal capture, we already checked if capture is legal
                elif row_mvmt == 1 and self._spaces[end_space] is not None:
                    return False
                elif row_mvmt == 1 and self._spaces[end_space] is None:
                    return True #can move 1 spaces but can't capture
                else:
                    return False


        #rooks
        rooks = ["wr1", "wr2", "br1", "br2"]
        if piece in rooks:
            #can only move forwards and backwards, may not jump pieces
            #may only capture pieces of opposite color
            if abs(row_mvmt) == abs(col_mvmt):
                return False
            if abs(row_mvmt) >= 1 and  abs(col_mvmt) >=1:
                return False
            if self.check_obstructions(start_space, end_space) == False:
                return False
            return True

        #bishops
        bishops = ["wb1", "wb2", "bb1", "bb2"]
        if piece in bishops:
            if row_mvmt != col_mvmt:
                return False
            if self.check_obstructions(start_space, end_space) == False:
                return False
            return True

        #knights
        knights = ["wn1", "wn2", "bn1", "bn2"]
        if piece in knights:
            #may move in an L direcon (two left or right plus one up or down, or one left or right plus two up or down)
            #may jump pieces, so we do not check for obstructions
            #may only capture pieces of the opposite color, which was already checked at the beginning of this function
            if row_mvmt == 2 and col_mvmt == 1 or row_mvmt == 1 and col_mvmt == 2:
                return True
            return False

        #hunters
        hunters = ["bh","wh"]
        if piece in hunters:
            #can move forwards like rook but not sideways
            if end_row < start_row and start_col == end_col and piece in self._white_set:
                return False
            if end_row > start_row and start_col == end_col and piece in self._white_set:
                if self.check_obstructions(start_space, end_space) == False:
                    return False
                return True
            if end_row > start_row and start_col == end_col and piece in self._black_set:
                return False
            if end_row < start_row and start_col == end_col and piece in self._black_set:
                if self.check_obstructions(start_space, end_space) == False:
                    return False
                return True

            #can move backwards like bishop
            if end_row < start_row and piece in self._white_set:
                if col_mvmt != row_mvmt:
                    return False
                if col_mvmt == row_mvmt:
                    if self.check_obstructions(start_space, end_space) == False:
                        return False
                return True

            if end_row > start_row and piece in self._black_set:
                if col_mvmt != row_mvmt:
                    return False
                if col_mvmt == row_mvmt:
                    if self.check_obstructions(start_space, end_space) == False:
                        return False
                return True
            return False

        #falcons
        falcons = ["bf", "wf"]
        if piece in falcons:
            # can move backwards like rook but not sideways
            if end_row < start_row and start_col == end_col and piece in self._white_set:
                if self.check_obstructions(start_space, end_space) == False:
                    return False
                return True
            if end_row > start_row and start_col == end_col and piece in self._black_set:
                if self.check_obstructions(start_space, end_space) == False:
                    return False
                return True

            #can move forwards like bishop
            if end_row > start_row and piece in self._white_set:
                if col_mvmt == row_mvmt:
                    if self.check_obstructions(start_space, end_space) == False:
                        return False
                return True

            if end_row < start_row and piece in self._black_set:
                if col_mvmt == row_mvmt:
                    if self.check_obstructions(start_space, end_space) == False:
                        return False
                return True
            return False

        #if somehow nothing was met, there was an invalid piece or move
        return False

    def check_obstructions(self, start_space, end_space):
        """
        checks for obstructions and will return false if there is an obstruction
        """
        spots = self._spaces

        ord_board = {}
        for space, entry in spots.items():
            if entry is not None:
                ord_col = (ord(space[0]) - ord('1'))
                ord_row = (ord(space[1]) - ord('a'))

                temp_key = (ord_col, ord_row)
                ord_board[temp_key] = entry

            else:
                temp_key = (ord(space[0]) - ord('1'), ord(space[1]) - ord('a'))
                ord_board[temp_key] = entry

        # the built in ord() function will be used to convert the spaces from chess notation to ordinals so that it is
        # easier to calculate moves
        start_row =(ord(start_space[1]) - ord('a'))
        start_col = (ord(start_space[0]) - ord('1'))
        end_row = (ord(end_space[1]) - ord('a'))
        end_col = (ord(end_space[0]) - ord('1'))
        row_mvmt = abs(start_row - end_row)
        col_mvmt = abs(start_col - end_col)

        if start_col == end_col and start_row < end_row: #moving vertically up
            for i in range(start_row+1, end_row):
                if ord_board[start_col,i] is not None:
                    return False
            return True

        if start_col == end_col and start_row > end_row: # moving vertically down
            for i in range(start_row-1, end_row, -1):
                if ord_board[start_col,i] is not None:
                    return False
            return True

        if start_row == end_row and start_col < end_col: #moving horizontally to the right
            for i in range(start_col+1, end_col):
                if ord_board[i, start_row] is not None:
                    return False
            return True

        if start_row == end_row and start_col > end_col: #moving horizontally to the left
            for i in range(start_col-1, end_col, -1):
                if ord_board[i, start_row] is not None:
                    return False
            return True


        if col_mvmt == row_mvmt: #diags
            if start_col > end_col and start_row < end_row:  # moving up and left/NW
                j = row_mvmt-1
                while j >=1:
                    for i in range(start_row+1, end_row):
                        if (ord_board[start_col - j, start_row + j]) is not None:
                            return False
                        j = j - 1

            if start_col < end_col and start_row < end_row:  # moving up and right/NE
                j = row_mvmt-1
                while j >=1:
                    for i in range(start_col+1, end_col):
                        if (ord_board[start_col + j, start_row + j]) is not None:
                            return False
                        j = j - 1

            if start_col < end_col and start_row > end_row:  # moving down and right/SE
                j = row_mvmt-1
                while j >=1:
                    for i in range(start_col+1, end_col):
                        if (ord_board[start_col + j, start_row - j]) is not None:
                            return False
                        j = j - 1


            if start_col > end_col and start_row > end_row:  # moving down and left/SW
                j = row_mvmt
                while j >= 1:
                    for i in range(end_row, start_row):
                        if (ord_board[start_col - j, start_row - j]) is not None:
                            return False
                        j = j - 1

        return True #no obstructions found


    def enter_fairy_piece(self, piece, square):
        """
        checks rules for fairy piece entry: only in home ranks and unoccupied spots
        """
        valid_pieces = ["F", "H", "f", "h"]

        #white falcon 'F', white hunter 'H', black falcon 'f', black hunter 'h'
        if piece not in valid_pieces:
            return False
        if (piece == "F" or piece == "H") and self._white_fairy == 0:
            return False
        if (piece == "f" or piece == "h") and self._black_fairy == 0:
            return False
        if (piece == "F" or piece == "H") and self._white_turn == False:
            return False
        if (piece == "f" or piece == "h") and self._black_turn == False:
            return False
        if (piece == "F" and "wf" not in self._white_set) or (piece == "F" and "wf" in self._spaces.values()):
            return False
        if (piece == "H" and "wh" not in self._white_set) or (piece == "H" and "wh" in self._spaces.values()):
            return False
        if (piece == "f" and "bf" not in self._black_set) or (piece == "f" and "bf" in self._spaces.values()):
            return False
        if (piece == "h" and "bh" not in self._black_set) or (piece == "h" and "bh" in self._spaces.values()):
            return False
        if self._spaces[square] is not None:
            return False

        white_rank = ['a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1', 'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2']
        black_rank = ['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7', 'a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8']

        if square in white_rank and piece in self._white_set:
            pass
        if square not in white_rank and piece in self._white_set:
            return False
        if square in black_rank and piece in self._black_set:
            pass
        if square not in black_rank and piece in self._black_set:
            return False


        if ((piece == "F" or piece == "H" and self._white_fairy == 2 and len(self._captured_white_pieces) >= 1) or
                (piece == "F" or piece == "H" and self._white_fairy == 1 and len(self._captured_white_pieces) >= 2)):
        # allows first placement of white fairy by virtue of at least one non pawn being missing from list

            if self._spaces[square] is not None:
                return False
            if self._white_turn is False:
                return False
            if square not in white_rank:
                return False
            self._white_fairy = self._white_fairy - 1
            self._white_turn = False
            self._black_turn = True
            if piece == "F":
                rpiece = "wf"
            if piece == "H":
                rpiece = "wh"
            self.update_board(None, rpiece, square, square)
            return True

        if ((piece == "f" or piece == "h" and self._black_fairy == 2 and len(self._captured_black_pieces) >= 1) or
                (piece == "f" or piece == "h" and self._black_fairy == 1 and len(self._captured_black_pieces) >= 2)):
        # allows first placement of white fairy by virtue of at least one non pawn being missing from list

            if self._spaces[square] is not None:
                return False
            if self._black_turn is False:
                return False
            if square not in black_rank:
                return False
            self._black_fairy = self._black_fairy - 1
            self._white_turn = True
            self._black_turn = False
            if piece == "f":
                rpiece = "bf"
            if piece == "h":
                rpiece = "bh"
            self.update_board(None, rpiece, square, square)
            return True

        return False #if other criteria are not met

    def print_board(self):
        """
        #Not part of the program for regular play, will be used to visualize
        #the board state during testing
        """

        if self._white_turn == True:
            print("white turn")
        if self._black_turn == True:
            print("black turn")
        print(self.get_game_state())

        row_8 = [self._spaces["a8"], self._spaces["b8"], self._spaces["c8"], self._spaces["d8"],
                 self._spaces["e8"], self._spaces["f8"], self._spaces["g8"], self._spaces["h8"]]
        row_7 = [self._spaces["a7"], self._spaces["b7"], self._spaces["c7"], self._spaces["d7"],
                 self._spaces["e7"], self._spaces["f7"], self._spaces["g7"], self._spaces["h7"]]
        row_6 = [self._spaces["a6"], self._spaces["b6"], self._spaces["c6"], self._spaces["d6"],
                 self._spaces["e6"], self._spaces["f6"], self._spaces["g6"], self._spaces["h6"]]
        row_5 = [self._spaces["a5"], self._spaces["b5"], self._spaces["c5"], self._spaces["d5"],
                 self._spaces["e5"], self._spaces["f5"], self._spaces["g5"], self._spaces["h5"]]
        row_4 = [self._spaces["a4"], self._spaces["b4"], self._spaces["c4"], self._spaces["d4"],
                 self._spaces["e4"], self._spaces["f4"], self._spaces["g4"], self._spaces["h4"]]
        row_3 = [self._spaces["a3"], self._spaces["b3"], self._spaces["c3"], self._spaces["d3"],
                 self._spaces["e3"], self._spaces["f3"], self._spaces["g3"], self._spaces["h3"]]
        row_2 = [self._spaces["a2"], self._spaces["b2"], self._spaces["c2"], self._spaces["d2"],
                 self._spaces["e2"], self._spaces["f2"], self._spaces["g2"], self._spaces["h2"]]
        row_1 = [self._spaces["a1"], self._spaces["b1"], self._spaces["c1"], self._spaces["d1"],
                 self._spaces["e1"], self._spaces["f1"], self._spaces["g1"], self._spaces["h1"]]
        print_list = [row_8, row_7, row_6, row_5, row_4, row_3, row_2, row_1]

        for i in print_list:
            k = []
            for j in i:

                if j != None:
                    if len(j) < 3:
                        temp = "[" + j + " ]"
                        temp = str(temp)
                        k.append(temp)
                    else:
                        temp = "[" + j + "]"
                        temp = str(temp)
                        k.append(temp)
                else:
                    k.append("[   ]")
            print(k)






