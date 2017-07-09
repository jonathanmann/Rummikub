#!/usr/bin/env python
from collections import namedtuple
import random

Tile = namedtuple('Tile','value color instance')
Block = namedtuple('Block','type tiles')

class Rummikub:
    """
    Implementation of Rummikub for testing strategy bots

    Attributes:
        colors (set): colors for a tile
        values (set) numbers for a tile
        instances (int): number of tile instances
        tiles (set): valid tiles
        pool (set): available tiles
        player_hands (dict): tile sets in each player's possession
    """
    def __init__(self,players=['1','2']):
        self.players = players
        self.make_tiles()
        self.pool = self.tiles.copy()
        self.public_space = []

    def deal(self,tile_count=14):
        """Deal the appropriate number of tiles to each player"""
        self.player_hands = {}
        for p in self.players:
            hand = set(random.sample(self.pool,tile_count))
            self.pool = self.pool.difference(hand)
            self.player_hands[p] = hand

    def draw(self,player):
        """Draw a tile if unable or unwilling to play"""
        tile = random.sample(self.pool,1)[0]
        self.player_hands[player].add(tile)
        self.pool.remove(tile)

    def validate_block(self,block):
        """Validate block of tiles as straight flush or as same value color combination"""
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
        for i in range(self.instances):
            for v in self.values:
                for c in self.colors:
                    tiles.append(Tile(v,c,i + 1))
            tiles.append(Tile(0,'Wild',i + 1))
        self.tiles = set(tiles)

def main():
    t = False
    while not t:
        g = Rummikub()
        g.deal()
        #p = random.sample(g.player_hands['1'],3)
        block = Block('straight',random.sample(g.player_hands['1'],3))
        t = g.validate_block(block[1])
    print block
    
if __name__ == '__main__':
    main()
