'''
Xiaoxi Yang
Code for project_Checkers Game
'''
import turtle
from board import Board


def main():
    board = Board()

    # Click handling
    screen = turtle.Screen()
    screen.onclick(board.click_handler)
    turtle.done()


if __name__ == "__main__":
    main()
