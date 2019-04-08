SQLite Dungeon
==============
<img src="https://66.media.tumblr.com/d471e4f3dee7aca7d07468ae89225edb/tumblr_ppnk1hKli51tk06jno1_540.jpg" align="right"> 
Adapted from <a href="https://github.com/dylanmc/SQLiteDungeon">Dylan's Dungeon</a> code from Spring 2019 Operating systems. 
Written in Python with SQLite3 as back-end. Image on right from RPG Maker VX with my character sprite in a designed dungeon map. This dungeon has rooms and exits. You can <i>spawn</i> a monster, <i>place</i>  loot, <i>take</i>  loot, and engage in combat with the monsters inside the dungeon. Users with a pick-axe in their inventory can <i>dig</i>  rooms. 

**Monster:**
minotaur, orc, plant, rat, ogre, scorpion, skeleton, slime, snake, succubus, werewolf, zombie, skeleton, vampire, chimera, cerberus, spider, ghost, fairy, dragon
 
**Loot:**
plain-chest,golden-chest,steel-chest,mini-chest,mana-crystal,pick-axe,potion,book,tome,ring 

**Weapons**
sword,pick-axe,bow 

The currently populated tables are `rooms` and `exits`. The schema for these tables are:

`CREATE TABLE rooms (id INTEGER PRIMARY KEY AUTOINCREMENT, short_desc TEXT, florid_desc TEXT)`

Each room has a primary key,

  * a *florid description*, which is the description you first see when entering a room (or when you use the `look` command)
  * a *brief description* which is the description you see on subsequent visits to a room

`CREATE TABLE exits (from_room INTEGER, to_room INTEGER, dir TEXT)`

Rooms are connected to each other by exits. An exit from a room has a
direction, which can be any single word, but should be something that
sounds like a direction (e.g., north, south, up, down, northeast,
etc.).

The exits are uni-directional - so to connect two rooms via exits
requires two entries in the database. For example, if room2 is east of
room1, there would be a from_room = 1, to_room = 2, dir = "east" link,
and most often, that would correspond to another entry in the table
with from_room = 2, to_room = 1, dir = "west". When a user digs a
tunnel between rooms, they supply labels for both directions, forward
and back.

--------

Here is an example session:

```
------------------------------------------------------------------------------------------------
  _/_/_/                                                                                        
   _/    _/     _/    _/      _/_/_/         _/_/_/       _/_/        _/_/       _/_/_/         
  _/    _/     _/    _/      _/    _/     _/    _/     _/_/_/_/    _/    _/     _/    _/        
 _/    _/     _/    _/      _/    _/     _/    _/     _/          _/    _/     _/    _/         
_/_/_/         _/_/_/      _/    _/       _/_/_/       _/_/_/      _/_/       _/    _/          
                                         _/                                                     
                                       _/_/                                                     
                                       
Welcome to the dungeon ( ͡° ͜ʖ ͡°) Try 'look' to see room descriptions, 'go' to use an exit,
'dig' to create a new room, and 'new' to start the dungeon creation process over again.
Use 'check' to survey your inventory, 'take' to steal loot, and 'place' to leave loot behind.
entrance
No items in this room.
There are exits in these directions: e
> e
chandelier room
No items in this room.
There's a fairy in this room! (ง •̀_•́)ง 
There are exits in these directions: w
> w
entrance
No items in this room.
There are exits in these directions: e
> q
bye!
```
