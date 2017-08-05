from BaseBot import BaseBot
from collections import Counter

class SampleBot(BaseBot):
    """Sample Bot"""
    def secret_strategy(self,public_space):
        """Naive play"""
        hand = self.hand
        p_tiles = hand + self.flatten(public_space)

        tiles,r_runs = self.play_strat(self.check_runs,p_tiles)
        r_tiles,r_groups = self.play_strat(self.check_groups,tiles)
        
        tiles,g_groups = self.play_strat(self.check_groups,p_tiles)
        g_tiles,g_runs = self.play_strat(self.check_runs,tiles)

        if len(r_tiles) < len(g_tiles):
            public_space = r_groups + r_runs
            self.hand = r_tiles
        else:
            public_space = g_groups + g_runs
            self.hand = g_tiles
        return public_space
        
    def play_strat(self,fn,tiles):
        tiles = tiles + []
        tx = Counter(tiles)
        possible_blocks = fn(tiles)
        blocks = self.flatten(possible_blocks)
        bks = Counter(blocks)
        tx = tx - bks
        tiles = list(tx)
        return tiles,possible_blocks


