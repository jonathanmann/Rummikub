#!/usr/bin/env python
from collections import namedtuple
from collections import Counter
import random
from itertools import combinations

Tile = namedtuple('Tile','value color')

class Rummikub:
    """
    Implementation of Rummikub for testing strategy bots

    Attributes:
        colors (set): possible colors for a tile
        values (set): possible numbers for a tile
        instances (int): number of tile instances
        tiles (list): available tiles
        player_hands (dict): tile sets in each player's possession
    """
    def __init__(self,players=['1','2','3','4']):
        self.players = players
        random.shuffle(self.players)
        self.flatten = lambda x: [e for block in x for e in block]
        self.make_tiles()
        self.public_space = []
        self.winner = None

    def deal(self,tile_count=14):
        """Deal the appropriate number of tiles to each player"""
        self.player_hands = {}
        for p in self.players:
            hand = self.tiles[-tile_count:]
            self.tiles = self.tiles[:-tile_count]
            self.player_hands[p] = hand

    def draw(self,player):
        """Draw a tile if unable or unwilling to play"""
        try:
            tile = self.tiles.pop()
            self.player_hands[player].append(tile)
        except:
            print("No more tiles")

    def play_strat(self,fn,tiles):
        tiles = tiles + []
        tx = Counter(tiles)
        possible_blocks = fn(tiles)
        blocks = self.flatten(possible_blocks)
        bks = Counter(blocks)
        tx = tx - bks
        tiles = list(tx)
        return tiles,possible_blocks

    def play(self,player):
        """Naive play"""
        hand = self.player_hands[player]
        starting_tiles = len(hand)
        public_holder = []
        p_tiles = hand + self.flatten(self.public_space)

        tiles,r_runs = self.play_strat(self.check_runs,p_tiles)
        r_tiles,r_groups = self.play_strat(self.check_groups,tiles)
        
        tiles,g_groups = self.play_strat(self.check_groups,p_tiles)
        g_tiles,g_runs = self.play_strat(self.check_runs,tiles)

        if len(r_tiles) < len(g_tiles):
            self.public_space = r_groups + r_runs
            self.player_hands[player] = r_tiles
        else:
            self.public_space = g_groups + g_runs
            self.player_hands[player] = g_tiles

        ending_tiles = len(self.player_hands[player])

        if ending_tiles >= starting_tiles:
            print("Player",player,'draws a tile...')
            self.draw(player)
        else:
            print("Player:",player,"starting_hand:",starting_tiles,"ending_hand",ending_tiles)

        if ending_tiles == 0:
            self.winner = player
            print("Player",player,'wins')
        


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
                blocks.append([Tile(g,c) for c in groups[g]])
        return blocks

    def check_runs(self,tiles):
        """Indentify possible runs from available tiles"""
        # This method has problems, but will fix later
        blocks = []
        runs = {}
        #tiles = [Tile(3,'Red'),Tile(1,'Red'),Tile(4,'Red'),Tile(5,'Red'),Tile(6,'Red'),Tile(9,'Black'),Tile(10,'Black'),Tile(8,'Black')]
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
                        srun = [Tile(v,r) for v in holder]
                        srun.reverse()
                        if len(srun) > 3:
                            blocks.pop() # get rid of subsection
                        blocks.append(srun)
                else:
                    holder = [rn.pop()]
        return blocks


    def validate_block(self,block):
        """Validate block of tiles as a run(straight flush) or group(same value color combination)"""
        if len(block) < 3:
            return False
        vals = []
        colors = []
        for tile in block:
            colors.append(tile.color)
            vals.append(tile.value)
        if len(set(colors)) > 1:
            return len(set(vals)) == 1 and len(vals) == len(set(colors))
        vals.sort()
        for i in range(len(vals) - 1):
            if vals[i] + 1 <> vals[i + 1]:
                return False
        return True

    def greedy_play(self,player):
        for block in self.public_space:
            print block

    def validate_state(self,state):
        """Validate game state by checking all public blocks"""
        pass

    def make_tiles(self):
        """Create the tiles to be used in the game"""
        self.colors = {'Red','Yellow','Blue','Black'}
        self.values = {x + 1 for x in range(13)}
        self.instances = 2 
        tiles = []
        for v in self.values:
            for c in self.colors:
                tiles.append(Tile(v,c))
        tiles.append(Tile(0,'Wild'))
        self.tiles = self.instances * tiles
        random.shuffle(self.tiles)

def main():
    g = Rummikub()
    g.deal()
    
    while g.winner is None and g.tiles:
        for player in g.players:
            g.play(player)
            if g.winner:
                break
            if len(g.tiles) == 0:
                print('Out of tiles!')
                break
    
if __name__ == '__main__':
    main()
