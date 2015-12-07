from gi.repository import Gtk
from gi.repository import Gdk
import os
from simplecrypt import encrypt, decrypt
from utils import get_password

import game
import game_display as gd


class GameInteractive(gd.GameDisplay):
    """A game of 2048 with a display and interactive moving."""

    def __init__(self):
        """Initialise the game and the display."""
        super(GameInteractive, self).__init__()
        if os.path.isfile(save_file):
            self._load_save()

    def _create_display(self):
        """Sets up the window ready for display."""
        self.win = Gtk.Window()
        self.win.set_title("2048 Interactive")
        self.win.set_default_size(gd.gridRight + gd.rightBorder, gd.gridBottom + gd.bottomBorder + buttonHeight)
        self.win.connect("key-press-event", self._key_pressed)

        grid = Gtk.Grid()
        self.win.add(grid)

        da = Gtk.DrawingArea()
        da.set_size_request(gd.gridRight + gd.rightBorder, gd.gridBottom + gd.bottomBorder)
        da.connect("draw", self.update_display)
        grid.attach(da, 0, 0, 2, 1)

        button = Gtk.Button.new_with_label("New Game")
        button.connect("clicked", self._start_new)
        align = Gtk.Alignment()
        align.set(xalign=0.5, yalign=0.5, xscale=0.0, yscale=0.0)
        align.add(button)
        grid.attach(align, 0, 1, 1, 1)

        button = Gtk.Button.new_with_label("Save and Quit")
        button.connect("clicked", self._save_quit)
        align = Gtk.Alignment()
        align.set(xalign=0.5, yalign=0.5, xscale=0.0, yscale=0.0)
        align.add(button)
        grid.attach(align, 1, 1, 1, 1)

        self.win.show_all()

    def _load_save(self):
        """Loads the saved game file."""

    def _key_pressed(self, widget, event):
        """Deals with keys pressed to make moves"""
        del widget
        key_name = Gdk.keyval_name(event.keyval).lower()
        if key_name in game.moves.values():
            self.make_move(key_name)
        self.win.queue_draw()
        return True

    def _start_new(self, button):
        """Starts a new game."""
        del button
        self.new_game()
        self.win.queue_draw()

    def _save_quit(self, button):
        """Writes the game data to a file and exits."""
        del button

        save = open(save_file, 'w')
        save_string = ""
        save_string += str(self.score) + '\n'
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                save_string += str(self.grid[i][j]) + '\n'

        cipher_text = encrypt(get_password(), save_string)
        save.write(cipher_text)
        save.close()

        Gtk.main_quit()


buttonHeight = 30
save_file = "save_game"
