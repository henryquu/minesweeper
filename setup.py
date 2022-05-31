import functools


DIFFICULTY = {
    'Easy': { 'height': 8,
              'width': 10,
              'mines': 10,
              'game_height': 420,
              'game_width': 450,
              'cell': 45},

    'Medium': { 'height': 14,
              'width': 18,
              'mines': 40,            
              'game_height': 480,
              'game_width': 540,
              'cell': 30},    
            
    'Hard': { 'height': 20,
              'width': 24,
              'mines': 99,
              'game_height': 560,
              'game_width': 600,
              'cell': 25}
}


FLAG = u"\U0001F6A9"
BOMB = u"\U0001F4A3"
CLOCK = u"\U0001F551"

Running = False

def function_running(func = None):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        global Running
        if Running == False:
            Running = True
            fun = func(*args, **kwargs)
            Running = False
            return fun
        return False
    return inner
