import game_display
from gi.repository import Gtk

class GameInteractive(game_display.GameDisplay):
  """A game of 2048 with a display and interactive moving."""

  def __init__(self):
    """Initialise the game and the display."""
    super(GameInteractive, self).__init__()
    self._createDisplay()

  def _createDisplay(self):
    """Sets up the window ready for display."""

    self.bottomBox = Gtk.Box(spacing = 50)
    self.add(bottomBox)

    self.newGameButton = Gtk.Button(label="New Game")
    self.newGameButton.connect("clicked", self.newGame)
    self.bottomBox.pack_start(self.newGameButton, True, True, 0)

    self.saveButton = Gtk.Button(label="Save & Quit")
    self.saveButton.connect("clicked", self._saveQuit)
    self.bottomBox.pack_start(self.saveButton, True, True, 0)

  def _saveQuit(self):
    """Writes the game data to a file and exits."""

