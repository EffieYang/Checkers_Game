'''
Xiaoxi Yang
Code for project_Checkers Game
'''
import random

NUM_SQUARES = 8
SQUARE = 50
INITIAL_ROWS = 3
BLACK = "black"
RED = "dark red"
EMPTY = "empty"
KING = "king"
PLAYER = [BLACK, RED]
SQUARE_COLORS = ("light gray", "white")


class GameState:
    '''
    Class -- GameState
        Represents the game status change of checkerboard
    Attributes:
        squares -- A nested list storing the state of each square on the board
        current_player -- A String, use piece colors to represent who is
        the current player
        possible_moves -- A list storing all locations of possible valid non
        capture moves of human player's piece
        possible_capture_moves -- A list storing all locations of possible
        valid capture moves of huamn player's piece
        movable_pieces -- A list storing all locations of human player's
        possible valid movable pieces
        movable_piece = A list storing the location of human player's selected
        movable piece
    Methods:
        set_squares -- Set the initial state of each square on the board
        click_position -- Calculate corresponding row and col by giving
        coordinates
        click_validation -- Check if the click position(piece) belongs to the
        current player, and also this piece is movable
        move_direction -- Calculate which move direction could be made
        non_capture_move -- Calculate all the possible non capture moves of
        current piece
        capture_move -- Calculate all possible capture moves of current piece
        move_options -- Calculate all possible moves(capture and non capture)
        and possible movable pieces of specific player -- human/computer
        movable_validation -- Calculate all the valid movable pieces of human
        player (must capture if possible)
        valid_move -- Check if the selected move is valid
        update_squares -- Update the state of each square on the board in
        nested list after human player's move
        king_upgrade -- Upgrage the piece as king if it arrives the last row
        of opponent
        storage_reset -- Reset human player's movable and possible moves list
        as empty
        switch_turn -- Switch the current player
        computer_move -- Calculate which move to make for computer player
        computer_update_squares -- Update the state of each square on the
        board in nested list after computer player's move
        game_end -- Check if the game ends or not
    '''

    def __init__(self):
        '''
        Constructor -- create a new instance of GameState
        Parameters:
            self -- the current GameState object
        '''
        self.squares = [[0 for _ in range(NUM_SQUARES)] for _ in
                        range(NUM_SQUARES)]
        self.set_squares()
        self.current_player = PLAYER[0]
        self.possible_moves = []
        self.possible_capture_moves = []
        self.movable_pieces = []
        self.movable_piece = []

    def set_squares(self):
        '''
        Method -- set_squares
            Set the initial state of each square on the board
        Parameter:
            self -- The current GameState object
        Returns:
            Nothing
        '''
        for row in range(NUM_SQUARES):
            for col in range(NUM_SQUARES):
                color = EMPTY
                if row % 2 != col % 2 and row < INITIAL_ROWS:
                    color = BLACK
                elif row % 2 != col % 2 and row > INITIAL_ROWS + 1:
                    color = RED
                self.squares[row][col] = color

    def click_position(self, x, y):
        '''
        Method -- click_position
            Calculate corresponding row and col by giving coordinates
        Parameters:
            self -- the current GameState object
            x -- the x-coordinate when a click happened
            y -- the y-coordinate when a click happened
        Returns:
            Corresponding row, col and if the click is within the board,
            returns row and col as -1 and inboard as False if the click is
            out of the board
        '''
        board_limit = [-1 * NUM_SQUARES//2 * SQUARE, NUM_SQUARES//2 * SQUARE]
        inboard = True
        if board_limit[0] <= x <= board_limit[1] \
           and board_limit[0] <= y <= board_limit[1]:
            row = int(y // SQUARE + NUM_SQUARES // 2)
            col = int(x // SQUARE + NUM_SQUARES // 2)
            return row, col, inboard
        else:
            inboard = False
            return -1, -1, inboard

    def click_validation(self, row, col):
        '''
        Method -- click_validation
            Check if the click position(piece) belongs to the current player,
            and also this piece is movable
        Parameters:
            self -- the current GameState object
            row -- the current click's row position
            col -- the current click's col position
        Returns:
            True or False if the click position(piece) belongs to the current
            player, meanwhile this piece is movable
        '''
        piece = (row, col)
        self.movable_pieces = self.movable_validation()
        if 0 <= row < NUM_SQUARES and 0 <= col < NUM_SQUARES\
           and row % 2 != col % 2:
            return ((self.squares[row][col] == self.current_player or
                    self.squares[row][col] == self.current_player + KING)
                    and piece in self.movable_pieces)

    def move_direction(self, row, col):
        '''
        Method -- move_direction
            Calculate which move direction could be made
        Parameters:
            self -- the current GameState object
            row -- the current click's row position
            col -- the current click's col position
        Returns:
            A list storing the possible move directions of current piece
        '''
        direction = []
        if self.squares[row][col] == BLACK:
            direction = [[1, -1], [1, 1]]
        elif self.squares[row][col] == RED:
            direction = [[-1, -1], [-1, 1]]
        elif (self.squares[row][col] == BLACK + KING
              or self.squares[row][col] == RED + KING):
            direction = [[1, -1], [1, 1], [-1, -1], [-1, 1]]
        return direction

    def non_capture_move(self, row, col):
        '''
        Method -- non_capture_move
            Calculate all the possible non capture moves of current piece
        Parameters:
            self -- the current GameState object
            row -- the current click's row position
            col -- the current click's col position
        Returns:
            A list storing the locations of all possible non capture moves of
            current piece
        '''
        possible_moves = []
        direction = self.move_direction(row, col)
        for item in direction:
            new_row, new_col = row + item[0], col + item[1]
            if (0 <= new_row < NUM_SQUARES and 0 <= new_col < NUM_SQUARES and
               self.squares[new_row][new_col] == EMPTY):
                possible_moves.append((new_row, new_col))
        return possible_moves

    def capture_move(self, row, col):
        '''
        Method -- capture_move
            Calculate all the possible capture moves of current piece
        Parameters:
            self -- the current GameState object
            row -- the current click's row position
            col -- the current click's col position
        Returns:
            A list storing the locations of all possible capture moves of
            current piece
        '''
        possible_capture_moves = []
        direction = self.move_direction(row, col)
        for item in direction:
            new_row, new_col = row + item[0], col + item[1]
            if (0 <= new_row < NUM_SQUARES and 0 <= new_col < NUM_SQUARES
               and self.squares[new_row][new_col] != EMPTY and
               self.squares[new_row][new_col] != self.current_player and
               self.squares[new_row][new_col] != self.current_player + KING):
                capture_row, capture_col = new_row + item[0], new_col + item[1]
                if (0 <= capture_row < NUM_SQUARES and
                   0 <= capture_col < NUM_SQUARES and
                   self.squares[capture_row][capture_col] == EMPTY):
                    possible_capture_moves.append((capture_row, capture_col))
        return possible_capture_moves

    def move_options(self):
        '''
        Method -- move_options
            Calculate all the possible moves(capture and non capture) and
            possible movable pieces of specific player -- human/computer
        Parameters:
            self -- the current GameState object
        Returns:
            Four lists storing the locations of all possible non capture
            capture moves, corresponding movable pieces, all possible capture
            capture moves, and corresponding movable pieces
        '''
        color = ""
        if self.current_player == RED:
            color = [RED, RED + KING]
        if self.current_player == BLACK:
            color = [BLACK, BLACK + KING]
        non_capture_options = []
        capture_options = []
        non_capture_movable_options = []
        capture_movable_options = []
        for row in range(0, NUM_SQUARES):
            for col in range(0, NUM_SQUARES):
                if (self.squares[row][col] == color[0] or
                   self.squares[row][col] == color[1]):
                    possible_non_capture_moves =\
                        self.non_capture_move(row, col)
                    possible_capture_moves = self.capture_move(row, col)
                    for item in possible_non_capture_moves:
                        non_capture_options.append(item)
                        non_capture_movable_options.append((row, col))
                    for item in possible_capture_moves:
                        capture_options.append(item)
                        capture_movable_options.append((row, col))
        return non_capture_options, non_capture_movable_options,\
            capture_options, capture_movable_options

    def movable_validation(self):
        '''
        Method -- movable_validation
            Calculate all the valid movable pieces of human player (must
            capture if possible)
        Parameters:
            self -- the current GameState object
        Returns:
            A list storing all locations of human player's possible valid
            movable pieces
        '''
        player_non_capture_moves, player_non_capture_movable_options,\
            player_capture_options, player_capture_movable_options \
            = self.move_options()
        if len(player_capture_options) > 0:
            self.movable_pieces = player_capture_movable_options
        elif len(player_non_capture_moves) > 0:
            self.movable_pieces = player_non_capture_movable_options
        return self.movable_pieces

    def valid_move(self, move_row, move_col):
        '''
        Method -- valid_move
            Check if the selected move is valid
        Parameters:
            self -- the current GameState object
            move_row -- the selected move's row position
            move_col -- the selected move's col position
        Returns:
            True or False if the selected move is valid or not
        '''
        move = (move_row, move_col)
        if move in self.possible_capture_moves:
            return True
        elif not self.possible_capture_moves:
            if move in self.possible_moves:
                return True
        return False

    def update_squares(self, move_row, move_col):
        '''
        Method -- update_squares
            Update the state of each square on the board in nested list after
            human player's move
        Parameters:
            self -- the current GameState object
            move_row -- the selected move's row position
            move_col -- the selected move's col position
        Returns:
            A nested list storing the newest state of each square on the board
        '''
        if self.movable_piece:
            movable_row, movable_col = self.movable_piece[0],\
                self.movable_piece[1]
            if self.possible_capture_moves:
                delete_row, delete_col = (move_row + movable_row) // 2,\
                    (move_col + movable_col) // 2
                self.squares[delete_row][delete_col] = EMPTY
                self.squares[movable_row][movable_col],\
                    self.squares[move_row][move_col] =\
                    self.squares[move_row][move_col],\
                    self.squares[movable_row][movable_col]
            elif not self.possible_capture_moves and self.possible_moves:
                self.squares[movable_row][movable_col],\
                    self.squares[move_row][move_col] =\
                    self.squares[move_row][move_col],\
                    self.squares[movable_row][movable_col]
        return self.squares

    def king_upgrade(self, move_row, move_col):
        '''
        Method -- king_upgrade
            Upgrage the piece as king if it arrives the last row of opponent
        Parameters:
            self -- the current GameState object
            move_row -- the selected move's row position
            move_col -- the selected move's col position
        Returns:
            Nothing
        '''
        if (self.squares[move_row][move_col] == BLACK and
           move_row == NUM_SQUARES - 1) or (self.squares[move_row][move_col]
           == RED and move_row == 0):
            self.squares[move_row][move_col] =\
                self.squares[move_row][move_col] + KING

    def storage_reset(self):
        '''
        Method -- storage_reset
            Reset human player's movable and possible moves list as empty
        Parameters:
            self -- the current GameState object
        Returns:
            Nothing
        '''
        self.movable_pieces = []
        self.possible_moves = []
        self.possible_capture_moves = []

    def switch_turn(self):
        '''
        Method -- switch_turn
            Switch the current player
        Parameters:
            self -- the current GameState object
        Returns:
            Nothing
        '''
        self.current_player = PLAYER[(PLAYER.index(self.current_player) + 1)
                                     % 2]

    def computer_move(self):
        '''
        Method -- computer_move
            Calculate which move to make for computer player
        Parameters:
            self -- the current GameState object
        Returns:
            Two lists storing location of computer player's valid movable
            piece choice and valid move choice, and a boolean representing if
            the move choice is a capture one or not
        '''
        dict_moves = {}
        computer_non_capture_moves, computer_non_capture_movables,\
            computer_capture_moves, computer_capture_movables = self.move_options()
        if computer_capture_moves:
            for i, computer_move in enumerate(computer_capture_moves):
                movable_row, movable_col = computer_capture_movables[i][0], computer_capture_movables[i][1]
                move_row, move_col = computer_move[0], computer_move[1]
                destination_move = computer_move
                dict_moves[((movable_row, movable_col), (move_row, move_col))] = 1
                capture_piece1_row, capture_piece1_col = (movable_row + move_row) // 2, (movable_col + move_col) // 2
                capture_piece1_origin = self.squares[capture_piece1_row][capture_piece1_col]
                self.squares[capture_piece1_row][capture_piece1_col] = EMPTY
                # update squares for computer capture move
                self.squares[movable_row][movable_col], self.squares[move_row][move_col] =\
                self.squares[move_row][move_col], self.squares[movable_row][movable_col]
                # identify if there is a continuous jump
                computer_possible_continuous_capture_moves = self.capture_move(move_row, move_col)
                if len(computer_possible_continuous_capture_moves) > 0:
                    dict_moves[((movable_row, movable_col), (move_row, move_col))] += 2
                    ind = random.choice(list(range(len(computer_possible_continuous_capture_moves))))
                    destination_move = computer_possible_continuous_capture_moves[ind]
                    destination_row, destination_col = destination_move[0], destination_move[1]
                    capture_piece2_row, capture_piece2_col = (move_row + destination_row) // 2, (move_col + destination_col) // 2
                    capture_piece2_origin = self.squares[capture_piece2_row][capture_piece2_col]
                    self.squares[capture_piece2_row][capture_piece2_col] = EMPTY
                    # update squares for computer capture move(continuous jump)
                    self.squares[move_row][move_col], self.squares[destination_row][destination_col] =\
                    self.squares[destination_row][destination_col], self.squares[move_row][move_col]
                # judge if human will capture back
                self.current_player = BLACK
                _, _, human_capture_moves, human_capture_movables = self.move_options()
                if human_capture_moves:
                    for i, human_move in enumerate(human_capture_moves):
                        human_move_row, human_move_col = human_move[0], human_move[1]
                        human_movable_row, human_movable_col = human_capture_movables[i][0], human_capture_movables[i][1]
                        delete_row, delete_col = (human_movable_row + human_move_row) // 2, (human_movable_col + human_move_col) // 2
                        possible_deleted_pieces = []
                        possible_deleted_pieces.append((delete_row, delete_col))
                        # update squares for human capture move
                        self.squares[human_movable_row][human_movable_col], self.squares[human_move_row][human_move_col] =\
                        self.squares[human_move_row][human_move_col], self.squares[human_movable_row][human_movable_col]
                        # judge if human will have a continuous capture
                        human_possible_continuous_capture_moves = self.capture_move(human_move_row, human_move_col)
                        if len(human_possible_continuous_capture_moves) > 0:
                            dict_moves[((movable_row, movable_col), (move_row, move_col))] -= 1
                        # update squares back for human move
                        self.squares[human_move_row][human_move_col], self.squares[human_movable_row][human_movable_col] =\
                        self.squares[human_movable_row][human_movable_col], self.squares[human_move_row][human_move_col]
                    if destination_move in possible_deleted_pieces:
                        dict_moves[((movable_row, movable_col), (move_row, move_col))] -= 1
                self.current_player = RED
                # update squares back to orginal
                if len(computer_possible_continuous_capture_moves) > 0:
                    self.squares[destination_row][destination_col], self.squares[movable_row][movable_col] =\
                    self.squares[movable_row][movable_col], self.squares[destination_row][destination_col]
                    self.squares[capture_piece2_row][capture_piece2_col] = capture_piece2_origin
                else:
                    self.squares[move_row][move_col], self.squares[movable_row][movable_col] =\
                    self.squares[movable_row][movable_col], self.squares[move_row][move_col]
                    self.squares[capture_piece1_row][capture_piece1_col] = capture_piece1_origin
                    
        if not computer_capture_moves and computer_non_capture_moves:
            for i, computer_move in enumerate(computer_non_capture_moves):
                movable_row, movable_col = computer_non_capture_movables[i][0], computer_non_capture_movables[i][1]
                move_row, move_col = computer_move[0], computer_move[1]
                dict_moves[((movable_row, movable_col), (move_row, move_col))] = 0
                self.squares[movable_row][movable_col], self.squares[move_row][move_col] =\
                self.squares[move_row][move_col], self.squares[movable_row][movable_col]
                # judge if human will capture back
                self.current_player = BLACK
                _, _, human_capture_moves, human_capture_movables = self.move_options()
                if human_capture_moves:
                    for i, human_move in enumerate(human_capture_moves):
                        human_move_row, human_move_col = human_move[0], human_move[1]
                        human_movable_row, human_movable_col = human_capture_movables[i][0], human_capture_movables[i][1]
                        delete_row, delete_col = (human_movable_row + human_move_row) // 2, (human_movable_col + human_move_col) // 2
                        possible_deleted_pieces = []
                        possible_deleted_pieces.append((delete_row, delete_col))
                        # update squares for human capture move
                        self.squares[human_movable_row][human_movable_col], self.squares[human_move_row][human_move_col] =\
                        self.squares[human_move_row][human_move_col], self.squares[human_movable_row][human_movable_col]
                        # update squares for human capture move(continuous jump)
                        human_possible_continuous_capture_moves = self.capture_move(human_move_row, human_move_col)
                        if len(human_possible_continuous_capture_moves) > 0:
                            dict_moves[((movable_row, movable_col), (move_row, move_col))] -= 1
                        # update squares back for human move
                        self.squares[human_movable_row][human_movable_col], self.squares[human_move_row][human_move_col] =\
                        self.squares[human_move_row][human_move_col], self.squares[human_movable_row][human_movable_col]
                    if computer_move in possible_deleted_pieces:
                        dict_moves[((movable_row, movable_col), (move_row, move_col))] -= 1
                self.current_player = RED
                # update squares back to orginal
                self.squares[move_row][move_col], self.squares[movable_row][movable_col] =\
                self.squares[movable_row][movable_col], self.squares[move_row][move_col]

        final_computer_move_path = max(dict_moves, key=lambda i: dict_moves[i])
        final_computer_movable = final_computer_move_path[0]
        final_computer_move = final_computer_move_path[1]
        if final_computer_move in computer_capture_moves:
            ifcapture = True
        else:
            ifcapture = False
        return final_computer_movable, final_computer_move, ifcapture

    def computer_update_squares(self, computer_movable, computer_move,
                                ifcapture):
        '''
        Method -- computer_update_squares
            Update the state of each square on the board in nested list after
            computer player's move
        Parameters:
            self -- the current GameState object
            computer_movable -- the computer player's movable piece
            computer_move -- the computer player's move piece
            ifcapture -- Boolean to represent if computer palyer's move is a
            capture move or a non capture move
        Returns:
            A nested list storing the newest state of each square on the board
        '''
        movable_row, movable_col = computer_movable[0], computer_movable[1]
        move_row, move_col = computer_move[0], computer_move[1]
        if ifcapture:
            delete_row, delete_col = (move_row + movable_row) // 2,\
                (move_col + movable_col) // 2
            self.squares[delete_row][delete_col] = EMPTY
            self.squares[movable_row][movable_col],\
                self.squares[move_row][move_col] =\
                self.squares[move_row][move_col],\
                self.squares[movable_row][movable_col]
        else:
            self.squares[movable_row][movable_col],\
                self.squares[move_row][move_col] =\
                self.squares[move_row][move_col],\
                self.squares[movable_row][movable_col]
        return self.squares

    def game_end(self):
        '''
        Method -- game_end
            Check if the game ends or not
        Parameters:
            self -- the current GameState object
        Returns:
            A boolean to represent if the game ends and the result prompt to
            show which player wins the game
        '''
        black_count = 0
        red_count = 0
        result_prompt = " "
        if_game_end = False
        BLACK_WIN = "Game Over! You win!"
        RED_WIN = "Game Over! Red player wins!"
        for row in range(0, NUM_SQUARES):
            for col in range(0, NUM_SQUARES):
                if (self.squares[row][col] == BLACK or
                   self.squares[row][col] == BLACK + KING):
                    black_count += 1
                elif (self.squares[row][col] == RED or
                      self.squares[row][col] == RED + KING):
                    red_count += 1
        if black_count == 0:
            result_prompt = RED_WIN
            if_game_end = True
            return if_game_end, result_prompt
        elif red_count == 0:
            result_prompt = BLACK_WIN
            if_game_end = True
            return if_game_end, result_prompt
        else:
            _, non_capture_movable_options, _, capture_movable_options =\
                self.move_options()
            movable_pieces =\
                non_capture_movable_options + capture_movable_options
            if self.current_player == BLACK and len(movable_pieces) == 0:
                result_prompt = RED_WIN
                if_game_end = True
                return if_game_end, result_prompt
            elif self.current_player == RED and len(movable_pieces) == 0:
                result_prompt = BLACK_WIN
                if_game_end = True
                return if_game_end, result_prompt
            else:
                return if_game_end, result_prompt
