import sys
import os
import fileinput
import sqlite3
import readline

## Dungeon adapted from Dylan's code 

class Dungeon:
    """
    """

    dungeon_map = "dungeon.map"
    prompt = '> '

    def repl(self):
        cmd = ''

        self.db = sqlite3.connect(self.dungeon_map)
        self.c = self.db.cursor()
        self.current_room = self.getEntranceOrCreateDatabase()
        self.doLook()
        
        self.c.execute("UPDATE rooms SET visit = 1 WHERE id={}".format(self.current_room))

        while True:
            line = input(self.prompt)
            words = line.split()

            if len(words) == 0:
                pass

            elif words[0] in ('exit', 'quit', 'q'):
                break

            # destroy the dungeon and start over
            # maybe we should ask "are you sure?"
            elif words[0] in ('new'):
                self.c.execute("DROP TABLE rooms")
                self.current_room = self.getEntranceOrCreateDatabase()
                print("The previous dungeon has been destroyed (⊙_☉) ")

            elif words[0] == 'look':
                self.doLook()

            elif words[0] == 'go':
                # move to an adjacent room.
                # todo - allow someone to type the direction of an
                # adjacent room without "go"
                if len(words) < 2:
                    print("usage: go <direction>")
                    continue
                self.c.execute("SELECT to_room FROM exits WHERE from_room = {} AND dir='{}'".format(self.current_room, words[1]))
                new_room_p = self.c.fetchone()
                if (new_room_p == None):
                    print("You can't go that way!! ಥ_ಥ")
                else:
                    self.current_room = new_room_p[0]
                    self.doLook()

            elif words[0] == 'dig':
                # TODO: only allow this if the player is a super-user
                # / wielding a pickaxe or dynamite or something like that
                descs = line.split("|")
                words = descs[0].split()
                if len(words) < 3 or len(descs) != 3:
                    print("usage: dig <direction> <reverse> | <brief description of new room> | <florid description of new room>")
                    continue
                forward = words[1]
                reverse = words[2]
                brief = descs[1].strip() # strip removes whitespace around |'s
                florid = descs[2].strip()
                # now that we have the directions and descriptions,
                # add the new room, and stitch it in to the dungeon
                # via its exits
                query = 'INSERT INTO rooms (short_desc, florid_desc, visit) VALUES ("{}", "{}","{}")'.format(brief, florid,0)
                # print (query)
                self.c.execute(query)
                new_room_id = self.c.lastrowid
                # now add tunnels in both directions
                query = 'INSERT INTO exits (from_room, to_room, dir) VALUES ({}, {}, "{}")'.format(self.current_room, new_room_id, forward)
                self.c.execute(query)
                query = 'INSERT INTO exits (from_room, to_room, dir) VALUES ({}, {}, "{}")'.format(new_room_id, self.current_room, reverse)
                self.c.execute(query)

            elif words[0] == 'spawn':
                # todo: spawn a monster object
                continue

            elif words[0] == 'take':
                # todo: track the player's inventory
                # todo: create a command to place loot
                # todo: implement take
                continue

            # todo: if player ends turn in a room with a hostile mob
            # figure out how to handle combat.

            else:
                print("unknown command {}".format(words[0]))

        # all done, clean exit
        print("bye!")
        print("------------------------------------------------------------------------------------------------")
        self.db.commit()
        self.db.close()

    # describe this room and its exits
    def doLook(self):
        # todo: change the schema so we mark rooms as we visit them,
        # and show the florid description only the first time we visit
        # a room, or if someone types "look" explicitly (so will
        # probably want a force_florid optional parameter to this function)

        ## Determine if we've already visited this room or not. 
        self.c.execute("SELECT visit FROM rooms WHERE id={}".format(self.current_room))
        status = self.c.fetchone()[0]

        if status == 0:         ## we have not visited this room yet—give florid descrition
            self.c.execute("SELECT florid_desc FROM rooms WHERE id={}".format(self.current_room))
            print(self.c.fetchone()[0])
        else:                   ## we've visited this room already—give simple description
            self.c.execute("SELECT short_desc FROM rooms WHERE id={}".format(self.current_room))
            print(self.c.fetchone()[0])

        ## Present the available exits, if any 
        self.c.execute("SELECT dir FROM exits WHERE from_room={}".format(self.current_room))
        print("There are exits in these directions: ", end='')
        count = 0 
        for exit in self.c.fetchall():
            print("{}  ".format(exit[0]), end='')
            count = count + 1 
        if count == 0:
            print("none found", end='')
        print("")

    # handle startup
    def getEntranceOrCreateDatabase(self):
        # check if we've initialized the database before
        # does it have a "rooms" table
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='rooms'")
        db_exists = self.c.fetchone()
        if (db_exists == None):
            self.c.execute("DROP TABLE if exists rooms")
            self.c.execute("DROP TABLE if exists mobs")
            self.c.execute("DROP TABLE if exists loot")
            self.c.execute("DROP TABLE if exists exits")
            self.c.execute("CREATE TABLE rooms (id INTEGER PRIMARY KEY AUTOINCREMENT, short_desc TEXT, florid_desc TEXT, visit INTEGER)")
            self.c.execute("CREATE TABLE mobs (id INTEGER PRIMARY KEY AUTOINCREMENT, desc TEXT, health INTEGER, room_id INTEGER)")
            self.c.execute("CREATE TABLE exits (from_room INTEGER, to_room INTEGER, dir TEXT)")
            # todo: create table for loot items
            # todo: create table for "held_by" relationship ?? 
            self.c.execute("INSERT INTO rooms (florid_desc, short_desc,visit) VALUES ('You are standing at the entrance of what appears to be a vast, complex cave.', 'entrance',0)")
            self.db.commit()

        # now we know the db exists - fetch the first room, which is
        # the entrance
        self.c.execute("SELECT MIN(id) FROM rooms")
        entrance_p = self.c.fetchone()
        return entrance_p[0]
    

assert sys.version_info >= (3,0), "This program requires Python 3"

histfile = ".shell-history"

if __name__ == '__main__':
    try:
        readline.read_history_file(histfile)
    except FileNotFoundError:
        open(histfile, 'wb').close()
    d = Dungeon()
    print("------------------------------------------------------------------------------------------------")
    print("  _/_/_/                                                                                        ")    
    print("   _/    _/     _/    _/      _/_/_/         _/_/_/       _/_/        _/_/       _/_/_/         ")  
    print("  _/    _/     _/    _/      _/    _/     _/    _/     _/_/_/_/    _/    _/     _/    _/        ")   
    print(" _/    _/     _/    _/      _/    _/     _/    _/     _/          _/    _/     _/    _/         ")     
    print("_/_/_/         _/_/_/      _/    _/       _/_/_/       _/_/_/      _/_/       _/    _/          ")      
    print("                                         _/                                                     ") 
    print("                                       _/_/                                                     ")
    print("")

    print("Welcome to the dungeon ( ͡° ͜ʖ ͡°) Try 'look' to see room descriptions, 'go' to use an exit,")
    print("'dig' to create a new room, and 'new' to start the dungeon creation process over again.")
    d.repl()
