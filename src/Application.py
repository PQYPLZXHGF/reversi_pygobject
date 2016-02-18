#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

import Field


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
        self.set_border_width(10)
        self.resize(1000, 800)

        # Default events
        self.connect('delete-event', Gtk.main_quit)

        # Create Title bar
        self.set_title('Reversi v0.1')
        title = Gtk.HeaderBar()
        title.set_title("Reversi 0.1")
        title.set_subtitle("TDT University - Spring 2016")
        title.set_show_close_button(True)
        self.set_titlebar(title)

        # Create main container
        self.hpaned_container = Gtk.HPaned()
        self.hpaned_container.set_properties('position', 800)
        self.add(self.hpaned_container)

        # Create drawing area
        box = Gtk.Box()
        self.drawing_area = Field.DrawingArea()
        box.add(self.drawing_area)
        self.hpaned_container.pack1(box, True, False)

        # Create right panel
        self.vbox_panel = Gtk.VBox()
        self.hpaned_container.pack2(self.vbox_panel, False, True)

        # Create panel entries
        lbl_time = Gtk.Label("Time", xalign=0)
        lbl_turn = Gtk.Label("Turn", xalign=0)
        lbl_score_player = Gtk.Label(self.player_label, xalign=0)
        lbl_score_computer = Gtk.Label(self.computer_label, xalign=0)
        lbl_time_count = Gtk.Label(self.timer, xalign=1)
        lbl_turn_count = Gtk.Label(self.turn, xalign=1)
        lbl_score_player_count = Gtk.Label(self.player_score, xalign=1)
        lbl_score_computer_count = Gtk.Label(self.computer_score, xalign=1)

        # Create buttons
        self.btn_start = Gtk.Button("Start Game")
        self.btn_start.connect('clicked', self.__on_button_start_clicked)
        self.btn_hiscore = Gtk.Button("High Score")
        self.btn_hiscore.connect('clicked', self.__on_button_hiscore_clicked)
        self.btn_quit = Gtk.Button("Quit")
        self.btn_quit.connect('clicked', self.__on_button_quit_clicked)
        self.switch_help = Gtk.Switch(valign=Gtk.Align.CENTER)
        self.switch_help.connect('notify::active',
                                 self.__on_switch_hint_activated)
        self.switch_show_moves = Gtk.Switch(valign=Gtk.Align.CENTER)
        self.switch_show_moves.connect('notify::active',
                                       self.__on_switch_show_move_activated)

        # Right panel listbox
        panel_listbox = Gtk.ListBox(selection_mode=Gtk.SelectionMode.NONE)
        self.vbox_panel.add(panel_listbox)

        # Sysinfo Label
        row = Gtk.ListBoxRow()
        row.add(Gtk.Label("Information"))
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
        row.add(Gtk.Label(""))
        panel_listbox.add(row)

        # Score Row
        row = Gtk.ListBoxRow()
        row.add(Gtk.Label("Score"))
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
        row.add(Gtk.Label(""))
        panel_listbox.add(row)

        # Help row
        row = Gtk.ListBoxRow()
        row.add(Gtk.Label("Help"))
        panel_listbox.add(row)

        # Show hints row
        row = Gtk.ListBoxRow()
        hbox = Gtk.HBox(spacing=50)
        hbox.pack_start(Gtk.Label("Show Hints", xalign=0), True, True, 0)
        hbox.pack_start(self.switch_help, False, True, 0)
        row.add(hbox)
        panel_listbox.add(row)

        # Show hints row
        row = Gtk.ListBoxRow()
        hbox = Gtk.HBox(spacing=50)
        hbox.pack_start(Gtk.Label("Show Moves", xalign=0), True, True, 0)
        hbox.pack_start(self.switch_show_moves, False, True, 0)
        row.add(hbox)
        panel_listbox.add(row)

        # Blank row
        row = Gtk.ListBoxRow()
        row.add(Gtk.Label(""))
        panel_listbox.add(row)

        # Add buttons
        self.vbox_panel.pack_end(self.btn_quit, False, True, 0)
        self.vbox_panel.pack_end(self.btn_hiscore, False, True, 0)
        self.vbox_panel.pack_end(self.btn_start, False, True, 0)

        # Display Application Window
        self.show_all()

    def __on_button_start_clicked(self, button):
        """
        TODO start game and change the label to "restart"
        """
        button.set_label('Restart')
        self.btn_hiscore.set_label('Pause')
        pass

    def __on_button_hiscore_clicked(self, button):
        pass

    def __on_button_quit_clicked(self, button):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION,
                                   Gtk.ButtonsType.NONE,
                                   "Do you want to quit?")
        dialog.add_button("Not now", Gtk.ResponseType.CANCEL)
        dialog.add_button("I said quit!", Gtk.ResponseType.OK)
        dialog.format_secondary_text("We will wait for you!")
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            Gtk.main_quit(self)
        else:
            pass

        dialog.destroy()

    def __on_button_restart_clicked(self, button):
        pass

    def __on_switch_hint_activated(self, switch, gparam):
        if switch.get_active():
            state = "on"
        else:
            state = "off"

        print("Switch \"Show hint\" was turned", state)

    def __on_switch_show_move_activated(self, switch, gparam):
        if switch.get_active():
            state = "on"
        else:
            state = "off"

        print("Switch \"Show moves\" was turned", state)

    timer = 0.00
    turn = 0
    player_label = "Player"
    player_score = 0
    computer_label = "Computer"
    computer_score = 0

application = Application()
Gtk.main()
