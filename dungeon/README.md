SQLite Dungeon
==============

Adapted from Dylan's Dungeon code from Spring 2019 Operating systems. 
Written in Python with SQLite3 as back-end. Image from RPG Maker VX with my character sprite in a designed dungeon map (ง •̀_•́)ง
<img src="https://66.media.tumblr.com/d471e4f3dee7aca7d07468ae89225edb/tumblr_ppnk1hKli51tk06jno1_540.jpg" align="right"> 

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


Things to do
------------

