import cairo, game, utils
from gi.repository import Gtk

#----------------------------------------------------------------------------------------------------------------------------------

class GameDisplay(game.Game):
  """A game of 2048 with a display."""

  def __init__(self):
    """Initialise the game and the display."""
    super(GameDisplay, self).__init__()
    self._createDisplay()

  def _createDisplay(self):
    """Sets up the window ready for display."""
    self.win = Gtk.Window()
    self.win.set_title("2048")
    self.win.set_default_size(gridRight + rightBorder, gridBottom + bottomBorder)

    self.da = Gtk.DrawingArea()
    self.da.connect("draw", self.updateDisplay)
    self.win.add(self.da)

    self.win.show_all()

  def updateDisplay(self, w, cr):
    """Draws to the drawing area display."""
    # Background color and cleaning
    cr.set_source_rgb(backgroundColor.getRedF(), backgroundColor.getGreenF(), backgroundColor.getBlueF())
    cr.paint()

    # The grid
    cr.set_line_width(gridLineWidth)
    cr.set_source_rgb(gridColor.getRedF(), gridColor.getGreenF(), gridColor.getBlueF())
    for i in range(self.gridSize+1):
      cr.move_to(gridLeft + i*tileSize + (i-0.5)*gridLineWidth, gridTop - gridLineWidth)
      cr.line_to(gridLeft + i*tileSize + (i-0.5)*gridLineWidth, gridBottom - gridLineWidth/2)
      cr.stroke_preserve()
      cr.move_to(gridLeft  - gridLineWidth, gridTop + i*tileSize + (i-0.5)*gridLineWidth)
      cr.line_to(gridRight - gridLineWidth/2, gridTop + i*tileSize + (i-0.5)*gridLineWidth)
      cr.stroke_preserve()

    # The tiles
    for i in range(self.gridSize):
      for j in range(self.gridSize):
        if(self.grid[i][j] != 0):
          color = tileColors[self.grid[i][j]]
          cr.set_source_rgb(color.getRedF(), color.getGreenF(), color.getBlueF())
          cr.rectangle(gridLeft + gridLineWidth*i + tileSize*i,     gridTop + gridLineWidth*j + tileSize*j,
                       tileSize, tileSize)
          cr.fill()

    # The tile labels
    for i in range(self.gridSize):
      for j in range(self.gridSize):
        if(self.grid[i][j] != 0):
          color = labelColor[labelDict[self.grid[i][j]]]
          cr.set_source_rgb(color.getRedF(), color.getGreenF(), color.getBlueF())
          cr.select_font_face("Helvetica", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
          cr.set_font_size(labelFontSize[self.grid[i][j]])
          (x, y, width, height, dx, dy) = cr.text_extents(str(self.grid[i][j]))
          cr.move_to(gridLeft + gridLineWidth*i + tileSize*(i+0.5) - width/2, gridTop + gridLineWidth*j + tileSize*(j+0.5) + height/2)
          cr.show_text(str(self.grid[i][j]))

#----------------------------------------------------------------------------------------------------------------------------------

backgroundColor = utils.HexColor("0xFAF8EF")
gridColor       = utils.HexColor("0xBBADA0")
squareColor     = utils.HexColor("0xCDC1B4")
labelColor      = [utils.HexColor("0x776E65"), utils.HexColor("0xF9F6F2")]
labelDict       = {2**i: 1 for i in range(3, 18)}
labelDict[2]    = 0
labelDict[4]    = 0
labelFontSize   = {2: 60, 4: 60, 8: 60,
                   16: 40, 32: 40, 64: 40,
                   128: 30, 256: 30, 512: 30,
                   1024: 25, 2048: 25, 4096: 25, 8192: 25,
                   16384: 20, 32768: 20, 65536: 20,
                   131072: 20}
tileColors      = {2:      utils.HexColor("0xEEE4DA"),
                   4:      utils.HexColor("0xEDE0C8"),
                   8:      utils.HexColor("0xF2B179"),
                   16:     utils.HexColor("0xF59563"),
                   32:     utils.HexColor("0xF67C5F"),
                   64:     utils.HexColor("0xF65E3B"),
                   128:    utils.HexColor("0xEDCF72"),
                   256:    utils.HexColor("0xEDCC61"),
                   512:    utils.HexColor("0xEDC850"),
                   1024:   utils.HexColor("0xEDC53F"),
                   2048:   utils.HexColor("0xEDC22E"),
                   4196:   utils.HexColor("0x3C3A32"),
                   8192:   utils.HexColor("0x3C3A32"),
                   16384:  utils.HexColor("0x3C3A32"),
                   32768:  utils.HexColor("0x3C3A32"),
                   65536:  utils.HexColor("0x3C3A32"),
                   131072: utils.HexColor("0x3C3A32")}

gridLineWidth = 20
tileSize      = 80
topBorder     = 50 + gridLineWidth
bottomBorder  = 50
leftBorder    = 50 + gridLineWidth
rightBorder   = 50

gridLeft   = leftBorder + gridLineWidth/2
gridRight  = leftBorder + 4*tileSize + 5*gridLineWidth
gridTop    = topBorder + gridLineWidth/2
gridBottom = topBorder + 4*tileSize + 5*gridLineWidth
