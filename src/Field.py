#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')

import cairo
from gi.repository import Gtk


class DrawingArea(Gtk.DrawingArea):

    def __init__(self):
        Gtk.DrawingArea.__init__(self)
        self.connect('delete-event', Gtk.main_quit)

        self.show_all()

if __name__ == '__main__':
    print("It's working!")
