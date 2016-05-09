import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, GLib
from reversi.game import Utilities


class Panel(Gtk.VBox):

    """
    Game right panel

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size_request(200, 200)

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

        lbl_show_hints = Gtk.Label(halign=Gtk.Align.START)
        lbl_show_hints.set_label('Show Hints')

        self.lbl_time_count = Gtk.Label(halign=Gtk.Align.END)
        self.lbl_time_count.set_label(Utilities().convert_time(self.timer))

        self.lbl_turn_count = Gtk.Label(halign=Gtk.Align.END)
        self.lbl_turn_count.set_label(repr(self.turn))

        self.lbl_score_player_count = Gtk.Label(halign=Gtk.Align.END)
        # self.lbl_score_player_count.set_label(repr(self.player_score))

        self.lbl_score_computer_count = Gtk.Label(halign=Gtk.Align.END)
        # self.lbl_score_computer_count.set_label(repr(self.computer_score))

        # Create buttons
        self.btn_start = Gtk.Button()
        self.btn_start.set_label("Start Game")
        self.btn_start.set_size_request(-1, 50)

        self.btn_hiscore = Gtk.Button()
        self.btn_hiscore.set_label("High Scores")
        self.btn_hiscore.set_size_request(-1, 50)

        self.btn_quit = Gtk.Button()
        self.btn_quit.set_size_request(-1, 50)
        self.btn_quit.set_label("Quit")

        self.switch_hint = Gtk.Switch(valign=Gtk.Align.END)

        panel_listbox = Gtk.ListBox(selection_mode=Gtk.SelectionMode.NONE)

        # System info Label
        row = Gtk.ListBoxRow()
        row.add(lbl_information)
        panel_listbox.add(row)

        # Timer row
        """
        row = Gtk.ListBoxRow()
        hbox = Gtk.HBox(spacing=50)
        hbox.pack_start(lbl_time, True, True, 0)
        hbox.pack_start(self.lbl_time_count, True, True, 0)
        row.add(hbox)
        panel_listbox.add(row)
        """

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

        """
        # Setting row
        row = Gtk.ListBoxRow()
        row.add(lbl_setting)
        panel_listbox.add(row)

        # Show hints row
        row = Gtk.ListBoxRow()
        hbox = Gtk.HBox(spacing=50)
        hbox.pack_start(lbl_show_hints, True, True, 0)
        hbox.pack_start(self.switch_hint, False, True, 0)
        row.add(hbox)
        panel_listbox.add(row)
        """

        self.pack_start(panel_listbox, True, True, 0)
        self.pack_end(self.btn_quit, False, True, 0)
        """self.pack_end(self.btn_hiscore, False, True, 0)"""
        self.pack_end(self.btn_start, False, True, 0)

    def set_score(self, player_score, computer_score):
        """Set score label for invidual player. Will update score labels.

        :player_score: Score of player
        :computer_score: Score of computer
        :returns: none

        """
        self.lbl_score_player_count.set_label(repr(player_score))
        self.lbl_score_computer_count.set_label(repr(computer_score))

    def run_time_counter(self):
        """Start or resume the time counter

        :returns: None

        """
        self.timer_callback = GLib.timeout_add_seconds(
            1, self.__update_timer_label, None
        )

    def stop_time_counter(self):
        """Stop or pause the time counter

        :returns: None

        """
        # TODO fix timer
        """
        if self.timer_callback is not None:
            GLib.source_remove(self.timer_callback)
            self.timer_callback = None
        """
        pass

    def set_time_label(self, time):
        """Set the time label's value.

        :time: counts in sec
        :returns: None

        """
        self.lbl_time_count.set_label(Utilities.convert_time(self.timer))

    def set_turn(self, turn):
        """Set the current turn. Will update the turn label as well.

        :turn: Current turn.
        :returns: None

        """
        self.turn = turn
        self.lbl_turn_count.set_label(repr(self.turn))

    def __update_timer_label(self, *args):
        """Update time label by 1 second

        :returns: True

        """
        self.timer += 1
        self.lbl_time_count.set_label(Utilities().convert_time(self.timer))

        return True

    def update_turn_label(self):
        """Update the turn label by 1
        :returns: None

        """
        self.turn += 1
        self.lbl_turn_count.set_label(repr(self.turn))

    timer = 0
    turn = 0
    player_label = "Player"
    computer_label = "Computer"

    timer_callback = None

if __name__ == "__main__":
    import signal

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    window = Gtk.Window()
    window.add(Panel())
    window.connect('delete-event', Gtk.main_quit)
    window.show_all()
    Gtk.main()
