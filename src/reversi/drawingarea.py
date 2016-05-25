#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')

import cairo
from gi.repository import Gtk, Gdk


class DrawingArea(Gtk.DrawingArea):
    """Custom widget to use as game screen"""

    def __init__(self, matrix, *args):
        Gtk.DrawingArea.__init__(self)
        self.connect('draw', self.__on_draw)
        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.add_events(Gdk.EventMask.BUTTON_RELEASE_MASK)

        # Init values
        self.matrix = matrix
        self.board_line_width = 2
        self.size = 500
        self.cell_size = self.size / 10
        self.radius = self.cell_size / 2 - 5
        self.pause_msg = "GAME PAUSED"
        self.is_paused = False

        self.bg_color = {'r': 0.9, 'g': 0.9, 'b': 0.9, 'a': 1}  # Gray
        self.fg_color = {'r': 0, 'g': 0, 'b': 0, 'a': 1}  # Black
        self.player_color = {'r': 0, 'g': 0, 'b': 0, 'a': 1}  # Black
        self.computer_color = {'r': 1, 'g': 1, 'b': 1, 'a': 1}  # White
        self.hint_color = {'r': self.player_color['r'],
                           'g': self.player_color['r'],
                           'b': self.player_color['b'],
                           'a': self.player_color['a'] / 2}

        self.set_size_request(self.size, self.size)
        self.show_all()

    def __on_draw(self, widget, ctx):
        # Init board
        if self.is_paused:
            self.__draw_pause_screen(ctx)
        else:
            self.__init_board(ctx)
            self.__draw_matrix(self.matrix, ctx)

    def __init_board(self, ctx):
        """Draw chess board"""
        ctx.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
        # Fill background's color
        ctx.set_source_rgba(self.bg_color['r'], self.bg_color['g'],
                            self.bg_color['b'], self.bg_color['a'])
        ctx.rectangle(0, 0, self.size, self.size)
        ctx.fill()

        # Draw matrix
        ctx.set_source_rgba(self.fg_color['r'], self.fg_color['g'],
                            self.fg_color['b'], self.fg_color['a'])

        for i in range(1, 10):
            ctx.move_to(self.cell_size * i, self.cell_size)
            ctx.line_to(self.cell_size * i, self.size - self.cell_size)
            ctx.move_to(self.cell_size, self.cell_size * i)
            ctx.line_to(self.size - self.cell_size, self.cell_size * i)

        ctx.stroke()

        # Draw border's texts
        ctx.select_font_face("PragmataPro for Powerline",
                             cairo.FONT_SLANT_NORMAL,
                             cairo.FONT_WEIGHT_NORMAL)
        ctx.set_font_size(30)

        for i in range(1, 9):
            x_bearing, y_bearing, width, height = \
                ctx.text_extents(repr(i))[:4]

            # Top border's texts
            ctx.move_to(self.cell_size * i + self.cell_size / 2 -
                        width / 2 - x_bearing,
                        self.cell_size / 2 - height / 2 - y_bearing)
            ctx.show_text(repr(i))

            # Bottom border's texts
            ctx.move_to(self.cell_size * i + self.cell_size / 2 -
                        width / 2 - x_bearing,
                        self.size - self.cell_size / 2 -
                        height / 2 - y_bearing)
            ctx.show_text(repr(i))

        ctx.stroke()  # Flush ctx

        # Draw border's numbers
        for i, char in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']):
            x_bearing, y_bearing, width, height = \
                ctx.text_extents(char)[:4]

            # Left border's texts
            ctx.move_to(self.cell_size / 2 - width / 2 - x_bearing,
                        self.cell_size * (i + 1) + self.cell_size / 2 -
                        height / 2 - y_bearing)
            ctx.show_text(char)

            # Right border's texts:
            ctx.move_to(self.size - self.cell_size / 2 -
                        width / 2 - x_bearing,
                        self.cell_size * (i + 1) + self.cell_size / 2 -
                        height / 2 - y_bearing)
            ctx.show_text(char)

        ctx.stroke()  # Flux ctx

        self.__draw_matrix(self.matrix, ctx)

    def draw_piece(self, ctx, position_x, position_y, color,
                   border=False):
        """Draw piece on selected position

        :param border:
        :param color:
        :param ctx:
        :param position_x: row number in matrix
        :param position_y: column number in matrix
        """

        ctx.set_source_rgba(color['r'], color['g'], color['b'], color['a'])
        ctx.arc((position_y + 1) * self.cell_size + self.cell_size / 2,
                (position_x + 1) * self.cell_size + self.cell_size / 2,
                self.radius, 0, 7.2)
        ctx.fill()

        if border:
            ctx.set_line_width(1)
            ctx.set_source_rgba(self.fg_color['r'], self.fg_color['g'],
                                self.fg_color['b'], self.fg_color['a'])
            ctx.arc((position_y + 1) * self.cell_size + self.cell_size / 2,
                    (position_x + 1) * self.cell_size + self.cell_size / 2,
                    self.radius, 0, 7.2)
            ctx.stroke()

    def __draw_pause_screen(self, ctx):
        """Draw pause screen"""
        # Fill background
        ctx.set_source_rgba(self.bg_color['r'], self.bg_color['g'],
                            self.bg_color['b'], self.bg_color['a'])
        ctx.rectangle(0, 0, self.size, self.size)
        ctx.fill()

        # Draw pause msg
        ctx.select_font_face("PragmataPro for Powerline",
                             cairo.FONT_SLANT_NORMAL,
                             cairo.FONT_WEIGHT_NORMAL)
        ctx.set_font_size(60)

        ctx.set_source_rgba(self.fg_color['r'], self.fg_color['g'],
                            self.fg_color['b'], self.fg_color['a'])

        x_bearing, y_bearing, width, height = ctx.text_extents(
            self.pause_msg
        )[:4]

        ctx.move_to(self.size / 2 - width / 2,
                    self.size / 2 + height / 2)
        ctx.show_text(self.pause_msg)

    def redraw(self):
        """Redraw screen"""
        self.queue_draw()

    def set_color(self, player_color, computer_color):
        """Set color for player and computer's pieces"""
        self.player_color = player_color
        self.computer_color = computer_color

    def __draw_matrix(self, matrix, ctx):
        """Draw the pieces on the screen based on matrix"""

        for row in range(8):
            for col in range(8):
                if matrix[row][col] == 1:
                    self.draw_piece(ctx, row, col, self.player_color, True)
                elif matrix[row][col] == 2:
                    self.draw_piece(ctx, row, col, self.computer_color, True)
                elif matrix[row][col] == -1:
                    self.draw_piece(ctx, row, col, self.hint_color, False)
                else:
                    self.draw_piece(ctx, row, col, self.bg_color)
