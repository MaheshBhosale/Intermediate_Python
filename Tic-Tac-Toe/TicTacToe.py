import sys
sys.path.append("C:\Users\Swapnil.Walke\Intermediate_Python\Tic-Tac-Toe")
from controller import Controller
from player import Player

class TicTacToeController(Controller):

    log_file = "tic_tac_toe.log"

    def __init__(self):
        Controller.__init__(self, self.log_file)
        self.logging.info("TicTacToe controller initiated")
        self.matrix = []
        for i in range(1,9,3):
            self.matrix.append(range(i, i+3))
        self.logging.info("matrix has been built")
        self.logging.info(str(self.matrix))


    def _pre_play(self):
        print "Welcome to tic tac toe"
        print "Enter number of players"
        a = int(raw_input())
        if a == 1:
            self.logging.debug("One player game is unsupported")
            print "Sorry! Our bot is under development, wait patiently till we get done with our bot. Thanks!"
            sys.exit(100)
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


    def display_matrix(self):
        """display the matrix"""
        self.logging.debug(str(self.matrix))
        for i in self.matrix:
            stri = ""
            for j in i:
                stri += str(j) + " "
            print stri


    def print_space(self):
        """display 3 spaces"""
        for i in range(3):
            print ""


    def win(self, player):
        """check the winning condition or check the draw condition"""
        if len(self.player_one.moves) + len(self.player_two.moves) == 9:
            print " Games is drawn"
            self.logging.debug("Game is draw, nobody won")
            self.logging.debug("Enjoy the game again :)")
            sys.exit(100)
        if player == 1:
            a = self.player_one.moves
        else:
            a = self.player_two.moves
        winning_moves = []
        for i in range(1,9,3):
            winning_moves.append(range(i, i+3))
        for i in range(1,4):
            winning_moves.append(range(i,i+7,3))
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
        return False, player


    def _play(self):
        print "Lets start the game"
        flg = 1
        while True:
            self.print_space()
            self.display_matrix()
            self.print_space()
            print "Enter move for player " + str(flg)
            m = int(raw_input())
            if m < 1 and m > 9:
                print "Wrong input"
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
            m-=1
            for i in self.matrix:
                if (m+1) in i:
                    m = m % 3
                    i.pop(m)
                    i.insert(m, ch)
            ret, player = self.win(1 if flg == 2 else 2)
            if ret == True:
                print " Congratulations! Player " + str(player) + " have won the match!"
                break


    def initiate(self):
        self._pre_play()
        self._play()



game = TicTacToeController()
game.initiate()