#!/usr/bin/env python3

try:
    import gi
    gi.require_version('Gtk', '3.0')
except ImportError:
    raise('Cannot import "gi" repository')

try:
    from gi.repository import Gtk
except ImportError:
    raise('Cannot import "Gtk" framework')

try:
    from gi.repository import Gdk
except ImportError:
    raise('Cannot import "Gdk" framework')

try:
    import cairo
except ImportError:
    raise('Cannot import "cairo" framework')


class Screen(Gtk.DrawingArea):

    """
    Custom widget to act as playing screen
    """

    def __init__(self, matrix):
        Gtk.DrawingArea.__init__(self)
        self.connect('draw', self.__on_draw)
        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.set_size_request(self.size, self.size)

        self.matrix = matrix

        self.show_all()

    def __on_draw(self, widget, ctx):
        # Init board
        self.__init_board(ctx)
        self.__draw_matrix(self.matrix, ctx)

    def __init_board(self, ctx):
        """Draw chess board

        :ctx: cairo context
        :returns: none

        """
        ctx.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
        # Fill background's color
        ctx.set_source_rgb(self.bg_color['r'], self.bg_color['g'],
                           self.bg_color['b'])
        ctx.rectangle(0, 0, self.size, self.size)
        ctx.fill()

        # Draw matrix
        ctx.set_source_rgb(self.fg_color['r'], self.fg_color['g'],
                           self.fg_color['b'])

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
        self.print_matrix()

    def __on_mouse_press(self, widget, event):
        pass

    def draw_piece(self, ctx, position_x, position_y, color, border=False):
        """Draw piece on selected position

        :position_x: row number in matrix
        :position_y: column number in matrix
        :color: color in format {'r': x, 'g': float, 'b': float} where
                float is a float in a number from 0 to 1
        :returns: none

        """
        ctx.set_source_rgb(color['r'], color['g'], color['b'])
        ctx.arc((position_y + 1) * self.cell_size + self.cell_size / 2,
                (position_x + 1) * self.cell_size + self.cell_size / 2,
                self.cell_size / 2 - 5, 0, 7.2)
        ctx.fill()

        if border:
            ctx.set_line_width(1)
            ctx.set_source_rgb(self.fg_color['r'], self.fg_color['g'],
                               self.fg_color['b'])
            ctx.arc((position_y + 1) * self.cell_size + self.cell_size / 2,
                    (position_x + 1) * self.cell_size + self.cell_size / 2,
                    self.cell_size / 2 - 5, 0, 7.2)
            ctx.stroke()

    def connect_positions(self, x0, y0, x1, y1, color):
        """Draw pieces on connected places. Use this to draw a scored line.

        :x0: TODO
        :y0: TODO
        :x1: TODO
        :y1: TODO
        :color: TODO
        :returns: none
        """

    def set_color(self, player_color, computer_color):
        """Set color for player and computer's pieces

        :player_color: TODO
        :computer_color: TODO
        :returns: none
        """
        self.player_color = player_color
        self.computer_color = computer_color

    def __draw_matrix(self, matrix, ctx):
        """
        Draw the screen based on matrix
        :matrix: matrix of 8x8
        :returns: none
        """

        for row in range(8):
            for col in range(8):
                if matrix[row][col] == 1:
                    self.draw_piece(ctx, row, col, self.player_color, True)
                elif matrix[row][col] == 2:
                    self.draw_piece(ctx, row, col, self.computer_color, True)
                else:
                    self.draw_piece(ctx, row, col, self.bg_color)

    def print_matrix(self):
        for i in range(8):
            print(self.matrix[i][:])

        print("")

    def game_pause(self, ctx):
        pass

    def game_resume(self, ctx):
        pass

    matrix = None
    board_line_width = 2
    size = 500
    cell_size = size / 10

    bg_color = {'r': 0.95, 'g': 0.95, 'b': 0.95}  # Gray
    fg_color = {'r': 0, 'g': 0, 'b': 0}  # Black

    player_color = {'r': 0, 'g': 0, 'b': 0}  # Black
    computer_color = {'r': 1, 'g': 1, 'b': 1}  # White

    current_player = None

if __name__ == '__main__':
    print("Hello there! Please do not execute this file alone.")
