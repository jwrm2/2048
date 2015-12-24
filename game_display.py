import cairo
from gi.repository import Gtk

import game
import utils


class GameDisplay(game.Game):
    """A game of 2048 with a display."""

    def __init__(self):
        """Initialise the game and the display."""
        super(GameDisplay, self).__init__()
        self._create_display()

    def _create_display(self):
        """Sets up the window ready for display."""
        self.win = Gtk.Window()
        self.win.set_title("2048")
        self.win.set_default_size(grid_right + right_border, grid_bottom + bottom_border)

        self.da = Gtk.DrawingArea()
        self.da.connect("draw", self.update_display)
        self.win.add(self.da)

        self.win.show_all()

    def make_move(self, direction):
        """Carries out a move in the specified direction and queues a display update."""
        super(GameDisplay, self).make_move(direction)
        self.win.queue_draw()

    def update_display(self, w, cr):
        """Draws to the drawing area display.

        @param w: the widget to be drawn upon
        @param cr: the cairo drawing context
        """

        del w

        # Background color and cleaning
        cr.set_source_rgb(background_color.get_red_f(), background_color.get_green_f(), background_color.get_blue_f())
        cr.paint()

        # The score
        cr.set_source_rgb(score_color.get_red_f(), score_color.get_green_f(), score_color.get_blue_f())
        cr.select_font_face("Helvetica", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(score_size)
        (x, y, width, height, dx, dy) = cr.text_extents(str(self.score))
        cr.move_to(grid_right - width - grid_line_width/2, top_border/2 + height/2)
        cr.show_text(str(self.score))

        # The grid
        cr.set_line_width(grid_line_width)
        cr.set_source_rgb(grid_color.get_red_f(), grid_color.get_green_f(), grid_color.get_blue_f())
        for i in range(self.grid_size+1):
            cr.move_to(grid_left + i * tile_size + (i - 0.5) * grid_line_width, grid_top - grid_line_width)
            cr.line_to(grid_left + i * tile_size + (i - 0.5) * grid_line_width, grid_bottom - grid_line_width / 2)
            cr.stroke_preserve()
            cr.move_to(grid_left - grid_line_width, grid_top + i * tile_size + (i - 0.5) * grid_line_width)
            cr.line_to(grid_right - grid_line_width / 2, grid_top + i * tile_size + (i - 0.5) * grid_line_width)
            cr.stroke_preserve()

        # The tiles
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j] != 0:
                    color = tile_colors[self.grid[i][j]]
                    cr.set_source_rgb(color.get_red_f(), color.get_green_f(), color.get_blue_f())
                    cr.rectangle(grid_left + grid_line_width * i + tile_size * i,
                                 grid_top + grid_line_width * j + tile_size * j,
                                 tile_size, tile_size)
                    cr.fill()

        # The tile labels
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j] != 0:
                    color = label_color[label_dict[self.grid[i][j]]]
                    cr.set_source_rgb(color.get_red_f(), color.get_green_f(), color.get_blue_f())
                    cr.select_font_face("Helvetica", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
                    cr.set_font_size(label_font_size[self.grid[i][j]])
                    (x, y, width, height, dx, dy) = cr.text_extents(str(self.grid[i][j]))
                    cr.move_to(grid_left + grid_line_width * i + tile_size * (i + 0.5) - width / 2,
                               grid_top + grid_line_width * j + tile_size * (j + 0.5) + height / 2)
                    cr.show_text(str(self.grid[i][j]))


background_color = utils.HexColor("0xEDEDED")
grid_color = utils.HexColor("0xBBADA0")
score_color = utils.HexColor("0x776E65")
score_size = 40
square_color = utils.HexColor("0xCDC1B4")
label_color = [utils.HexColor("0x776E65"), utils.HexColor("0xF9F6F2")]
label_dict = {2 ** i: 1 for i in range(3, 18)}
label_dict[2] = 0
label_dict[4] = 0
label_font_size = {2: 60, 4: 60, 8: 60,
                   16: 40, 32: 40, 64: 40,
                   128: 30, 256: 30, 512: 30,
                   1024: 25, 2048: 25, 4096: 25, 8192: 25,
                   16384: 20, 32768: 20, 65536: 20,
                   131072: 20}
tile_colors = {2: utils.HexColor("0xEEE4DA"),
               4: utils.HexColor("0xEDE0C8"),
               8: utils.HexColor("0xF2B179"),
               16: utils.HexColor("0xF59563"),
               32: utils.HexColor("0xF67C5F"),
               64: utils.HexColor("0xF65E3B"),
               128: utils.HexColor("0xEDCF72"),
               256: utils.HexColor("0xEDCC61"),
               512: utils.HexColor("0xEDC850"),
               1024: utils.HexColor("0xEDC53F"),
               2048: utils.HexColor("0xEDC22E"),
               4096: utils.HexColor("0x3C3A32"),
               8192: utils.HexColor("0x3C3A32"),
               16384: utils.HexColor("0x3C3A32"),
               32768: utils.HexColor("0x3C3A32"),
               65536: utils.HexColor("0x3C3A32"),
               131072: utils.HexColor("0x3C3A32")}

grid_line_width = 20
tile_size = 80
top_border = 50 + grid_line_width
bottom_border = 50
left_border = 50 + grid_line_width
right_border = 50

grid_left = left_border + grid_line_width / 2
grid_right = left_border + 4 * tile_size + 5 * grid_line_width
grid_top = top_border + grid_line_width / 2
grid_bottom = top_border + 4 * tile_size + 5 * grid_line_width
