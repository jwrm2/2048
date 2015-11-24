import game_display as gd
from gi.repository import Gtk

class GameInteractive(gd.GameDisplay):
  """A game of 2048 with a display and interactive moving."""

  def __init__(self):
    """Initialise the game and the display."""
    super(GameInteractive, self).__init__()

  def _createDisplay(self):
    """Sets up the window ready for display."""
    self.win = Gtk.Window()
    self.win.set_title("2048 Interactive")
    self.win.set_default_size(gd.gridRight + gd.rightBorder, gd.gridBottom + gd.bottomBorder + buttonHeight)

    hbox = Gtk.Box(spacing=6)
    self.win.add(hbox)

    self.da = Gtk.DrawingArea()
    self.da.set_size_request(gd.gridRight + gd.rightBorder, gd.gridBottom + gd.bottomBorder)
    self.da.connect("draw", self.updateDisplay)
    hbox.pack_start(self.da, True, True, 0)

    button = Gtk.Button.new_with_label("New Game")
    button.connect("clicked", self._startNew)
    hbox.pack_start(button, True, True, 0)

    button = Gtk.Button.new_with_label("Save and Quit")
    button.connect("clicked", self._saveQuit)
    hbox.pack_start(button, True, True, 0)

    self.win.show_all()

  def _startNew(self):
    """Starts a new game."""
    self.newGame()
    self.updateDisplay()

  def _saveQuit(self):
    """Writes the game data to a file and exits."""

buttonHeight = 50
