#!/usr/bin/env python
from collections import namedtuple
import random

from bots.SampleBot import SampleBot


Tile = namedtuple('Tile','value color')
bots = [SampleBot('1'),SampleBot('2'),SampleBot('3'),SampleBot('4')]

class RulesEngine:
    """
    Implementation of a Rummikub rules engine for testing strategy bots

    Attributes:
        colors (set): possible colors for a tile
        values (set): possible numbers for a tile
        instances (int): number of tile instances
        tiles (list): available tiles
        bots (list): bots playing in the tournament
    """
    def __init__(self,bots):
        self.bots = bots
        random.shuffle(self.bots)
        self.make_tiles()
        self.public_space = []
        self.winner = None

    def deal(self,tile_count=14):
        """Deal the appropriate number of tiles to each bot"""
        for b in self.bots:
            hand = self.tiles[-tile_count:]
            self.tiles = self.tiles[:-tile_count]
            b.hand = hand

    def draw(self,bot):
        """Draw a tile if unable or unwilling to play"""
        try:
            tile = self.tiles.pop()
            bot.hand.append(tile)
        except:
            print("No more tiles")

    def play(self,bot):
        """Test bot strategy"""
        self.public_space = bot.play(self.public_space)

        if bot.ending_tiles >= bot.starting_tiles:
            print("Player",bot.name,'draws a tile...')
            self.draw(bot)
        else:
            print("Player:",bot.name,"starting_hand:",bot.starting_tiles,"ending_hand",bot.ending_tiles)

        if bot.ending_tiles == 0:
            self.winner = bot.name
            print("Player",bot.name,'wins')
        

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
    g = RulesEngine(bots)
    g.deal()
    
    while g.winner is None and g.tiles:
        for b in g.bots:
            g.play(b)
            if g.winner:
                break
            if len(g.tiles) == 0:
                print('Out of tiles!')
                break
    
if __name__ == '__main__':
    main()
