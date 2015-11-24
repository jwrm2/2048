#!/usr/bin/env python

import game_interactive
from gi.repository import Gtk

gi = game_interactive.GameInteractive()
gi.win.connect('destroy', Gtk.main_quit)

Gtk.main()
