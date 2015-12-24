#!/usr/bin/env python

#import game_interactive
#from gi.repository import Gtk

#gi = game_interactive.GameInteractive()
#gi.win.connect('destroy', Gtk.main_quit)
#Gtk.main()

import controller

c = controller.Controller(4, [4, 4])
score = 0
for i in range(100):
  score += controller.run_game(c)
print "Average score = " + str(score / 100)

