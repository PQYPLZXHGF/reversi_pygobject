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

import random
import UI
import Leaderboard


class Application(Gtk.Window):

    """
    Main window of game.
    """

    def __init__(self):
        """
        Initialize Application Window
        """
        Gtk.Window.__init__(self)

        # Default properties
        self.set_title("reversi")
        self.set_border_width(10)
        self.set_resizable(False)

        # Default events
        self.connect('delete-event', Gtk.main_quit)

        # Initialize the matrix
        self.__init_matrix()

        # Create Title bar
        header = Gtk.HeaderBar(title='Reversi 0.1',
                               subtitle="TDT University - Spring 2016",
                               show_close_button=True)
        self.set_titlebar(header)

        # Create main container
        self.hcontainer = Gtk.HBox(spacing=10)
        self.add(self.hcontainer)

        # Create drawing area
        self.screen = UI.Screen(self.matrix)
        self.screen.connect('button-press-event',
                            self.on_mouse_pressed_drawingarea)
        self.screen.connect('button-release-event',
                            self.on_mouse_released_drawingarea)
        self.hcontainer.pack_start(self.screen, True, True, 0)

        # Create right panel
        vbox_panel = Gtk.VBox()
        self.__init_panel(vbox_panel)
        self.hcontainer.pack_end(vbox_panel, False, False, 0)

        # Display Application Window
        self.show_all()

    def __init_matrix(self):
        """Initialize the matrix

        :returns: none

        """
        self.matrix = [[0 for col in range(8)] for row in range(8)]
        self.matrix[3][4] = 1
        self.matrix[4][3] = 1
        self.matrix[3][3] = 2
        self.matrix[4][4] = 2

    def __init_panel(self, widget):
        """Initialize right panel and connect it to events

        :widget: container
        :returns: none

        """
        # Create panel labels

        lbl_information = Gtk.Label()
        lbl_information.set_markup("<b>Information</b>")

        lbl_score = Gtk.Label()
        lbl_score.set_markup("<b>Score</b>")

        lbl_setting = Gtk.Label()
        lbl_setting.set_markup('<b>Setting</b>')

        lbl_time = Gtk.Label(halign=Gtk.Align.START)
        lbl_time.set_label("Time")

        lbl_turn = Gtk.Label(halign=Gtk.Align.START)
        lbl_turn.set_label("Turn")

        lbl_score_player = Gtk.Label(halign=Gtk.Align.START)
        lbl_score_player.set_label(self.player_label)

        lbl_score_computer = Gtk.Label(halign=Gtk.Align.START)
        lbl_score_computer.set_label(self.computer_label)

        lbl_showhint = Gtk.Label(halign=Gtk.Align.START)
        lbl_showhint.set_label('Show hint')

        lbl_showmove = Gtk.Label(halign=Gtk.Align.START)
        lbl_showmove.set_label('Show move')

        lbl_time_count = Gtk.Label(halign=Gtk.Align.END)
        lbl_time_count.set_label(repr(self.timer))

        lbl_turn_count = Gtk.Label(halign=Gtk.Align.END)
        lbl_turn_count.set_label(repr(self.turn))

        lbl_score_player_count = Gtk.Label(halign=Gtk.Align.END)
        lbl_score_player_count.set_label(repr(self.player_score))

        lbl_score_computer_count = Gtk.Label(halign=Gtk.Align.END)
        lbl_score_computer_count.set_label(repr(self.computer_score))

        # Create buttons
        self.btn_start = Gtk.Button()
        self.btn_start.set_label("Start Game")
        self.btn_start.set_size_request(-1, 50)
        self.btn_start.connect('clicked', self.on_button_start_clicked)

        self.btn_hiscore = Gtk.Button()
        self.btn_hiscore.set_label("High Scores")
        self.btn_hiscore.set_size_request(-1, 50)
        self.btn_hiscore.connect('clicked', self.on_button_hiscore_clicked)

        self.btn_quit = Gtk.Button()
        self.btn_quit.set_size_request(-1, 50)
        self.btn_quit.set_label("Quit")
        self.btn_quit.connect('clicked', self.on_button_quit_clicked)

        self.switch_hint = Gtk.Switch(valign=Gtk.Align.END)
        self.switch_hint.connect('notify::active',
                                 self.on_switch_hint_activated)

        self.switch_show_moves = Gtk.Switch(valign=Gtk.Align.END)
        self.switch_show_moves.set_active(True)
        self.switch_show_moves.connect('notify::active',
                                       self.on_switch_show_move_activated)

        # Right panel listbox
        panel_listbox = Gtk.ListBox(selection_mode=Gtk.SelectionMode.NONE)
        widget.add(panel_listbox)

        # Sysinfo Label
        row = Gtk.ListBoxRow()
        row.add(lbl_information)
        panel_listbox.add(row)

        # Timer row
        row = Gtk.ListBoxRow()
        hbox = Gtk.HBox(spacing=50)
        hbox.pack_start(lbl_time, True, True, 0)
        hbox.pack_start(lbl_time_count, True, True, 0)
        row.add(hbox)
        panel_listbox.add(row)

        # Turn row
        row = Gtk.ListBoxRow()
        hbox = Gtk.HBox(spacing=50)
        hbox.add(lbl_turn)
        hbox.add(lbl_turn_count)
        row.add(hbox)
        panel_listbox.add(row)

        # Blank Row
        row = Gtk.ListBoxRow()
        lbl_blank = Gtk.Label()
        lbl_blank.set_label("")
        row.add(lbl_blank)
        panel_listbox.add(row)

        # Score Row
        row = Gtk.ListBoxRow()
        row.add(lbl_score)
        panel_listbox.add(row)

        # Player's score row
        row = Gtk.ListBoxRow()
        hbox = Gtk.HBox(spacing=50)
        hbox.add(lbl_score_player)
        hbox.add(lbl_score_player_count)
        row.add(hbox)
        panel_listbox.add(row)

        # Computer's score row
        row = Gtk.ListBoxRow()
        hbox = Gtk.HBox(spacing=50)
        hbox.add(lbl_score_computer)
        hbox.add(lbl_score_computer_count)
        row.add(hbox)
        panel_listbox.add(row)

        # Blank row
        row = Gtk.ListBoxRow()
        lbl_blank = Gtk.Label()
        lbl_blank.set_label("")
        row.add(lbl_blank)
        panel_listbox.add(row)

        # Setting row
        row = Gtk.ListBoxRow()
        row.add(lbl_setting)
        panel_listbox.add(row)

        # Show hints row
        row = Gtk.ListBoxRow()
        hbox = Gtk.HBox(spacing=50)
        hbox.pack_start(lbl_showhint, True, True, 0)
        hbox.pack_start(self.switch_hint, False, True, 0)
        row.add(hbox)
        panel_listbox.add(row)

        # Show hints row
        row = Gtk.ListBoxRow()
        hbox = Gtk.HBox(spacing=50)
        hbox.pack_start(lbl_showmove, True, True, 0)
        hbox.pack_start(self.switch_show_moves, False, True, 0)
        row.add(hbox)
        panel_listbox.add(row)

        # Add buttons to the bottom
        widget.pack_end(self.btn_quit, False, True, 0)
        widget.pack_end(self.btn_hiscore, False, True, 0)
        widget.pack_end(self.btn_start, False, True, 0)

    def __init_newgame(self):
        """Initialize new game

        :returns: none

        """
        self.__init_matrix()
        self.screen.matrix = self.matrix
        self.game_state = 1
        self.timer = 0
        self.turn = 0
        self.player_score = 0
        self.computer_score = 0

    def on_button_start_clicked(self, button):
        """Start game and change the label to "restart",
        "High Scores" label to "Pause"

        :button: button
        :return: none

        """
        self.turn = random.randint(1, 2)

        if self.game_state == 1:
            self.__init_matrix()
            self.screen.matrix = self.matrix
            self.screen.queue_draw()
        elif self.game_state == 2:
            pass
        else:  # self.game_state == 0
            button.set_label('Restart')
            self.btn_hiscore.set_label('Pause')
            self.btn_quit.set_label('Surrender')
            self.game_state = 1
            self.__init_matrix()
            self.screen.matrix = self.matrix
            self.screen.queue_draw()
        pass

    def on_mouse_pressed_drawingarea(self, widget, event):
        """Handle mouse press event: Save current mouse clicked position and
        pass the event to next handler.

        :widget: Gtk.DrawingArea
        :event: mouse event
        :return: none

        """

        self.pre_x, self.pre_y = self.get_position_in_matrix(int(event.x),
                                                             int(event.y))

        return False  # Pass the event to next handler

    def on_mouse_released_drawingarea(self, widget, event):
        """Handle mouse release on drawing area

        :widget: Gtk.DrawingArea
        :event: mouse click
        :returns: none

        """
        row, col = self.get_position_in_matrix(int(event.x), int(event.y))

        """
        Check if mouse pressed event and mouse released event is is the
        same cell. If not, ignore move.
        """
        if not (self.pre_x == row and self.pre_y == col):
            return

        # if self.turn == 1 and self.is_valid_move(row, col):
        # TODO recheck
        if self.is_valid_move(row, col):
            self.matrix[row][col] = self.turn
            widget.queue_draw()
            self.turn_switch()

        return True

    def on_button_hiscore_clicked(self, button, args=""):
        """Show the leaderboard and receive new high score (if any).

        :button: button
        :args: current score and time
        :returns: none

        """
        leaderboard = Leaderboard.Leaderboard()
        leaderboard.add_highscore(args)
        leaderboard.show_all()

        pass

    def on_button_quit_clicked(self, button, args=""):
        """Show the quit confirmation dialog.

        :button: button
        :args: TODO
        :returns: none
        """
        if self.game_state == 1:
            self.game_state = 0
            self.btn_start.set_label('Start Over')
            self.btn_hiscore.set_label('High Scores')
            button.set_label('Quit')
            self.turn = 0
        else:
            dialog = Gtk.MessageDialog(parent=self)
            dialog.set_markup("<b><big>Do you want to quit?</big></b>")
            dialog.format_secondary_text("We will wait for you!")
            dialog.set_properties('buttons', Gtk.ButtonsType.NONE)
            dialog.set_properties('message-type', Gtk.MessageType.QUESTION)

            dialog.add_button("Not now", Gtk.ResponseType.CANCEL)
            dialog.add_button("I said quit!", Gtk.ResponseType.OK)

            response = dialog.run()

            if response == Gtk.ResponseType.OK:
                Gtk.main_quit(self)
            else:
                pass

            dialog.destroy()

    def on_button_restart_clicked(self, button):
        pass

    def on_switch_hint_activated(self, switch, args=""):
        """Show hints.

        :switch: switch
        :args: TODO
        :returns: none
        """
        if switch.get_active():
            state = "on"
        else:
            state = "off"

        print("Switch \"Show hint\" was turned", state)

    def on_switch_show_move_activated(self, switch, args=""):
        """Show moves.

        :switch: switch
        :args: TODO
        :returns: none
        """
        if switch.get_active():
            state = "on"
        else:
            state = "off"

        print("Switch \"Show moves\" was turned", state)

    def is_valid_move(self, x, y):
        """Check if the movement in current position is a valid move

        :x: matrix row
        :y: matrix column
        :returns: True if is a valid move, false otherwise


        """
        if self.matrix[x][y] != 0:
            return False

        if x >= 0 and y >= 0:
            return True

        return False

    def get_valid_moves(self, x, y):
        """Get a list of valid moves for the current position

        :x: matrix row
        :y: matrix column
        :returns: List of valid moves for current turn

        """
        if self.turn == 1:
            pass
        elif self.turn == 2:
            pass

    def get_position_in_matrix(self, position_x, position_y):
        """Determine the current pair of x, y position is in which cell of
           matrix

        :position_x: x position in pixel
        :position_y: y position in pixel
        :returns: position x, y of matrix, (-1, -1) if out-of-bound
        """
        if (position_x < self.screen.cell_size) \
           or (position_x > self.screen.size - self.screen.cell_size) \
           or (position_y < self.screen.cell_size) \
           or (position_y > self.screen.size - self.screen.cell_size):
            return -1, -1

        for row in range(8):
            if (row + 2) * self.screen.cell_size > position_y:
                break

        for col in range(8):
            if (col + 2) * self.screen.cell_size > position_x:
                break

        return row, col

    def turn_switch(self):
        if self.turn == 1:
            self.turn = 2
        elif self.turn == 2:
            self.turn = 1

    def connect_positions(self, x0, y0, x1, y1, color):
        """Draw pieces on connected places. Use this to draw a scored line.

        :x0: matrix's x source position
        :y0: matrix's y source position
        :x1: matrix's x destination position
        :y1: matrix's y destination position
        :color: color in format {'r': val, 'g': val, 'b': val} where
                'val' is a float in a number from 0 to 1

        :returns: none
        """
        pass

    timer = 0.00
    turn = 0
    player_label = "Player"
    player_score = 0
    computer_label = "Computer"
    computer_score = 0
    game_state = 0

    pre_x = None
    pre_y = None

    matrix = None

application = Application()
Gtk.main()
