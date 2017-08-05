#!/usr/bin/env python
from collections import namedtuple
import random

from bots.SampleBot import SampleBot

Tile = namedtuple('Tile','value color')

class RulesEngine:
    """
    Implementation of a Rummikub rules engine for testing strategy bots

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

    def play(self,player):
        """Test bot strategy"""
        s = SampleBot()
        s.hand = self.player_hands[player]
        self.public_space = s.play(self.public_space)
        self.player_hands[player] = s.hand

        if s.ending_tiles >= s.starting_tiles:
            print("Player",player,'draws a tile...')
            self.draw(player)
        else:
            print("Player:",player,"starting_hand:",s.starting_tiles,"ending_hand",s.ending_tiles)

        if s.ending_tiles == 0:
            self.winner = player
            print("Player",player,'wins')
        

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
    g = RulesEngine()
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
