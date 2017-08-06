from BaseBot import BaseBot
from collections import Counter

class SampleBot(BaseBot):
    """Sample Bot"""
    def secret_strategy(self,public_space):
        """Naive play"""
        p_tiles = self.hand + self.flatten(public_space)

        tiles,r_runs = self.play_strat(self.check_runs,p_tiles)
        r_tiles,r_groups = self.play_strat(self.check_groups,tiles)
        
        tiles,g_groups = self.play_strat(self.check_groups,p_tiles)
        g_tiles,g_runs = self.play_strat(self.check_runs,tiles)

        if len(r_tiles) < len(g_tiles):
            public_space = r_groups + r_runs
            self.hand = r_tiles
            self.strat = 'runs first'
        else:
            public_space = g_groups + g_runs
            self.hand = g_tiles
            self.strat = 'groups first'
        return public_space
        
    def play_strat(self,fn,tiles):
        tiles = tiles + []
        tx = Counter(tiles)
        possible_blocks = fn(tiles)
        blocks = self.flatten(possible_blocks)
        bks = Counter(blocks)
        tx = tx - bks
        tiles = list(tx.elements())
        return tiles,possible_blocks

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
