#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')

import cairo
from gi.repository import Gtk


class Screen(Gtk.DrawingArea):

    """
    Playing Screen
    """

    def __init__(self):
        Gtk.DrawingArea.__init__(self)
        self.connect('delete-event', Gtk.main_quit)
        self.connect('draw', self.__draw)

        self.show_all()

    def __draw(self, screen, ctx):
        self.__init_background(ctx)

        ctx.scale(self.size, self.size)
        ctx.set_source_rgb(0, 0, 0)
        ctx.set_line_width(self.line_width)
        ctx.set_tolerance(0.1)

        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.set_dash([], 0)

        ctx.translate(0.1, 0.1)

    def __init_background(self, ctx):
        """Draw the background for the screen

        :ctx: cairo region
        :returns: void

        """
        pat = cairo.LinearGradient(0.0, 0.0, 0.0, 1.0)
        pat.add_color_stop_rgba(0.8, 0.8, 0.8, 0.8, 1)

        ctx.rectangle(0, 0, self.size, self.size)
        ctx.set_source(pat)
        ctx.fill()

        pass

    line_width = 2
    size = 500
    cell_size = size / 10


if __name__ == '__main__':
    print("Hello there! Please do not execute this file alone.")
