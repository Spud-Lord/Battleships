from abc import ABCMeta, abstractmethod
from random import randint
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer
import time

class Board():
    def __init__(self, width, height, number):
        self.__columns = width
        self.__rows = height
        self.__board = [[" "]*self.__columns for i in range(self.__rows)]
        self.__playerNumber = number

    def display(self, number):
        firstLine = "-"
        for c in range(self.__columns):
            if c < 9:
                firstLine += ("| " + str(c+1) + " ")
            else:
                firstLine += ("|" + str(c+1) + " ")
        firstLine += "|"
        print(firstLine)

        for r in range(self.__rows):
            print(str(chr(r+65)), end='')
            for x in self.__board[r]:
                #1 Mark for hiding the locations of the opponent's ships (ETO)
                if self.__playerNumber != number and x == "■":
                    y = " "
                else:
                    y = x
                print("| " + y + " ", end="")
            print("|")

    def getWidth(self):
        return self.__columns

    def getHeight(self):
        return self.__rows

    def takeShot(self, row, column):
        if self.__board[row][column] == "M" or self.__board[row][column] == "X":
            return "Invalid"
        elif self.__board[row][column] == "■":
            self.__board[row][column] = "X"
            return "Hit"
        else:
            self.__board[row][column] = "M"
            return "Miss"

    def placeShip(self, size, number, player="CPU"):
        while True:
            columnSet = False
            rowSet = False
            orientationSet = False

            if player == "Human":
                self.display(number)

            while not columnSet:
                if player == "Human":
                    try:
                        column = int(input("Enter the column where you would like to position the ship (1-" + str(self.__columns) + "): "))
                        print()
                        if column >= 1 and column <= self.__columns:
                            column = column - 1
                            columnSet = True
                        else:
                            print("That column doesn't exist. Please try again.")
                    except:
                        print("That column doesn't exist. Please try again.")
                else:
                    column = randint(0, self.__columns -1)
                    columnSet = True

            while not rowSet:
                if player == "Human":
                    try:
                        row = ord(input("Enter the row where you would like to position the ship (A-" + str(chr(self.__rows+65)) + "): ").upper())
                        print()
                        if row >= 65 and row <= self.__rows+65:
                            row = row-65
                            rowSet = True
                        else:
                            print("That row doesn't exist. Please try again.")
                    except:
                        print("That row doesn't exist. Please try again.")
                else:
                    row = randint(0, self.__rows -1)
                    rowSet = True

            validPos = True

            while not orientationSet:
                if player == "Human":
                    orientation = input("Do you want to place your ship vertically down or horizontally to the right(v/h)?: ")
                    print()
                else:
                    if randint(0,1) == 0:
                        orientation = "v"
                    else:
                        orientation = "h"

                if orientation.lower() == "v" or orientation.lower() == "vertical":
                    orientationSet = True
                    try:
                        for r in range(row, row + size):
                            if self.__board[r][column] == "■":
                                validPos = False
                        if validPos == True:
                            for r in range(row, row + size):
                                self.__board[r][column] = "■"
                            return
                    except:
                        pass

                elif orientation.lower() == "h" or orientation.lower() == "horizontal":
                    orientationSet = True
                    try:
                        for c in range(column, column + size):
                            if self.__board[row][c] == "■":
                                validPos = False
                        if validPos == True:
                            for c in range(column, column + size):
                                self.__board[row][c] = "■"
                            return
                    except:
                        pass

                else:
                    print("You can only position your ship vertically down (v) or horizontally to the right(h)!")
            if player == "Human":
                print("You can't position the ship like that! Try again (The ship is " + size + "tiles long):")

    def checkWinner(self):
        for r in range(self.__rows):
            for c in range(self.__columns):
                if self.__board[r][c] == "■":
                    return False
        return True

class Player(metaclass=ABCMeta):
    def __init__(self, number, width, height):
        self._playerNumber = number
        self._playerBoard = Board(width, height, number)
        self._placeShips()

    def getNumber(self):
        return self._playerNumber

    def getBoard(self):
        return self._playerBoard

    @abstractmethod
    def _placeShips(self):
        pass

    @abstractmethod
    def takeShot(self, board):
        pass

    @abstractmethod
    def _getColumn(self):
        pass

    @abstractmethod
    def _getRow(self):
        pass

class HumanPlayer(Player):
    def _placeShips(self):
        print("Position your carrier (5 tiles long): ")
        self._playerBoard.placeShip(5, self._playerNumber, "Human")
        print("Your carrier is in position!\n")
        time.sleep(2)
        print("Position your battleship (4 tiles long): ")
        self._playerBoard.placeShip(4, self._playerNumber, "Human")
        print("Your battleship is in position!\n")
        time.sleep(2)
        print("Position your cruiser (3 tiles long): ")
        self._playerBoard.placeShip(3, self._playerNumber, "Human")
        print("Your cruiser is in position!\n")
        time.sleep(2)
        print("Position your submarine (3 tiles long): ")
        self._playerBoard.placeShip(3, self._playerNumber, "Human")
        print("Your submarine is in position!\n")
        time.sleep(2)
        print("Position your destroyer (2 tiles long): ")
        self._playerBoard.placeShip(2, self._playerNumber, "Human")
        print("Your destroyer is in position!")
        print()
        time.sleep(2)

    def takeShot(self, board):
        shotMade = False
        while not shotMade:
            print("")
            column = self._getColumn(board)
            row = self._getRow(board)
            result = board.takeShot(row, column)
            if result == "Invalid":
                print("You've already shot that target, aim somewhere else!")
            else:
                shotMade = True
                mixer.init()
                mixer.music.load("Gunshot.mp3")
                mixer.music.play()
                time.sleep(1)
                print(result)
                time.sleep(2)

    def _getColumn(self, board):
        while True:
            try:
                column = int(input("Enter the column you would like to target (1-" + str(board.getWidth()) + "):"))
                if column >= 1 and column <= board.getWidth():
                    return column - 1
                else:
                    print("That column doesn't exist. Please try again.")
            except:
                print("That column doesn't exist. Please try again.")

    def _getRow(self, board):
        while True:
            try:
                print("")
                row = ord(input("Enter the row you would like to target (A-" + str(chr(board.getHeight()+64)) + "):").upper())
                print()
                if row >= 65 and row < board.getHeight() + 65:
                    return row - 65
                else:
                    print("That row doesn't exist. Please try again.")
            except:
                print("That row doesn't exist. Please try again.")

class ComputerPlayer(Player):
    def _placeShips(self):
        print("The computer is positioning its ships...\n")
        time.sleep(3)
        self._playerBoard.placeShip(5, self._playerNumber)
        self._playerBoard.placeShip(4, self._playerNumber)
        self._playerBoard.placeShip(3, self._playerNumber)
        self._playerBoard.placeShip(3, self._playerNumber)
        self._playerBoard.placeShip(2, self._playerNumber)
        print("The computer has positioned its ships!")

    def takeShot(self, board):
        shotMade = False
        while not shotMade:
            column = self._getColumn(board)
            row = self._getRow(board)
            result = board.takeShot(row, column)
            if result != "Invalid":
                shotMade = True
                mixer.init()
                mixer.music.load("Gunshot.mp3")
                mixer.music.play()
                time.sleep(1)
                print("")
                print(result)
                time.sleep(2)

    def _getColumn(self, board):
        return randint(0, board.getWidth()-1)

    def _getRow(self, board):
        return randint(0, board.getHeight()-1)

def main():
    widthSet = False
    heightSet = False

    while not widthSet:
        try:
            width = int(input("Enter the width of your game board (10-26): "))
            print()
            if width >= 10 and width <= 26:
                widthSet = True
            else:
                print("The width must be an integer from 10-26. Please try again.")
        except:
            print("The width must be an integer from 10-26. Please try again.")

    while not heightSet:
        try:
            height = int(input("Enter the height of your game board (10-26): "))
            print()
            if height >= 10 and height <= 26:
                heightSet = True
            else:
                print("The height must be an integer from 10-26. Please try again.")
        except:
            print("The height must be an integer from 10-26. Please try again.")

    player1 = HumanPlayer(1, width, height)
    player2 = ComputerPlayer(2, width, height)
    board1 = player1.getBoard()
    board2 = player2.getBoard()

    while True:
        print()
        print("It's your turn:\n")

        makeShot = False

        while not makeShot:
            result = input("Would you like to take a shot(1), look at the computer's board(2), or look at your board(3)?: ")
            print()
            if result == "1":
                makeShot = True
            elif result == "2":
                board2.display(player1.getNumber())
            elif result == "3":
                board1.display(player1.getNumber())
            else:
                print("That is not a valid option!")

        board2.display(player1.getNumber())
        player1.takeShot(board2)

        if board2.checkWinner():
            print()
            board2.display(player1.getNumber())
            input("You have won!")
            return

        print()
        print("It's the computer's turn:")
        time.sleep(2)
        player2.takeShot(board1)
        board1.display(player1.getNumber())
        if board1.checkWinner():
            print()
            board1.display(player1.getNumber())
            input("You have lost!")
            return

if __name__ == '__main__':
    main()
