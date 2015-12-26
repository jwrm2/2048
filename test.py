#!/usr/bin/env python

# import game_interactive
# from gi.repository import Gtk

# gi = game_interactive.GameInteractive()
# gi.win.connect('destroy', Gtk.main_quit)
# Gtk.main()

# import controller

# c = controller.Controller(4, [4, 4])
# score = 0
# for i in range(100):
#    score += controller.run_game(c)
# print "Average score = " + str(score / 100)

import genetic

genetic.run_breeding(pop=100, sel=10, grid_size=4, hidden_list=[16, 16], drift=0.1, sigma=0.1, gen=10, num=10, proc=2)
