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
    from gi.repository import GLib
except ImportError:
    raise('Cannot import "GLib" framework')

import random
from Reversi.UI.DrawingArea import DrawingArea
from Reversi.UI.Leaderboard import Leaderboard
from Reversi.Engine.Game import GameStatus, Player


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

        # Initialize the new game
        self.__init_newgame()

        # Create Title bar
        header = Gtk.HeaderBar(title='Reversi 0.1',
                               subtitle="TDT University - Spring 2016",
                               show_close_button=True)
        self.set_titlebar(header)

        # Create main container
        self.hcontainer = Gtk.HBox(spacing=10)
        self.add(self.hcontainer)

        # Create drawing area
        self.screen = DrawingArea(self.matrix)
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
        lbl_showmove.set_label('Show debug log')

        self.lbl_time_count = Gtk.Label(halign=Gtk.Align.END)
        self.lbl_time_count.set_label(repr(self.timer))

        self.lbl_turn_count = Gtk.Label(halign=Gtk.Align.END)
        self.lbl_turn_count.set_label(repr(self.turn))

        self.lbl_score_player_count = Gtk.Label(halign=Gtk.Align.END)
        self.lbl_score_player_count.set_label(repr(self.player_score))

        self.lbl_score_computer_count = Gtk.Label(halign=Gtk.Align.END)
        self.lbl_score_computer_count.set_label(repr(self.computer_score))

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

        self.switch_show_debug = Gtk.Switch(valign=Gtk.Align.END)
        self.switch_show_debug.set_active(self.debug)
        self.switch_show_debug.connect('notify::active',
                                       self.on_switch_show_debug_activated)

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
        hbox.pack_start(self.lbl_time_count, True, True, 0)
        row.add(hbox)
        panel_listbox.add(row)

        # Turn row
        row = Gtk.ListBoxRow()
        hbox = Gtk.HBox(spacing=50)
        hbox.add(lbl_turn)
        hbox.add(self.lbl_turn_count)
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
        hbox.add(self.lbl_score_player_count)
        row.add(hbox)
        panel_listbox.add(row)

        # Computer's score row
        row = Gtk.ListBoxRow()
        hbox = Gtk.HBox(spacing=50)
        hbox.add(lbl_score_computer)
        hbox.add(self.lbl_score_computer_count)
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
        hbox.pack_start(self.switch_show_debug, False, True, 0)
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
        self.game_state = GameStatus.NONE
        self.timer = 0
        self.turn = 0
        self.current_player = Player.NONE
        self.player_score = 2
        self.computer_score = 2

        if self.matrix is None:
            self.matrix = [[0 for col in range(8)] for row in range(8)]

        for row in range(8):
            for col in range(8):
                self.matrix[row][col] = Player.NONE

        self.matrix[3][4] = Player.PLAYER
        self.matrix[4][3] = Player.PLAYER
        self.matrix[3][3] = Player.COMPUTER
        self.matrix[4][4] = Player.COMPUTER

        self.current_player = random.randint(1, 2)

    def do_start_game(self):
        self.__init_newgame()
        self.screen.queue_draw()
        self.current_player = Player().get_player()
        self.game_state = GameStatus.PLAYING
        self.run_time_counter()

        self.btn_start.set_label("Restart")
        self.btn_hiscore.set_label("Pause")
        self.btn_quit.set_label("Surrender")

        self.update_turn_label()
        self.update_score_label()

    def do_pause_game(self):
        self.game_state = GameStatus.PAUSED
        self.stop_time_counter()

        self.btn_start.set_label("Restart")
        self.btn_hiscore.set_label("Resume")
        self.btn_quit.set_label("Surrender")

        self.btn_start.set_sensitive(False)
        self.btn_quit.set_sensitive(False)

    def do_resume_game(self):
        self.game_state = GameStatus.PLAYING
        self.run_time_counter()

        self.btn_start.set_label("Restart")
        self.btn_hiscore.set_label("Pause")
        self.btn_quit.set_label("Surrender")

        self.btn_start.set_sensitive(True)
        self.btn_quit.set_sensitive(True)

    def do_stop_game(self):
        self.game_state = GameStatus.STOPPED
        self.stop_time_counter()
        self.btn_start.set_label("Start Over")
        self.btn_hiscore.set_label("High Scores")
        self.btn_quit.set_label("Quit")

    def on_button_start_clicked(self, button):
        """Handle Start/Restart button

        :returns: True

        """
        if self.game_state == GameStatus.NONE \
                or self.game_state == GameStatus.STOPPED:
            self.do_start_game()
            self.print_debug("\n===========================================")
            self.print_debug("Game started. Player", self.current_player,
                             "takes the first turn")
            self.print_debug("===========================================\n")
        else:
            self.do_pause_game()
            dialog = Gtk.MessageDialog(parent=self)
            dialog.set_markup("<b><big>Do you want to Restart?</big></b>")
            dialog.format_secondary_text("Note that all of your progress "
                                         "will be lost!")
            dialog.set_properties('buttons', Gtk.ButtonsType.NONE)
            dialog.set_properties('message-type', Gtk.MessageType.QUESTION)

            dialog.add_button("Maybe not...", Gtk.ResponseType.CANCEL)
            dialog.add_button("I know.", Gtk.ResponseType.OK)

            response = dialog.run()

            if response == Gtk.ResponseType.OK:
                self.stop_time_counter()
                self.do_start_game()
                self.print_debug(
                    "\n===========================================")
                self.print_debug("Game started. Player", self.current_player,
                                 "takes the first turn")
                self.print_debug(
                    "===========================================\n")
            else:
                self.do_resume_game()

            dialog.destroy()

        return True

    def on_button_hiscore_clicked(self, button, *args):
        """Show the leaderboard and receive new high score (if any).

        :button: button
        :args: current score and time
        :returns: none

        """
        if self.game_state == GameStatus.PLAYING:
            self.do_pause_game()
            self.print_debug("\nGame paused")
            self.print_debug("-----------")
        elif self.game_state == GameStatus.PAUSED:
            self.do_resume_game()
            self.print_debug("\nGame resumed")
            self.print_debug("------------")
        else:
            leaderboard = Leaderboard()
            leaderboard.show_all()

    def on_button_quit_clicked(self, button, *args):
        """Show the quit confirmation dialog.

        :button: button
        :args: TODO
        :returns: none
        """
        if self.game_state == GameStatus.PLAYING \
                or self.game_state == GameStatus.PAUSED:
            # Create surrender confirmation dialog
            dialog = Gtk.MessageDialog(parent=self)
            dialog.set_markup("<b><big>Do you want to surrender?</big></b>")
            dialog.format_secondary_text("Why so soon? Just a lil' more!")
            dialog.set_properties('buttons', Gtk.ButtonsType.NONE)
            dialog.set_properties('message-type', Gtk.MessageType.QUESTION)

            dialog.add_button("Changed my mind.", Gtk.ResponseType.CANCEL)
            dialog.add_button("NO MORE D:", Gtk.ResponseType.OK)

            response = dialog.run()

            if response == Gtk.ResponseType.OK:
                self.do_stop_game()
                self.print_debug("\nYou're weak...")
                self.print_debug("--------------")
            else:
                pass

            dialog.destroy()
        else:
            # Create quit confirmation dialog
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

    def on_mouse_pressed_drawingarea(self, widget, event):
        """Handle mouse press event: Save current mouse clicked position and
        pass the event to next handler.

        :widget: Gtk.DrawingArea
        :event: mouse event
        :return: none

        """
        if self.game_state == GameStatus.NONE:
            return True

        self.pre_x, self.pre_y = self.get_position_in_matrix(int(event.x),
                                                             int(event.y))

        return False  # Pass the event to next handler

    def on_mouse_released_drawingarea(self, widget, event):
        """Handle mouse release on drawing area

        :widget: Gtk.DrawingArea
        :event: mouse click
        :returns: none

        """
        # Block movement on certains game status
        if self.game_state != GameStatus.PLAYING:
            return True

        row, col = self.get_position_in_matrix(int(event.x), int(event.y))

        """
        Check if mouse pressed event and mouse released event is is the
        same cell. If not, ignore move.
        """
        if not (self.pre_x == row and self.pre_y == col):
            return

        flip_stack = self.is_valid_move(row, col)
        self.print_debug("")
        self.print_debug("Turn:", self.turn, "Player:", self.current_player)
        self.print_debug("Time:", self.timer)
        self.print_debug("Mouse:", row, col)
        self.print_debug("Valid movement:", flip_stack is not False)

        if flip_stack is False:
            self.print_debug("None flip trace found.")
            return True

        for i in range(len(flip_stack)):
            x, y = flip_stack[i][:]
            self.matrix[x][y] = self.current_player

        self.matrix[row][col] = self.current_player
        widget.queue_draw()

        for i in range(len(flip_stack)):
            x, y = flip_stack[i][:]
            self.matrix[x][y] = self.current_player

        if self.current_player == Player.PLAYER:
            self.player_score += (len(flip_stack) + 1)
            self.computer_score -= len(flip_stack)
        else:
            self.computer_score += (len(flip_stack) + 1)
            self.player_score -= len(flip_stack)

        self.turn += 1

        self.print_debug("Score:", "Player", self.player_score,
                         "Computer", self.computer_score)
        self.print_debug("Flip trace:", flip_stack[:])
        self.print_debug("Matrix:")
        self.print_matrix()

        self.update_turn_label()
        self.update_score_label()
        self.player_switch()
        return True

    def on_switch_hint_activated(self, switch, *args):
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

    def on_switch_show_debug_activated(self, switch, *args):
        """Show Debug

        :switch: switch
        :args: TODO
        :returns: none
        """
        if switch.get_active():
            self.debug = True
            print("\n'Debug turned on")
            print("---------------\n")
        else:
            self.debug = False
            print("\nDebug turned off")
            print("----------------\n")

    def is_valid_move(self, x, y):
        """Check if the movement in current position is a valid move

        :x: matrix row
        :y: matrix column
        :returns: True if is a valid move, false otherwise

        """
        if self.matrix[x][y] != 0:
            return False

        if not self.is_on_matrix(x, y):
            return False

        valid_moves = self.get_valid_moves(x, y)

        if valid_moves is False:
            return False

        return valid_moves

    def get_valid_moves(self, x, y):
        """Get a list of valid moves for the current position

        :x: matrix row
        :y: matrix column
        :returns: List of valid moves for current turn and its tiles to flip

        """
        tile = self.current_player

        if tile == Player.PLAYER:
            other_tile = Player.COMPUTER
        elif tile == Player.COMPUTER:
            other_tile = Player.PLAYER

        flip = []

        for x_direction, y_direction in [[-1, -1], [-1, 0], [-1, 1],
                                         [0, -1], [0, 1],
                                         [1, -1], [1, 0], [1, 1]]:
            x_start, y_start = x, y
            x_start += x_direction
            y_start += y_direction

            if self.is_on_matrix(x_start, y_start) \
                    and self.matrix[x_start][y_start] == other_tile:
                x_start += x_direction
                y_start += y_direction

                if not self.is_on_matrix(x_start, y_start):
                    continue

                while self.matrix[x_start][y_start] == other_tile:
                    x_start += x_direction
                    y_start += y_direction

                    if not self.is_on_matrix(x_start, y_start):
                        break

                if not self.is_on_matrix(x_start, y_start):
                    continue

                if self.matrix[x_start][y_start] == tile:
                    while True:
                        x_start -= x_direction
                        y_start -= y_direction

                        if x_start == x and y_start == y:
                            break

                        flip.append([x_start, y_start])

        # self.matrix[x][y] = 0

        if len(flip) == 0:
            return False

        return flip

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

    def is_on_matrix(self, x, y):
        """
        Check if current position is on matrix

        :x: matrix column
        :y: matrix row
        """
        if x < 0 or y < 0 or x > 7 or y > 7:
            return False

        return True

    def player_switch(self):
        if self.current_player == Player.PLAYER:
            self.current_player = Player.COMPUTER
        elif self.current_player == Player.COMPUTER:
            self.current_player = Player.PLAYER

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

    def print_matrix(self):
        """Print the current matrix

        :returns: none

        """
        for i in range(7):
            self.print_debug(self.matrix[i][:])

    def run_time_counter(self):
        """Run time counter

        :returns: none

        """

        self.timer_callback = GLib.timeout_add_seconds(
            1, self.__update_timer_label, None
        )

    def stop_time_counter(self):
        """Pause the current time counter (if any)

        :returns: none

        """
        if self.timer_callback is not None:
            GLib.source_remove(self.timer_callback)

    def update_score_label(self):
        """ Update the score labels

        :returns: none

        """
        self.lbl_score_player_count.set_label(repr(self.player_score))
        self.lbl_score_computer_count.set_label(repr(self.computer_score))

    def update_turn_label(self):
        """Update the turn label

        :returns: none

        """
        self.lbl_turn_count.set_label(repr(self.turn))

    def __update_timer_label(self, *user_data):
        """Update the timer label

        :returns: none

        """
        self.timer += 1
        self.lbl_time_count.set_label(GameStatus().convert_time(self.timer))

        return True

    def print_debug(self, *msg):
        if self.debug:
            print(*msg)

    timer = 0
    timer_formatted = "0s"
    turn = 0
    player_label = "Player"
    player_score = 2
    computer_label = "Computer"
    computer_score = 2
    game_state = GameStatus.NONE
    current_player = Player.NONE

    pre_x = None
    pre_y = None
    matrix = None
    debug = True

application = Application()
Gtk.main()
