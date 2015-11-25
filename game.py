import copy
import random
import utils


class Game(object):
    """A game of 2048."""

    def __init__(self):
        """Creates the game and sets up the board."""
        self.grid_size = 4
        self.grid = [[i*j*0 for i in range(self.grid_size)] for j in range(self.grid_size)]
        self.playing = True
        self.score = 0
        self.new_game()

    def game_over(self):
        """Makes necessary changes for the end of a game."""
        self.playing = False

    def _get_sequences(self, direction):
        """Returns the four sequences in order for the specified move."""
        if direction == "left":
            seqs = [Sequence(self.grid_size, [self.grid[i][j] for i in range(self.grid_size)]) for j in
                    range(self.grid_size)]
        elif direction == "right":
            seqs = [Sequence(self.grid_size, [self.grid[i][j] for i in range(self.grid_size - 1, -1, -1)]) for j in
                    range(self.grid_size)]
        elif direction == "up":
            seqs = [Sequence(self.grid_size, [self.grid[i][j] for j in range(self.grid_size)]) for i in
                    range(self.grid_size)]
        elif direction == "down":
            seqs = [Sequence(self.grid_size, [self.grid[i][j] for j in range(self.grid_size - 1, -1, -1)]) for i in
                    range(self.grid_size)]
        else:
            raise ValueError("%s is not a recognised direction" % direction)
        return seqs

    def get_tile(self, x, y):
        """Returns the value of a specified tile, or 0 if it is free..

        :param x: the x coordinate of the tile
        :param y: the y coordinate of the tile
        :return: the value of the specified tile, 0 or a power of two
        """
        return self.grid[x][y]

    def _is_available(self, x, y):
        """Returns true is a space is free, false is occupied by a tile.

        Arguments:
        @param x: the x coordinate of the tile
        @param y: the y coordinate of the tile
        @return: True or False for whether the specified tile is occupied
        """
        return self.get_tile(x, y) == 0

    def make_move(self, direction):
        """Carries out a move in the specified direction.

        @param direction: left, right, up or down to specify the move direction
        """
        if not (direction in moves.values()):
            raise ValueError("%s is not a recognised direction" % direction)

        if not self.playing:
            raise utils.GameOverException("Attempting to make a move on a finished game")

        move_score = 0

        seqs = self._get_sequences(direction)
        for i in range(self.grid_size):
            s, v = seqs[i].make_move()
            move_score += s
        self._set_sequences(seqs, direction)
        self.score += move_score

        self._spawn_tile()
        if not self.test_available_moves():
            self.game_over()

    def new_game(self):
        """Creates a new game."""
        self.score = 0
        self.playing = True
        self.grid = [[i*j*0 for i in range(self.grid_size)] for j in range(self.grid_size)]
        self._spawn_tile()
        self._spawn_tile()

    def _set_sequences(self, seqs, direction):
        """Sets the grid to the pattern specified by seqs.

        Arguments:
        @param seqs: the list of four sequences containing the current game state
        @param direction: left, right, up or down to specify the move direction
        """

        if not self.playing:
            raise utils.GameOverException("Attempting to make a change a the grid for a finished game")

        if len(seqs) != self.grid_size:
            raise ValueError("Number of sequences does not match the grid size")
        for seq in seqs:
            if seq.get_size() != self.grid_size:
                raise ValueError("Length of a sequence does not match the grid size")

        if direction == "left":
            for x in range(self.grid_size):
                for y in range(self.grid_size):
                    self._set_tile(x, y, seqs[y].get_value(x))
        elif direction == "right":
            for x in range(self.grid_size - 1, -1, -1):
                for y in range(self.grid_size):
                    self._set_tile(x, y, seqs[y].get_value(x))
        elif direction == "up":
            for x in range(self.grid_size):
                for y in range(self.grid_size):
                    self._set_tile(x, y, seqs[x].get_value(y))
        elif direction == "down":
            for x in range(self.grid_size):
                for y in range(self.grid_size - 1, -1, -1):
                    self._set_tile(x, y, seqs[x].get_value(x))
        return seqs

    def _set_tile(self, x, y, value):
        """Sets the specified square to the value."""

        if not self.playing:
            raise utils.GameOverException("Attempting to make a change a tile for a finished game")

        if not (utils.isPower(value, 2)) and value != 0:
            raise ValueError("%i is not a power of 2 or zero" % value)
        self.grid[x][y] = value

    def _spawn_tile(self):
        """Randomly spawns a new tile in an available space."""

        if not self.playing:
            raise utils.GameOverException("Attempting to make a spawn a tile for a finished game")

        x = -1
        y = -1

        while True:
            x = random.randint(0, 3)
            y = random.randint(0, 3)
            if self._is_available(x, y):
                break

        if random.random() < 0.1:
            self._set_tile(x, y, 4)
        else:
            self._set_tile(x, y, 2)

    def test_available_moves(self):
        """Tests whether or not there are available moves."""
        available_moves = False
        for direction in moves.values():
            available_moves = (available_moves or self.test_move(direction))
        return available_moves

    def test_move(self, direction):
        """Returns whether or not the move in the specified direction is legal.

        @param direction: left, right, up or down to specify the move direction
        """
        if not (direction in moves.values()):
            raise ValueError("%s is not a recognised direction" % direction)

        if not self.playing:
            raise utils.GameOverException("Attempting to make a test a move for a finished game")

        valid = False
        seqs = self._get_sequences(direction)
        for i in range(self.grid_size):
            s, v = seqs[i].make_move()
            valid = (valid or v)

        return valid


class Sequence:
    """A row in the grid for the purpose of move making."""

    def __init__(self, size, seq_list):
        """Sets up the sequence."""
        self.grid_size = size
        self.seq_list = seq_list
        self.seq_orig = copy.copy(seq_list)
        self.score = 0

    def get_value(self, i):
        """Returns the value at index i.

        @param i: the index
        """
        return self.seq_list[i]

    def get_size(self):
        """Returns the length of the sequence."""
        return self.grid_size

    def make_move(self):
        """Applies the move taking algorithm to the sequence, returning the score and whether the move is valid"""

        self._shift_left()
        for i in range(self.grid_size - 1):
            if self.seq_list[i] == self.seq_list[i + 1]:
                self.seq_list[i] *= 2
                self.seq_list[i + 1] = 0
                self.score += self.seq_list[i]
                self._shift_left()

        valid = not (self.seq_list == self.seq_orig)

        return self.score, valid

    def _shift_left(self):
        """Moves all elements to the left, filling up blanks"""
        for i in range(self.grid_size):
            if self.seq_list[i] == 0:
                for j in range(i, self.grid_size - 1):
                    self.seq_list[j] = self.seq_list[j + 1]
                self.seq_list[self.grid_size - 1] = 0


moves = {0: "left", 1: "right", 2: "up", 3: "down"}
