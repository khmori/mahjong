from hand import *
from settings import *

class Player:
    def __init__(self, name, cpu=False, hidden_tiles=True):
        self.name = name
        self.hand = []
        self.cpu = cpu 
        self.drawn_tile = None
        self.ron_tile = None
        self.hidden_tiles = hidden_tiles
        self.discarded = False
        self.called = False
        self.meld = []