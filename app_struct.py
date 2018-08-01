import threading
from functools import wraps
from enum import Enum

class GameState(Enum):
    GAME_MENU = 0
    GAME_PLAY = 1
    GAME_END = 2
    GAME_EXIT = 3

def delay(delay=0.):
    def wrap(f):
        @wraps(f)
        def delayed(*args, **kwargs):
            timer = threading.Timer(delay, f, args=args, kwargs=kwargs)
            timer.start()
        return delayed
    return wrap
