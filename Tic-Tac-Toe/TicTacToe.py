
import sys
import copy
from controller import Controller
from player import Player

sys.path.append("C:\Users\Swapnil.Walke\Intermediate_Python\Tic-Tac-Toe")


class TicTacToeController(Controller):
    log_file = "tic_tac_toe.log"

    def __init__(self):
        Controller.__init__(self, self.log_file)
        self.logging.info("TicTacToe controller initiated")
        self.matrix = []
        self.board = []
        self.alpha = -9999999999
        self.beta = 9999999999
        for i in range(3):
            a = []
            for i in range(3):
                a.append('_')
            self.board.append(a)

        for i in range(1, 9, 3):
            self.matrix.append(range(i, i + 3))
        self.logging.info("matrix has been built")
        self.logging.info(str(self.matrix))

    def _pre_play(self):
        print "Welcome to tic tac toe"
        print "Enter number of players"
        a = int(raw_input())
        if a == 1:
            self.logging.info("One player game has been started....")
            print "Welcome to the game"
            print "Enter the name of player one:"
            player_one = raw_input()
            self.player_one = Player(player_one)
            print "Welcome " + player_one + "!! you will play against JARVIS!"
            self.player_two = Player("--JARVIS--")
            self.logging.info(str(self.player_one) + " is playing against " + str(self.player_two))
            self._play_bot()
        if a == 2:
            self.logging.debug("Two player game has been started....")
            print "Welcome to the game"
            print "Enter the name of player one:"
            """Enter the names of the player, and initiate the players"""
            player_one = raw_input()
            print "Enter the name of player two:"
            player_two = raw_input()
            self.logging.debug("player " + player_one + " and " + " player " + player_two + " has started playing...")
            self.player_one = Player(player_one)
            self.player_two = Player(player_two)
            self._play()

    def display_matrix(self):
        """display the matrix"""
        self.logging.debug(str(self.matrix))
        for i in self.matrix:
            stri = ""
            for j in i:
                stri += str(j) + " "
            print stri

    def display_board(self):
        self.logging.debug(str(self.board))
        for i in range(3):
            for j in range(3):
                print self.board[i][j],
            print

    @staticmethod
    def print_space():
        """display 3 spaces"""
        for i in range(3):
            print ""

    def win(self, player):
        """check the winning condition or check the draw condition"""
        if player == 1:
            a = self.player_one.moves
        else:
            a = self.player_two.moves
        winning_moves = []
        for i in range(1, 9, 3):
            winning_moves.append(range(i, i + 3))
        for i in range(1, 4):
            winning_moves.append(range(i, i + 7, 3))
        winning_moves.append([1, 5, 9])
        winning_moves.append([3, 5, 7])
        for move in winning_moves:
            flg = True
            for index in move:
                if index not in a:
                    flg = False
                    break
            if flg:
                return True, player
        if len(self.player_one.moves) + len(self.player_two.moves) == 9:
            self.print_space()
            self.display_board()
            self.print_space()
            print " Games is drawn"
            self.logging.debug("Game is draw, nobody won")
            self.logging.debug("Enjoy the game again :)")
            sys.exit(100)
        return False, player

    def is_valid_move(self, m):
        if m < 1 or m > 9:
            print "Wrong input"
            return -1
        if m in self.player_one.moves or m in self.player_two.moves:
            return -2

    def evaluate(self, board):

        # check for rows
        for i in board:
            if '_' not in i:
                s = set(i)
                if len(s) == 1 and 'X' in s:
                    return 10
                elif len(s) == 1 and 'O' in s:
                    return -10
        # check for columns
        for i in range(3):
            a = []
            for j in range(3):
                a.append(board[j][i])
            if '_' not in a:
                s = set(a)
                if len(s) == 1 and 'X' in s:
                    return 10
                elif len(s) == 1 and 'O' in s:
                    return -10
        # check for diagonals
        if board[1][1] != '_':
            if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
                # print "Congratulations! player " + str(player) + " has won the match!"
                if board[1][1] == 'X':
                    return 10
                else:
                    return -10
            if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
                # print "Congratulations! player " + str(player) + " has won the match!"
                if board[1][1] == 'X':
                    return 10
                else:
                    return -10
        flg = 0
        for i in board:
            if '_' in i:
                flg = 1
        if flg == 0:
            return 0

    def min_max(self, board, palpha, pbeta, alpha, beta, depth, isMax):

        # Check which player has won and return score accordingly
        score = self.evaluate(board)
        if score == 10:
            return score - depth

        if score == -10:
            return score + depth

        if score == 0:
            return score

        # If this is Maximizer move
        if (isMax):
            best = -1000

            # Traverse all the cells
            for i in range(0, 3, 1):
                for j in range(0, 3, 1):

                    if board[i][j] == '_':

                        if alpha > beta:
                            alpha = palpha
                            continue

                        # make the move
                        board[i][j] = 'X'

                        # Call min_max recursively and find out the maximun value
                        best = max(best, self.min_max(copy.deepcopy(board), palpha, pbeta, alpha, beta, depth + 1,
                                                      not (isMax)))

                        # Undo the move
                        board[i][j] = '_'

                        palpha = alpha
                        alpha = max(best, alpha)
            return best
        else:
            best = 1000

            # Traverse all the cells
            for i in range(0, 3, 1):
                for j in range(0, 3, 1):

                    if board[i][j] == '_':

                        if alpha > beta:
                            beta = pbeta
                            continue

                        # make the move
                        board[i][j] = 'O'

                        # Call min_max recursively and find out the minimum value
                        best = min(best, self.min_max(copy.deepcopy(board), palpha, pbeta, alpha, beta, depth + 1,
                                                      not (isMax)))

                        # Undo the move
                        board[i][j] = '_'

                        pbeta = beta
                        beta = min(best, beta)
            return best

    def find_best_move(self, board):
        best_val = -1000
        best_row = -1
        best_col = -1

        for i in range(0, 3):
            for j in range(0, 3):
                if board[i][j] == '_':

                    # Make the move
                    board[i][j] = 'X'
                    move_val = self.min_max(copy.deepcopy(board), -9999999999, 9999999999, -9999999999, 9999999999, 0, False)

                    # Undo the move
                    board[i][j] = '_'

                    # if value of current move > best_value, update
                    if move_val > best_val:
                        best_val = move_val
                        best_row = i
                        best_col = j

        return best_row, best_col

    def check(self, player):
        if player == 2:
            ch = 'X'
        else:
            ch = 'O'
        # check for rows
        for i in self.board:
            if '_' not in i:
                s = set(i)
                if len(s) == 1 and ch in s:
                    return True, player
        # check for columns
        for i in range(3):
            a = []
            for j in range(3):
                a.append(self.board[j][i])
            if '_' not in a:
                s = set(a)
                if len(s) == 1 and ch in s:
                    return True, player
        # check for diagonals
        if self.board[1][1] != '_':
            if self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2]:
                return True, player
            if self.board[0][2] == self.board[1][1] and self.board[1][1] == self.board[2][0]:
                return True, player
        flg = 1
        for i in self.board:
            if '_' in i:
                flg = 0
        if flg == 1:
            return False, "draw"
        return -1, None

    def _play_bot(self):
        print "Lets start the game..."
        players = [self.player_one.name, self.player_two.name]
        flg = 1
        while True:
            self.print_space()
            self.display_board()
            self.print_space()
            if players[flg - 1] == "--JARVIS--":
                print "Let JARVIS play...."
                m, n = self.find_best_move(copy.deepcopy(self.board))
            else:
                print "Enter move for player " + str(players[flg - 1]) + "row and column"
                m = int(raw_input("row:"))
                n = int(raw_input("col:"))
            print str(m) + " " + str(n)
            if m < 0 or m > 2:
                print "Invalid Move!"
                continue
            if n < 0 or n > 2:
                print "Invalid Move!"
                continue
            if self.board[m][n] != '_':
                print "Invalid Move, already played.."
                continue
            if flg == 2:
                ch = "X"
            else:
                ch = "O"
            self.board[m][n] = ch
            ret, player = self.check(flg)
            if flg == 1:
                flg = 2
            else:
                flg = 1
            if ret is True:
                self.print_space()
                self.display_board()
                self.print_space()
                print " Congratulations! Player " + str(player) + " have won the match!"
                break
            if ret is False and player == "draw":
                self.print_space()
                self.display_board()
                self.print_space()
                print "Match has been drawn!"
                break

    def _play(self):
        print"Lets start the game"
        flg = 1
        while True:
            self.print_space()
            self.display_matrix()
            self.print_space()
            print"Enter move for player " + str(flg)
            m = int(raw_input())

            ret = self.is_valid_move(m)
            if ret == -1:
                continue
            elif ret == -2:
                print "Invalid Move, already played.."
                continue
            if flg == 1:
                self.player_one.make_move(m)
                flg = 2
            else:
                self.player_two.make_move(m)
                flg = 1
            if flg == 2:
                ch = "X"
            else:
                ch = "O"
            m -= 1
            for i in self.matrix:
                if (m + 1) in i:
                    m = m % 3
                    i.pop(m)
                    i.insert(m, ch)
            ret, player = self.win(1 if flg == 2 else 2)
            if ret is True:
                print " Congratulations! Player " + str(player) + " have won the match!"
                break

    def initiate(self):
        self._pre_play()


game = TicTacToeController()
game.initiate()
