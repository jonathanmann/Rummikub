from collections import namedtuple

class BaseBot(object):
    """
    BaseBot is the base class from which all Rummikub bots in this competition must be constructed

    Attributes:
        name (string): name assigned to bot
        hand (list): tiles in player's hand; assigned by the rules engine
        public_space (list): bot's copy of the public space consisting of blocks of tiles
    """
    def __init__(self,name=None):
        self.Tile = namedtuple('Tile','value color')
        self.name = name
        self.hand = None
        self.starting_tiles = 0
        self.ending_tiles = 0

    def play(self,public_space):
        """Play turn"""
        self.flatten = lambda x: [e for block in x for e in block]
        self.starting_tiles = len(self.hand)
        self.starting_total = len(self.flatten(public_space)) + self.starting_tiles
        public_space = self.secret_strategy(public_space)
        self.ending_tiles = len(self.hand)
        self.ending_total = len(self.flatten(public_space)) + self.ending_tiles
        
        # checksum validation
        assert self.starting_total == self.ending_total

        return public_space

    def secret_strategy(self):
        """Implement top secret strategy"""
        pass


