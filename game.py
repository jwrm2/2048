import random, utils
from math import log

#----------------------------------------------------------------------------------------------------------------------------------

class Game(object):
  """A game of 2048."""

  def __init__(self):
    """Creates the game and sets up the board."""
    self.gridSize = 4
    self.newGame()

  def gameOver(self):
    """Makes necessary changes for the end of a game."""
    self.playing = False

  def _getSequences(self, direction):
    """Returns the four sequences in order for the specified move."""
    if (direction == "left"):
      seqs = [Sequence(self.gridSize, (self.grid[i,j] for i in range(self.gridSize))) for j in range(self.gridSize)]
    elif (direction == "right"):
      seqs = [Sequence(self.gridSize, (self.grid[i,j] for i in range(self.gridSize-1, -1, -1))) for j in range(self.gridSize)]
    elif (direction == "up"):
      seqs = [Sequence(self.gridSize, (self.grid[i,j] for j in range(self.gridSize))) for i in range(self.gridSize)]
    elif (direction == "down"):
      seqs = [Sequence(self.gridSize, (self.grid[i,j] for j in range(self.gridSize-1, -1, -1))) for i in range(self.gridSize)]
    return seqs

  def getTile(self, x, y):
    """Returns the value of the specified tile, or 0 if it is free."""
    return self.grid[x][y]

  def _isAvailable(self, x, y):
    """Returns true is a space is free, false is occupied by a tile."""
    return self.getTile(x, y) == 0

  def makeMove(self, direction):
    """Carries out a move in the specified direction."""
    if not (direction in moves.values()):
      raise ValueError("%s is not a recognised direction" % direction)

    if not self.playing:
      raise utils.GameOverException("Attempting to make a move on a finished game")

    moveScore = 0

    seqs = self._getSequences(direction)
    for i in range(self.gridSize):
      moveScore += seqs[i].makeMove()
    self._setSequences(seqs)
    self.score += moveScore

    self._spawnTile()
    if not self.testAvailableMoves():
      self.gameOver()

  def newGame(self):
    """Creates a new game."""
    self.score = 0
    self.playing = True
    self.grid = [[0 for i in range(self.gridSize)] for i in range(self.gridSize)]
    self._spawnTile()
    self._spawnTile()

  def _setSequences(self, seqs):
    """Sets the grid to the pattern specified by seqs."""

    if not self.playing:
      raise utils.GameOverException("Attempting to make a change a the grid for a finished game")

    if(len(seqs) != self.gridSize):
      raise ValueError("Number of sequences does not match the grid size")
    for seq in seqs:
      if(len(seq) != self.gridSize):
        raise ValueError("Length of a sequence does not match the grid size")

    if (direction == "left"):
      for x in range(self.gridSize):
        for y in range(self.gridSize):
          self.setTile(x, y, seqs[y].getValue(x))
    elif (direction == "right"):
      for x in range(self.gridSize-1, -1, -1):
        for y in range(self.gridSize):
          self.setTile(x, y, seqs[y].getValue(x))
    elif (direction == "up"):
      for x in range(self.gridSize):
        for y in range(self.gridSize):
          self.setTile(x, y, seqs[x].getValue(y))
    elif (direction == "down"):
      for x in range(self.gridSize):
        for y in range(self.gridSize-1, -1, -1):
          self.setTile(x, y, seqs[x].getValue(x))
    return seqs

  def _setTile(self, x, y, value):
    """Sets the specified square to the value."""

    if not self.playing:
      raise utils.GameOverException("Attempting to make a change a tile for a finished game")

    if not (utils.isPower(value, 2)) and value != 0:
      raise ValueError("%i is not a power of 2 or zero" % value)
    self.grid[x][y] = value

  def _spawnTile(self):
    """Randomly spawns a new tile in an available space."""

    if not self.playing:
      raise utils.GameOverException("Attempting to make a spawn a tile for a finished game")

    while (True):
      x = random.randint(0,3)
      y = random.randint(0,3)
      if (self._isAvailable(x, y)):
        break;

    if (random.random() < 0.1):
      self._setTile(x, y, 4)
    else:
      self._setTile(x, y, 2)

  def testAvailableMoves(self):
    """Tests whether or not there are available moves."""
    availableMoves = False
    for direction in moves.values():
      availableMoves = (availableMoves or self.testMove(direction))
    return availableMoves

  def testMove(self, direction):
    """Returns whether or not the move in the specified direction is legal."""
    if not (direction in moves.values()):
      raise ValueError("%s is not a recognised direction" % direction)

    if not self.playing:
      raise utils.GameOverException("Attempting to make a test a move for a finished game")

    moveScore = 0
    seqs = self._getSequences(direction)
    for i in range(self.gridSize):
      moveScore += seqs[i].makeMove()

    return (moveScore > 0)

#----------------------------------------------------------------------------------------------------------------------------------

class Sequence:
  """A row in the grid for the purpose of move making."""

  def __init__(self, size, seqlist):
    """Sets up the sequence."""
    self.gridSize = size
    self.seqList = seqlist
    self.score = 0

  def getValue(self, i):
    """Returns the value at index i."""
    return self.seqList[i]

  def makeMove(self):
    """Applies the move taking algorithm to the sequence, returning the score increase."""

    self._shiftLeft()
    for i in range(self.gridSize-1):
      if(self.seqList[i] == self.seqList[i+1]):
        self.seqList[i] *= 2
        self.seqList[i+1] = 0
        self.score += self.seqList[i]
        self._shiftLeft()

    return self.score

  def _shiftLeft(self):
    """Moves all elements to the left, filling up blanks"""
    for i in range(self.gridSize):
      if(self.seqList[i] == 0):
        for j in range(i, self.gridSize-1):
          self.seqList[j] = self.seqList[j+1]
        self.seqList[self.gridSize-1] = 0

#----------------------------------------------------------------------------------------------------------------------------------

moves = {0: "left", 1: "right", 2: "up", 3: "down"}
