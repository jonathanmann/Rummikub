#!/usr/bin/env python
from collections import namedtuple
import random

Tile = namedtuple('Tile','value color instance')

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
        pass

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
    g = Rummikub()
    g.deal()
    print g.player_hands['1']
    print len(g.pool)
    print len(g.tiles)
    
if __name__ == '__main__':
    main()
