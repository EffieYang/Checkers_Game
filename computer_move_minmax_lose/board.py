'''
Xiaoxi Yang
Code for project_Checkers Game
'''
import turtle
from game_state import GameState

NUM_SQUARES = 8
SQUARE = 50
INITIAL_ROWS = 3
QUARTER = 4
BLACK = "black"
RED = "dark red"
EMPTY = "empty"
KING = "king"
SQUARE_COLORS = ("light gray", "white")
PIECES_COLORS = ("black", "dark red")
DELAY_TIME = 1000
CLOSE_WINDOW = "Click again to close the window."
TURN_REMINDER = "It's your turn now."
game = GameState()


class Board:
    '''
    Class -- Board
        Draw the board, pieces and represents the UI
    Attributes:
        pen1 -- a turtle object, used to write prompt regarding player's move
        at the bottom of screen
        pen2 -- a turtle object, used to write prompt regarding game result at
        the top of screen
    Methods:
        draw_squares -- Draw a square of a given size
        draw_board -- Draw a board of given size and conditions
        draw_movable_piece_square -- Draw a highlight blue square frame for
        movable piece
        draw_possible_moves_square -- Draw highlight red square frames for
        possible moves
        draw_circle -- Draw a circle with a given radius
        draw_pieces -- Draw pieces on board according to the board state
        write_prompt -- Write prompt regarding player's move at the bottom of
        screen
        write_result -- Write prompt regarding game result at the top of screen
        click_handler -- The overall logic of the UI game
        computer_control -- The overall logic of computer player
    '''

    def __init__(self):
        '''
        Constructor -- create a new instance of Board
        Parameters:
            self -- the current Board object
        '''
        self.draw_board()
        self.draw_pieces()
        self.pen1 = turtle.Turtle()
        self.pen1.penup()
        self.pen1.hideturtle()
        self.pen1.setposition(-SQUARE * NUM_SQUARES // 2,
                              -SQUARE * NUM_SQUARES // 2 - SQUARE // 2)
        self.pen2 = turtle.Turtle()
        self.pen2.penup()
        self.pen2.hideturtle()
        self.pen2.setposition(-SQUARE * NUM_SQUARES // 2,
                              SQUARE * NUM_SQUARES // 2 + SQUARE // QUARTER)
        self.write_prompt(TURN_REMINDER)

    def draw_square(self, a_turtle, size):
        '''
        Method -- draw_square
            Draw a square of a given size
        Parameters:
            self -- the current Board object
            a_turtle -- an instance of Turtle
            size -- the length of each side of the square
        Returns:
            Nothing. Draws a square in the graphics window
        '''
        RIGHT_ANGLE = 90
        SQUARE_EDGES = 4
        a_turtle.pendown()
        a_turtle.begin_fill()
        for i in range(SQUARE_EDGES):
            a_turtle.forward(size)
            a_turtle.left(RIGHT_ANGLE)
        a_turtle.end_fill()
        a_turtle.penup()

    def draw_board(self):
        '''
        Method -- draw_board
            Draw a board of given size and conditions
        Parameters:
            self -- the current Board object
        Returns:
            Nothing. Draws a board in the graphics window
        '''
        board_size = SQUARE * NUM_SQUARES
        window_size = board_size + SQUARE
        turtle.setup(window_size, window_size + SQUARE)
        turtle.screensize(board_size, board_size)
        turtle.bgcolor("white")
        turtle.tracer(0, 0)
        pen = turtle.Turtle()
        pen.penup()
        pen.hideturtle()
        pen.color("black", "white")
        origin_point = - board_size / 2
        pen.setposition(origin_point, origin_point)
        self.draw_square(pen, board_size)
        pen.color("black", SQUARE_COLORS[0])
        for row in range(NUM_SQUARES):
            for col in range(NUM_SQUARES):
                if row % 2 != col % 2:
                    pen.setposition(origin_point + col * SQUARE,
                                    origin_point + row * SQUARE)
                    self.draw_square(pen, SQUARE)

    def draw_movable_piece_square(self):
        '''
        Method -- draw_movable_piece_square
            Draw a highlight blue square frame for movable piece
        Parameters:
            self -- the current Board object
        Returns:
            Nothing.
        '''
        pen = turtle.Turtle()
        pen.penup()
        pen.hideturtle()
        pen.color("blue", SQUARE_COLORS[0])
        row, col = game.movable_piece[0], game.movable_piece[1]
        x = (col - NUM_SQUARES // 2) * SQUARE
        y = (row - NUM_SQUARES // 2) * SQUARE
        pen.setposition(x, y)
        self.draw_square(pen, SQUARE)
        pen.color("black", game.current_player)
        pen.setposition(x + SQUARE // 2, y)
        self.draw_circle(pen, SQUARE // 2)
        if game.squares[row][col] == game.current_player + KING:
            pen.color("white", game.current_player)
            pen.setposition(x + SQUARE // 2, y + SQUARE // QUARTER)
            self.draw_circle(pen, SQUARE // QUARTER)

    def draw_possible_moves_square(self):
        '''
        Method -- draw_possible_moves_square
            Draw highlight red square frames for possible moves
        Parameters:
            self -- the current Board object
        Returns:
            Nothing.
        '''
        pen = turtle.Turtle()
        pen.penup()
        pen.hideturtle()
        pen.color("red", SQUARE_COLORS[0])
        if game.possible_capture_moves:
            for move in game.possible_capture_moves:
                x = (move[1] - NUM_SQUARES // 2) * SQUARE
                y = (move[0] - NUM_SQUARES // 2) * SQUARE
                pen.setposition(x, y)
                self.draw_square(pen, SQUARE)
        elif not game.possible_capture_moves and game.possible_moves:
            for move in game.possible_moves:
                x = (move[1] - NUM_SQUARES // 2) * SQUARE
                y = (move[0] - NUM_SQUARES // 2) * SQUARE
                pen.setposition(x, y)
                self.draw_square(pen, SQUARE)

    def draw_circle(self, a_turtle, size):
        '''
        Method -- draw_circle
            Draw a circle with a given radius
        Parameters:
            self -- the current Board object
            a_turtle -- an instance of Turtle
            size -- the radius of the circle
        Returns:
            Nothing. Draws a circle in the graphics window.
        '''
        a_turtle.pendown()
        a_turtle.begin_fill()
        a_turtle.circle(size)
        a_turtle.end_fill()
        a_turtle.penup()

    def draw_pieces(self):
        '''
        Method -- draw_pieces
            Draw pieces on board according to the board state
        Parameters:
            self -- the current Board object
            a_turtle -- an instance of Turtle
            size -- the radius of the circle
        Returns:
            Nothing. Draws pieces in the graphics window.
        '''
        squares = game.squares
        for row in range(0, NUM_SQUARES):
            for col in range(0, NUM_SQUARES):
                pen = turtle.Turtle()
                pen.penup()
                pen.hideturtle()
                x = (col - NUM_SQUARES // 2) * SQUARE + SQUARE // 2
                y = (row - NUM_SQUARES // 2) * SQUARE
                pen.setposition(x, y)
                if squares[row][col] == BLACK:
                    pen.color("black", PIECES_COLORS[0])
                    self.draw_circle(pen, SQUARE // 2)
                elif squares[row][col] == BLACK + KING:
                    pen.color("black", PIECES_COLORS[0])
                    self.draw_circle(pen, SQUARE // 2)
                    y = y + SQUARE // QUARTER
                    pen.setposition(x, y)
                    pen.color("white", PIECES_COLORS[0])
                    self.draw_circle(pen, SQUARE // QUARTER)
                elif squares[row][col] == RED:
                    pen.color("black", PIECES_COLORS[1])
                    self.draw_circle(pen, SQUARE // 2)
                elif squares[row][col] == RED + KING:
                    pen.color("black", PIECES_COLORS[1])
                    self.draw_circle(pen, SQUARE // 2)
                    y = y + SQUARE // QUARTER
                    pen.setposition(x, y)
                    pen.color("white", PIECES_COLORS[1])
                    self.draw_circle(pen, SQUARE // QUARTER)

    def write_prompt(self, prompt):
        '''
        Method -- write_prompt
            Write prompt regarding player's move at the bottom of screen
        Parameters:
            self -- the current Board object
            prompt -- a string which represent the UI feedback
        Returns:
            Nothing.
        '''
        self.pen1.pencolor("black")
        self.pen1.write(prompt, align='left', font=('Arial', 12, 'normal'))

    def write_result(self, prompt):
        '''
        Method -- write_result
            write prompt regarding game result at the top of screen
        Parameters:
            self -- the current Board object
            prompt -- a string which represent the game result
        Returns:
            Nothing.
        '''
        self.pen2.pencolor("green")
        self.pen2.write(prompt, align='left', font=('Broadway', 15, 'normal'))

    def click_handler(self, x, y):
        '''
        Method -- click_handler
            The overall logic of the UI game
            Verify if the game is end and if the click is within the board,
            then judge if the click is to choose the movable piece/to select
            a possible move, when a valid move has been made, switch the turn,
            until the game end
        Parameters:
            self -- the current Board object
            x -- the x-coordinate when a click happened
            y -- the y-coordinate when a click happened
        Returns:
            Nothing
        '''
        self.pen1.clear()
        if_game_end, result_prompt = game.game_end()
        game.current_player = BLACK
        if not if_game_end:
            row, col, inboard = game.click_position(x, y)
            if inboard:
                if game.click_validation(row, col):
                    if (not game.movable_pieces and not game.possible_moves
                       and not game.possible_capture_moves):
                        pass
                    elif (game.movable_pieces or game.possible_moves
                          or game.possible_capture_moves):
                        game.storage_reset()
                        self.draw_board()
                        self.draw_pieces()
                    game.possible_moves = game.non_capture_move(row, col)
                    game.possible_capture_moves = game.capture_move(row, col)
                    game.movable_piece = (row, col)
                    self.draw_possible_moves_square()
                    self.draw_movable_piece_square()
                elif game.valid_move(row, col):
                    game.update_squares(row, col)
                    game.king_upgrade(row, col)
                    self.draw_board()
                    self.draw_pieces()
                    if (row, col) in game.possible_capture_moves:
                        game.storage_reset()
                        if len(game.capture_move(row, col)) > 0:
                            self.possible_moves = []
                            self.movable_pieces = [(row, col)]
                            self.draw_possible_moves_square()
                            self.draw_movable_piece_square()
                            return self.click_handler(x, y)
                    else:
                        game.storage_reset()
                    game.switch_turn()
                    if game.current_player == RED:
                        self.computer_control()
                else:
                    self.write_prompt("Not a valid piece/move!")
                    game.storage_reset()
                    self.draw_board()
                    self.draw_pieces()
            else:
                self.write_prompt("Click within the board!")
        else:
            self.write_result(result_prompt)
            self.write_prompt(CLOSE_WINDOW)
            turtle.exitonclick()

    def computer_control(self):
        '''
        Method -- computer_control
            The overall logic of computer player
            Verify if the game is end, then choose the movable piece and
            a valid move for computer, when a valid move has been made,
            switch the turn, until the game end
        Parameters:
            self -- the current Board object
        Returns:
            Nothing
        '''
        self.pen1.clear()
        if_game_end, result_prompt = game.game_end()
        if not if_game_end:
            computer_movable, computer_move, ifcapture = game.computer_move()
            game.computer_update_squares(computer_movable, computer_move,
                                         ifcapture)
            move_row, move_col = computer_move[0], computer_move[1]
            game.king_upgrade(move_row, move_col)
            self.draw_board()
            turtle.ontimer(self.draw_pieces(), DELAY_TIME)
            if (move_row, move_col) == computer_move and ifcapture:
                possible_capture_moves = game.capture_move(move_row, move_col)
                while len(possible_capture_moves) > 0:
                    computer_movable = (move_row, move_col)
                    computer_move = possible_capture_moves[0]
                    move_row, move_col = computer_move[0], computer_move[1]
                    ifcapture = True
                    game.computer_update_squares(computer_movable,
                                                 computer_move, ifcapture)
                    game.king_upgrade(move_row, move_col)
                    self.draw_board()
                    turtle.ontimer(self.draw_pieces(), DELAY_TIME)
                    possible_capture_moves = game.capture_move(move_row,
                                                               move_col)
            if_game_end, result_prompt = game.game_end()
            if not if_game_end:
                game.switch_turn()
                self.write_prompt(TURN_REMINDER)
            else:
                self.write_result(result_prompt)
                self.write_prompt(CLOSE_WINDOW)
                turtle.exitonclick()
        else:
            self.write_result(result_prompt)
            self.write_prompt(CLOSE_WINDOW)
            turtle.exitonclick()
