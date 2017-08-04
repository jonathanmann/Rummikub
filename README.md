# Rummikub Bot Tournament

[Rummikub](https://en.wikipedia.org/wiki/Rummikub) is a tile based startegy game. The purpose of this tournament is to create a bot that will defeat all others in a 1000 game Rummikub championship. For the purposes of this competition the rules have been simplified. For further information on the rules, refer to the rules section below.

# Setup

To play, clone this repository and create a new bot by inheriting from the BaseBot class. Within your subclass, implement the "secret_strategy" method. Refer to the SampleBot subclass in the bots folder as an example. When your bot is ready it will be pitted against the other bots in the tournament. In the end, their can be only one!

# Rules

For the purposes of this tournament, the rules of this game have been simplified. The object of the game is to get rid of all your tiles. In each round, there is only one winner and the losers will not be penalized for the tiles they hold after someone wins. The rules this tournament will follow are implemented in the RulesEngine class.

#### Play order is randomly assigned.

#### Each player is dealt 14 tiles.

#### The first player to get rid of all their tiles wins.

#### Players get rid of tiles by playing groups or runs and putting them into the public space.

#### A group is a collection of three or more tiles of differing colors, but the same numerical value.

#### A run is a collection of three or more tiles of the same color and in sequential order. For example, an all red 2,3,4 would be valid, but an all red 2,3,3,4 would be invalid. Simpilarly, an all blue 4,5,6 would be valid, but an all blue 3,5,6 would be invalid.

#### A player may rearrange tiles in the public space or take tiles out of the public space into their hand as long as all collections in the public space are valid at the end of the player's turn.

#### If a player does not end up with few tiles in their hand than when they began, they must draw a tile.

These rules may change as bugs are discovered in the rules engine, but the general idea will stay the same.
