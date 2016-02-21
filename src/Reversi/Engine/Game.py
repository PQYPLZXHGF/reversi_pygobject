#!/usr/bin/env python3

import random
import datetime


class GameStatus():

    def __init__(self, *args):
        pass

    def convert_time(self, s):
        return str(datetime.timedelta(seconds=s))

    NONE = 0
    PLAYING = 1
    PAUSED = 2
    STOPPED = 3


class Player():

    def __init__(self, *args):
        pass

    def get_player(self):
        return random.randint(self.PLAYER, self.COMPUTER)

    NONE = 0
    PLAYER = 1
    COMPUTER = 2
