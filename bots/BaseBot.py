class BaseBot(object):
    """
    BaseBot is the base class from which all Rummikub bots in this competition must be constructed

    Attributes:
        name (string): name assigned to bot
        hand (list): tiles in player's hand; assigned by the rules engine
        public_space (list): bot's copy of the public space consisting of blocks of tiles
    """
    def __init__(self,name):
        self.name = name
        self.hand = None

    def play(self,public_space):
        """Play turn"""
        self.flatten = lambda x: [e for block in x for e in block] 
        self.hand += self.flatten(public_space)
        self.public_space = []
        self.secret_strategy()
        return self.public_space

    def secret_strategy():
        """Implement top secret strategy"""
        pass
