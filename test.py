#!/usr/bin/env python

import game_display
from gi.repository import Gtk

gd = game_display.GameDisplay()
gd.win.connect('destroy', Gtk.main_quit)

Gtk.main()
