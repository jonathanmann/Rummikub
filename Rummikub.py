#!/usr/bin/env python
from collections import namedtuple
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
    def __init__(self,players=['1','2']):
        self.players = players
        random.shuffle(self.players)
        self.make_tiles()
        self.public_space = []

    def deal(self,tile_count=14):
        """Deal the appropriate number of tiles to each player"""
        self.player_hands = {}
        for p in self.players:
            hand = self.tiles[-tile_count:]
            self.tiles = self.tiles[:-tile_count]
            self.player_hands[p] = hand

    def draw(self,player):
        """Draw a tile if unable or unwilling to play"""
        tile = self.tiles.pop()
        self.player_hands[player].append(tile)

    def possible_groups(self,tiles):
        """Indentify possible groups from available tiles"""
        blocks = []
        groups = {}
        for tile in tiles + self.public_space:
            if tile.value not in groups:
                groups[tile.value] = {tile.color}
            groups[tile.value].add(tile.color)
        for g in groups:
            if len(groups[g]) > 2:
                blocks.append([Tile(g,c) for c in groups[g]])
        return blocks

    def possible_runs(self,tiles):
        """Indentify possible runs from available tiles"""
        # This method has problems, but will fix later
        blocks = []
        runs = {}
        #tiles = [Tile(3,'Red'),Tile(1,'Red'),Tile(4,'Red'),Tile(5,'Red'),Tile(6,'Red'),Tile(9,'Black'),Tile(10,'Black'),Tile(8,'Black')]
        for tile in tiles + self.public_space:
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
                        blocks.append(srun)
                else:
                    holder = [rn.pop()]
        return blocks

    def brute_force(self,hand):
        available = hand + self.public
        for block in combinations(available,3):
            if self.validate_block(block):
                print block

    def validate_group(self,group):
        pass

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
    print g.possible_groups(g.player_hands['1'])
    print g.possible_runs(g.player_hands['1'])
    print g.possible_groups(g.player_hands['2'])
    print g.possible_runs(g.player_hands['2'])
    #g.validate_block()
    
if __name__ == '__main__':
    main()
