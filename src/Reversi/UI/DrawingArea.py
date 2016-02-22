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


class DrawingArea(Gtk.DrawingArea):

    """
    Custom widget to act as playing screen
    """

    def __init__(self, matrix, *args):
        Gtk.DrawingArea.__init__(self)
        self.connect('draw', self.__on_draw)
        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.add_events(Gdk.EventMask.BUTTON_RELEASE_MASK)
        self.set_size_request(self.size, self.size)

        self.matrix = matrix

        self.show_all()

    def __on_draw(self, widget, ctx):
        # Init board
        if self.is_paused:
            self.__draw_pause_screen(ctx)
        else:
            self.__init_board(ctx)
            self.__draw_matrix(self.matrix, ctx)

    def __init_board(self, ctx):
        """Draw chess board

        :ctx: cairo context
        :returns: none

        """
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

    def __on_mouse_press(self, widget, event):
        pass

    def draw_piece(self, ctx, position_x, position_y, color,
                   border=False):
        """Draw piece on selected position

        :position_x: row number in matrix
        :position_y: column number in matrix
        :color: color in format {'r': val, 'g': val, 'b': val, 'a': val}
                where val is a float in a number from 0 to 1
        :returns: none

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
        """Draw pause screen

        :returns: none

        """
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

    def set_color(self, player_color, computer_color):
        """Set color for player and computer's pieces

        :player_color: color in format {'r': val, 'g': val, 'b': val, 'a': val}
                       where val is a float in a number from 0 to 1
        :computer_color: color in format {'r': val, 'g': val, 'b': val,
                        'a': val} where val is a float in a number from 0 to 1
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

    matrix = None
    board_line_width = 2
    size = 500
    cell_size = size / 10
    radius = cell_size / 2 - 5
    pause_msg = "GAME PAUSED"
    is_paused = False

    bg_color = {'r': 0.9, 'g': 0.9, 'b': 0.9, 'a': 1}  # Gray
    fg_color = {'r': 0, 'g': 0, 'b': 0, 'a': 1}  # Black

    player_color = {'r': 0, 'g': 0, 'b': 0, 'a': 1}  # Black
    computer_color = {'r': 1, 'g': 1, 'b': 1, 'a': 1}  # White
    hint_color = {'r': player_color['r'], 'g': player_color['r'],
                  'b': player_color['b'], 'a': player_color['a'] / 2}
