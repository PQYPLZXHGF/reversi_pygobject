import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, GLib
from reversi.game import Utilities


class Panel(Gtk.VBox):

    """Game right panel"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size_request(200, 200)

        self.turn = 0
        self.player_label = "Player"
        self.computer_label = "Computer"

        lbl_information = Gtk.Label()
        lbl_information.set_markup("<b>Information</b>")

        lbl_score = Gtk.Label()
        lbl_score.set_markup("<b>Score</b>")

        lbl_time = Gtk.Label(halign=Gtk.Align.START)
        lbl_time.set_label("Time")

        lbl_turn = Gtk.Label(halign=Gtk.Align.START)
        lbl_turn.set_label("Turn")

        lbl_score_player = Gtk.Label(halign=Gtk.Align.START)
        lbl_score_player.set_label(self.player_label)

        lbl_score_computer = Gtk.Label(halign=Gtk.Align.START)
        lbl_score_computer.set_label(self.computer_label)

        lbl_show_hints = Gtk.Label(halign=Gtk.Align.START)
        lbl_show_hints.set_label('Show Hints')

        self.lbl_turn_count = Gtk.Label(halign=Gtk.Align.END)
        self.lbl_turn_count.set_label(repr(self.turn))

        self.lbl_score_player_count = Gtk.Label(halign=Gtk.Align.END)

        self.lbl_score_computer_count = Gtk.Label(halign=Gtk.Align.END)

        # Create buttons
        self.btn_start = Gtk.Button()
        self.btn_start.set_label("Start Game")
        self.btn_start.set_size_request(-1, 50)

        self.btn_quit = Gtk.Button()
        self.btn_quit.set_size_request(-1, 50)
        self.btn_quit.set_label("Quit")

        self.switch_hint = Gtk.Switch(valign=Gtk.Align.END)

        panel_listbox = Gtk.ListBox(selection_mode=Gtk.SelectionMode.NONE)

        # System info Label
        row = Gtk.ListBoxRow()
        row.add(lbl_information)
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

        self.pack_start(panel_listbox, True, True, 0)
        self.pack_end(self.btn_quit, False, True, 0)
        self.pack_end(self.btn_start, False, True, 0)

    def set_score(self, player_score, computer_score):
        """Set score label for invidual player. Will update score labels"""
        self.lbl_score_player_count.set_label(repr(player_score))
        self.lbl_score_computer_count.set_label(repr(computer_score))

    def set_turn(self, turn):
        """Set the current turn. Will update the turn label as well.

        :turn: Current turn.
        :returns: None

        """
        self.turn = turn
        self.lbl_turn_count.set_label(repr(self.turn))

    def update_turn_label(self):
        """Update the turn label by 1
        :returns: None

        """
        self.turn += 1
        self.lbl_turn_count.set_label(repr(self.turn))
