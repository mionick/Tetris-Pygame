#RandomGenerator
from random import shuffle

_sequence = [1, 2, 3, 4, 5, 6, 7]
shuffle(_sequence)
_current = 0



def get_next():
    global _current, _sequence
    _current+=1
    if (_current == 7):
        _current = 0
        shuffle(_sequence)
    
    poop = _sequence[_current]
    return poop

def reseed():
    global _sequence, _current
    _current = 0
    shuffle(_sequence)

