#!/usr/bin/env python3
try:
    import gi
    gi.require_version('Gtk', '3.0')
except ImportError:
    raise Exception('Cannot import "gi" repository')

import signal
from gi.repository import Gtk
from reversi.application import Application

# Response to keyboard interrupt signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

# Launch game
application = Application()
Gtk.main()
