#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk


class Leaderboard(Gtk.Window):

    """Leaderboard to save high scores."""

    def __init__(self, *args):
        """Initialize the leaderboard.

        :new_score: TODO

        """
        Gtk.Window.__init__(self)
        self.connect('delete-event', self.__on_quit)

    def add_highscore(self, *args):
        """Add new high score to the leaderboard.

        :name: player's name
        :score: player's score
        :time: time taken
        :returns: none

        """
        pass

    def __on_quit(self, widget, param):
        Gtk.Window.hide(self)
