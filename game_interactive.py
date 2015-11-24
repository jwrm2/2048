import game_display as gd
from gi.repository import Gtk

#----------------------------------------------------------------------------------------------------------------------------------

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

    grid = Gtk.Grid()
    self.win.add(grid)

    da = Gtk.DrawingArea()
    da.set_size_request(gd.gridRight + gd.rightBorder, gd.gridBottom + gd.bottomBorder)
    da.connect("draw", self.updateDisplay)
    grid.attach(da, 0, 0, 2, 1)

    button = Gtk.Button.new_with_label("New Game")
    button.connect("clicked", self._startNew)
    align = Gtk.Alignment()
    align.set(xalign=0.5, yalign=0.5, xscale=0.0, yscale=0.0)
    align.add(button)
    grid.attach(align, 0, 1, 1, 1)

    button = Gtk.Button.new_with_label("Save and Quit")
    button.connect("clicked", self._saveQuit)
    align = Gtk.Alignment()
    align.set(xalign=0.5, yalign=0.5, xscale=0.0, yscale=0.0)
    align.add(button)
    grid.attach(align, 1, 1, 1, 1)

    self.win.show_all()

  def _startNew(self, button):
    """Starts a new game."""
    self.newGame()
    self.win.queue_draw()

  def _saveQuit(self, button):
    """Writes the game data to a file and exits."""

#----------------------------------------------------------------------------------------------------------------------------------

buttonHeight = 30
