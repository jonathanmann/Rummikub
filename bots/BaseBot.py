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
        public_space = self.secret_strategy(public_space)
        self.ending_tiles = len(self.hand)
        return public_space

    def secret_strategy(self):
        """Implement top secret strategy"""
        pass

    def check_runs(self,tiles):
        """Indentify possible runs from available tiles"""
        # This method has problems, but will fix later
        blocks = []
        runs = {}
        for tile in tiles:
            if tile.color not in runs:
                runs[tile.color] = {tile.value}
            runs[tile.color].add(tile.value)

        for r in runs:
            rn = list(runs[r])
            rn.sort()
            holder = [rn.pop()]
            while rn:
                if rn[-1] + 1 == holder[-1]:
                    holder.append(rn.pop())
                    if len(holder) > 2:
                        srun = [self.Tile(v,r) for v in holder]
                        srun.reverse()
                        if len(srun) > 3:
                            blocks.pop() # get rid of subsection
                        blocks.append(srun)
                else:
                    holder = [rn.pop()]
        return blocks

    def check_groups(self,tiles):
        """Indentify possible groups from available tiles"""
        blocks = []
        groups = {}
        for tile in tiles:
            if tile.value not in groups:
                groups[tile.value] = {tile.color}
            groups[tile.value].add(tile.color)
        for g in groups:
            if len(groups[g]) > 2:
                blocks.append([self.Tile(g,c) for c in groups[g]])
        return blocks
