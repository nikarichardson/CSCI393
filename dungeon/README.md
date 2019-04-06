SQLite Dungeon
==============

Note: this was created for my Spring 2019 Intro to Operating systems
class at Reed College, but of course anyone can check it out and play
around with it.

This is a minimal skeleton of a possibly-multi-player dungeon crawler
/ builder.  It's written in Python, and uses SQLite3 as its back-end.
It *should* enable multi-user dungeons, but that hasn't been
demonstrated yet.  It is intended as a starting point for learning
more about databases, database schemas, transactions and the
model/view/controller architecture of interactive application design.

Various points in the code are marked with TODOs as obvious areas of enhancement.
However, this is a practically bare skeleton - it can be taken in many different directions.

Using it
--------

Here is an example session:

```
$ python3 Dungeon.py
Welcome to the dungeon. Try 'look' 'go' and 'dig'
You are standing at the entrance of what appears to be a vast, complex cave.
There are exits in these directions:
> dig e w | Chandelier room | You are in a considerably large room, inexplicably illuminated by a rough-hewn chandelier that is encrusted with glowing jewels.
> look
You are standing at the entrance of what appears to be a vast, complex cave.
There are exits in these directions: e
> go e
You are in a considerably large room, inexplicably illuminated by a rough-hewn chandelier that is encrusted with glowing jewels.
There are exits in these directions: w
> go w
You are standing at the entrance of what appears to be a vast, complex cave.
There are exits in these directions: e
> q
bye!
```

The schema
----------

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

These exits are uni-directional - so to connect two rooms via exits
requires two entries in the database. For example, if room2 is east of
room1, there would be a from_room = 1, to_room = 2, dir = "east" link,
and most often, that would correspond to another entry in the table
with from_room = 2, to_room = 1, dir = "west". When a user digs a
tunnel between rooms, they supply labels for both directions, forward
and back.

Things to do
------------

The source code has many TODO's embedded in the comments, but at a high level:

 * implement MOBs (monster objects). They could be static, or they
   could have a life of their own. Create stats (besides just health),
   and things they do. Maybe friendly, maybe hostile - have fun!

 * implement inventory and loot. This will require at least one more
   table, to denote the loot-item, and that table could have a relation of where it is (holder/container/room), or it could be in a separate table.

 * limit the super-power of digging. Maybe have one designated pick
   axe, and only the wielder can dig new tunnels? How to manage this
   is an interesting design question.

 * support local multi-player - figure out how to allow multiple
   SQLite connections to the one database. it works with one user
   connecting more than once, but in our experiments in class, another
   user isn't able to connect. Maybe it's about permissions on the
   lock-file / journal? Probably will want players to be in the MOBs table, to enable interaction.
   Will want to notify users what other players do while they're in the same room.
   "Say" is an obvious command, which will enable chatting.

 * your idea here - have fun!
