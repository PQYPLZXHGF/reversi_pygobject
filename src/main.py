#!/usr/bin/env python3

import gi
import signal

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

from reversi.application import Application

# Response to keyboard interrupt signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

# Launch game
application = Application()
Gtk.main()
