#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, GLib
from multiprocessing import Process

from reversi.algorithm import Algorithm
from reversi.drawingarea import DrawingArea
from reversi.game import Game, GameStatus, GameMode, Player, Utilities
from reversi.panel import Panel
from reversi.leaderboard import Leaderboard


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
        self.__init_new_game()

        # Create Title bar
        header = Gtk.HeaderBar(title='Reversi 0.8',
                               subtitle="TDT University - Spring 2016",
                               show_close_button=True)
        self.set_titlebar(header)

        # Create main container
        vcontainer = Gtk.VBox(spacing=10)
        # TODO consider entry
        # self.status_entry = Gtk.Entry()
        # self.status_entry.set_editable(False)
        # self.status_entry.set_text("Press Start button to begin")
        # vcontainer.pack_end(self.status_entry, True, True, 0)

        self.add(vcontainer)

        hcontainer = Gtk.HBox(spacing=10)
        vcontainer.pack_start(hcontainer, True, True, 0)

        # Create drawing area
        self.screen = DrawingArea(self.matrix)
        self.screen.connect('button-press-event',
                            self.on_mouse_pressed_drawingarea)
        self.screen.connect('button-release-event',
                            self.on_mouse_released_drawingarea)
        hcontainer.pack_start(self.screen, True, True, 0)

        # Create right panel
        self.panel = Panel()
        hcontainer.pack_end(self.panel, False, False, 0)

        self.panel.btn_start.connect('clicked',
                                     self.on_button_start_clicked)
        self.panel.btn_hiscore.connect('clicked',
                                       self.on_button_hiscore_clicked)
        self.panel.btn_quit.connect('clicked',
                                    self.on_button_quit_clicked)

        # Display Application Window
        self.show_all()

    def __init_new_game(self):
        """Initialize new game

        :returns: none

        """
        self.game_state = GameStatus.NONE
        self.current_player = Player.NONE
        self.player_score = 2
        self.computer_score = 2

        if self.matrix is None:
            self.matrix = [[0 for col in range(8)] for row in range(8)]
        else:
            for row in range(8):
                for col in range(8):
                    self.matrix[row][col] = Player.NONE

        self.matrix[3][4] = Player.PLAYER
        self.matrix[4][3] = Player.PLAYER
        self.matrix[3][3] = Player.COMPUTER
        self.matrix[4][4] = Player.COMPUTER

    def start_game(self):
        """Start the game

        :returns: none

        """
        self.__init_new_game()
        self.screen.redraw()
        self.current_player = Utilities().get_player()
        self.game_state = GameStatus.PLAYING
        self.panel.run_time_counter()

        self.panel.btn_start.set_label("Restart")
        self.panel.btn_hiscore.set_label("Pause")
        self.panel.btn_quit.set_label("Surrender")

        self.panel.btn_start.set_sensitive(True)
        self.panel.btn_quit.set_sensitive(True)

        self.panel.set_turn(self.turn)
        self.panel.set_score(self.player_score, self.computer_score)

        self.screen.is_paused = False
        # self.screen.queue_draw()

        # Difficulity dialog
        dialog = Gtk.MessageDialog(parent=self)
        dialog.set_markup("<b><big>What do you want to try?</big></b>")
        dialog.format_secondary_text("Or I should say, how good are you?")
        dialog.set_properties('buttons', Gtk.ButtonsType.NONE)
        dialog.set_properties('message-type', Gtk.MessageType.QUESTION)

        dialog.add_button("I'm new", GameMode.EASY)
        dialog.add_button("I'm good ", GameMode.NORMAL)
        dialog.add_button("Try to beat me", GameMode.HARD)

        response = dialog.run()
        dialog.destroy()

        if response == GameMode.EASY:
            self.depth = 1

            dialog_msg = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                Gtk.ButtonsType.OK, "Take it easy")
            dialog_msg.format_secondary_text(
                "Remember, you cannot win if you move blindly."
            )
            dialog_msg.run()
            dialog_msg.destroy()

        elif response == GameMode.NORMAL:
            self.depth = 5

            dialog_msg = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                Gtk.ButtonsType.OK, "The Fotune Teller")
            dialog_msg.format_secondary_text(
                "I can see what will you do. Be prepared."
            )
            dialog_msg.run()
            dialog_msg.destroy()
        else:  # GameMode.HARD
            self.depth = 5

            dialog_msg = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                Gtk.ButtonsType.OK, "Challenge Accepted")
            dialog_msg.format_secondary_text(
                "Don't regret what you just said."
            )
            dialog_msg.run()
            dialog_msg.destroy()


        if self.current_player == Player.COMPUTER:
            self.make_move_AI()

    def pause_game(self):
        """Send the game to 'paused' status

        :returns: none

        """
        self.game_state = GameStatus.PAUSED
        self.panel.stop_time_counter()

        self.panel.btn_start.set_label("Restart")
        self.panel.btn_hiscore.set_label("Resume")
        self.panel.btn_quit.set_label("Surrender")

        self.panel.btn_start.set_sensitive(False)
        self.panel.btn_quit.set_sensitive(False)

        self.screen.is_paused = True
        self.screen.redraw()

    def resume_game(self):
        """Resume the game from 'paused' status

        :returns: none
        """
        self.game_state = GameStatus.PLAYING
        self.panel.run_time_counter()

        self.panel.btn_start.set_label("Restart")
        self.panel.btn_hiscore.set_label("Pause")
        self.panel.btn_quit.set_label("Surrender")

        self.panel.btn_start.set_sensitive(True)
        self.panel.btn_quit.set_sensitive(True)

        self.screen.is_paused = False
        self.screen.redraw()

    def stop_game(self):
        """Stop game

        :returns: none

        """
        self.game_state = GameStatus.STOPPED
        self.panel.btn_start.set_label("Start Over")
        self.panel.btn_hiscore.set_label("High Scores")
        self.panel.btn_quit.set_label("Quit")

        self.panel.btn_start.set_sensitive(True)
        self.panel.btn_quit.set_sensitive(True)

        self.screen.is_paused = False
        self.screen.redraw()

    def on_button_start_clicked(self, button):
        """Handle Start/Restart button

        :returns: True

        """
        if self.game_state == GameStatus.NONE \
                or self.game_state == GameStatus.STOPPED:
            self.start_game()
        else:
            self.pause_game()
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
                # self.stop_time_counter()
                self.start_game()
            else:
                self.resume_game()

            dialog.destroy()

        return True

    def on_button_hiscore_clicked(self, button, *args):
        """Show the leaderboard and receive new high score (if any).

        :button: button
        :args: current score and time
        :returns: none

        """
        if self.game_state == GameStatus.PLAYING:
            self.pause_game()
        elif self.game_state == GameStatus.PAUSED:
            self.resume_game()
        else:
            leaderboard = Leaderboard()
            # TODO implement leaderboard
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
            self.pause_game()
            dialog = Gtk.MessageDialog(parent=self)
            dialog.set_markup("<b><big>Do you want to Surrender?</big></b>")
            dialog.format_secondary_text("Why so soon? Just a lil' more!")
            dialog.set_properties('buttons', Gtk.ButtonsType.NONE)
            dialog.set_properties('message-type', Gtk.MessageType.QUESTION)

            dialog.add_button("Changed my mind.", Gtk.ResponseType.CANCEL)
            dialog.add_button("NO MORE D:", Gtk.ResponseType.OK)

            response = dialog.run()

            if response == Gtk.ResponseType.OK:
                self.stop_game()
            else:
                self.resume_game()

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
        # Ignore if
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
        if self.game_state != GameStatus.PLAYING \
                or self.current_player != Player.PLAYER:
            return True

        row, col = self.get_position_in_matrix(int(event.x), int(event.y))

        """
        Check if mouse pressed event and mouse released event is is the
        same cell. If not, ignore move.
        """
        if not (self.pre_x == row and self.pre_y == col):
            return True

        result = self.make_move([row, col])

        # Move not made
        if result is False:
            return True

        # Change player
        self.switch_player()

        # Destroy the event
        return True

    def on_switch_hint_activated(self, switch, *args):
        """Show hints.

        :switch: switch
        :args: none
        :returns: none

        """
        if switch.get_active():
            pass
        else:
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

    def make_move(self, position):
        """TODO: Make move at the given position to given player

        :player: current player
        :position: list of [x, y]
        :screen: screen to draw
        :returns: True if move made

        """
        # Make the actual move and get the result
        score = Game.make_move(self.current_player, position, self.matrix)

        # Redraw screen
        self.screen.redraw()

        if score is False:  # Invalid move
            return False

        # Update score label
        if self.current_player == Player.PLAYER:
            self.player_score += (score + 1)
            self.computer_score -= score
        else:
            self.computer_score += (score + 1)
            self.player_score -= score

        # Move to next turn
        self.panel.update_turn_label()
        self.panel.set_score(self.player_score, self.computer_score)

    def make_move_AI(self):
        """Makes move for AI

        :returns: none

        """
        avail_moves = Game.get_available_moves(self.current_player,
                                               self.matrix)
        pair = []

        if self.game_mode == GameMode.EASY:
            pair = Algorithm.do_shallow_scan(self.matrix, self.current_player,
                                             avail_moves)
        elif self.game_mode == GameMode.NORMAL:
            pair = Algorithm().do_minimax(self.depth - 1, self.matrix,
                                          self.current_player, avail_moves)
        else:  # GameMode.HARD
            pair = Algorithm().do_alpha_beta_pruning(
                self.depth - 1, self.matrix, self.current_player, avail_moves
            )

        self.make_move(pair[0])

        self.switch_player()

    def switch_player(self):
        """Switch current player

        :returns: none

        """
        opponent = None

        if self.current_player == Player.PLAYER:
            opponent = Player.COMPUTER
        elif self.current_player == Player.COMPUTER:
            opponent = Player.PLAYER

        # Check if there's any available moves for the opponent
        if not Game.get_available_moves(opponent, self.matrix):

            # Check if both players have no moves
            if not Game.get_available_moves(self.current_player, self.matrix):
                self.panel.stop_time_counter()
                self.stop_game()

                if self.player_score > self.computer_score:
                    dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                                               Gtk.ButtonsType.OK,
                                               "Well Done! You're good.")
                    dialog.format_secondary_text(
                        "You beat computer for " +
                        str(self.player_score - self.computer_score) +
                        " points.")
                    dialog.run()
                    dialog.destroy()
                elif self.player_score < self.computer_score:
                    dialog = Gtk.MessageDialog(
                        self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK,
                        "Luck may not always be by your side"
                    )
                    dialog.format_secondary_text(
                        "Computer got over you by " +
                        str(self.computer_score - self.player_score) +
                        " points."
                    )
                    dialog.run()
                    dialog.destroy()
                else:
                    dialog = Gtk.MessageDialog(
                        self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK,
                        "I'm actually impressed!"
                    )
                    dialog.format_secondary_text(
                        "Wanna take another try? " +
                        "You just got a draw with computer."
                    )
                    dialog.run()
                    dialog.destroy()
            else:
                if self.current_player == Player.PLAYER:
                    self.print_debug("\nAI has no moves, get the chance!\n")
                else:
                    self.print_debug("\nToo bad, you have no moves."
                                     "One extra move for AI!")

        else:
            self.current_player = opponent

            # TODO add player to leaderboard

        # If there's any valid moves for computer and the game still continues,
        # let it make the way
        if self.current_player == Player.COMPUTER \
                and self.game_state == GameStatus.PLAYING:
            self.make_move_AI()

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

    def start_pulse(self):
        self.status_entry.set_progress_pulse_step(0.2)
        self.timeout_id = GLib.timeout_add(100, self.do_pulse, None)

    def stop_pulse(self):
        GLib.source_remove(self.timeout_id)
        self.timeout_id = None
        self.status_entry.set_progress_pulse_step(0)

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
        self.lbl_time_count.set_label(Utilities().convert_time(self.timer))

        return True

    def print_debug(self, *msg):
        pass

    timer = 0
    turn = 0
    player_label = "Player"
    player_score = 2
    computer_label = "Computer"
    computer_score = 2
    game_state = GameStatus.NONE
    current_player = Player.NONE

    game_mode = None

    depth = None

    pre_x = None
    pre_y = None
    matrix = None
    debug = True
