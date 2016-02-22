#!/usr/bin/env python3

import random
import datetime
import time


class GameStatus():

    def __init__(self, *args):
        pass

    NONE = 0
    PLAYING = 1
    PAUSED = 2
    STOPPED = 3


class Player():

    def __init__(self, *args):
        pass

    NONE = 0
    PLAYER = 1
    COMPUTER = 2


class Utilities():

    def __init__(self):
        pass

    def convert_time(self, s):
        return str(datetime.timedelta(seconds=s))

    def get_player(self):
        return random.randint(Player.PLAYER, Player.COMPUTER)

    def get_current_time(self, time_format="%H:%M:%S %d/%m/%Y"):
        return time.strftime(time_format)
