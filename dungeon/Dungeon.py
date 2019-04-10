import sys
import os
import fileinput
import sqlite3
import readline

## Dungeon project built off Dylan's code. 

class Dungeon:
    """
    """

    dungeon_map = "dungeon.map"
    prompt = '> '
   
    ## MONSTERS :  minotaur, orc, plant, rat, ogre, scorpion, skeleton, slime, snake
    ## succubus, werewolf, zombie, skeleton, vampire,
    ## chimera, cerberus, spider, ghost, fairy, dragon,

    ## LOOT : plain-chest, golden-chest, steel-chest, mini-chest
    ## mana-crystal, pick-axe, potion, book, tome, ring, herb, shield

    ## WEAPONS : sword, pick-axe,bow,dagger,spear,claw,crossbow

    ## CLASSES : hero, warrior, mage, priest

    ## SKILLS : attack, guard, double-attack,triple-attack,heal

    ## STATES : knockout, rage, confusion, sleep, immortal, blind, rage, normal 


    def repl(self):
        cmd = ''

        self.db = sqlite3.connect(self.dungeon_map)
        self.c = self.db.cursor()
        self.current_room = self.getEntranceOrCreateDatabase()


        self.doLook(0)
        
        self.c.execute("UPDATE rooms SET visit = 1 WHERE id={}".format(self.current_room))

        while True:
            line = input(self.prompt)
            words = line.split()

            if len(words) == 0:
                pass

            elif words[0] in ('exit', 'quit', 'q'):
                print("bye!")
                break

            # destroy the dungeon and start over
            elif words[0] == 'new':
                print("Type 1 to go forward with this operation, unless you've recognized the importance of preserving cultural artifacts like dungeons!") 
                answer = int(input("Are you sure? "))
                if answer == 1: 
                    self.c.execute("DROP TABLE rooms")
                    self.c.execute("DROP TABLE mobs")
                    self.c.execute("DROP TABLE Inventory")
                    self.c.execute("DROP TABLE loot")
                    self.c.execute("DROP TABLE exits")
                    self.c.execute("DROP TABLE stats")  
                    self.current_room = self.getEntranceOrCreateDatabase()
                    print("The previous dungeon has been destroyed (⊙_⊙) ")
                    break
                else:
                    print("You've made a noble decision, warrior.")

            elif words[0] == 'look':
                self.doLook(1)

            elif words[0] == 'go':
                # move to an adjacent room.
                if len(words) < 2:
                    print("usage: go <direction>")
                    continue
                self.c.execute("SELECT to_room FROM exits WHERE from_room = {} AND dir='{}'".format(self.current_room, words[1]))
                new_room_p = self.c.fetchone()
                if (new_room_p == None):
                    print("You can't go that way!! ಥ_ಥ")
                else:
                    self.current_room = new_room_p[0]
                    self.doLook(0)

            elif words[0] == 'e' or words[0] == 'w' or words[0] == 'n' or words[0] == 's': 
                # move to an adjacent room.
                # we allow someone to type the direction of an
                # adjacent room without "go"
                self.c.execute("SELECT to_room FROM exits WHERE from_room = {} AND dir='{}'".format(self.current_room, words[0]))
                new_room_p = self.c.fetchone()
                if (new_room_p == None):
                    print("You can't go that way!! ಥ_ಥ")
                else:
                    self.current_room = new_room_p[0]
                    self.doLook(0)

            elif words[0] == 'use':
                ## to do : implement use item
                continue 

            elif words[0] == 'dig':
                # only users with a shovel in their inventory can dig rooms
                yes_shovel = False
 
                # check inventory for a shovel 
                self.c.execute("SELECT name FROM inventory") 

                for item in self.c.fetchall():
                    if item[0] == 'shovel': 
                        yes_shovel = True 

                if yes_shovel == True: 
                    descs = line.split("|")
                    words = descs[0].split()
                    if len(words) < 3 or len(descs) != 4:
                        print("usage: dig <direction> <reverse> | <brief description of new room> | <florid description of new room> | <loot item>")
                        continue
                    forward = words[1]
                    reverse = words[2]
                    brief = descs[1].strip() # strip removes whitespace around |'s
                    florid = descs[2].strip()
                    loot = descs[3].strip()
                    # now that we have the directions and descriptions,
                    # add the new room, and stitch it in to the dungeon
                    # via its exits
                    query = 'INSERT INTO rooms (short_desc, florid_desc,visit,loot) VALUES ("{}", "{}","{}","{}")'.format(brief,florid,0,loot)
                    # print (query)
                    self.c.execute(query)
                    new_room_id = self.c.lastrowid
                    # now add tunnels in both directions
                    query = 'INSERT INTO exits (from_room, to_room, dir) VALUES ({}, {}, "{}")'.format(self.current_room, new_room_id, forward)
                    self.c.execute(query)
                    query = 'INSERT INTO exits (from_room, to_room, dir) VALUES ({}, {}, "{}")'.format(new_room_id, self.current_room, reverse)
                    self.c.execute(query)

                else:
                    print("Sorry, only users with a shovel in their inventory can dig rooms.")


            elif words[0] == 'spawn':
                # spawn a monster object
                print("You can spawn the following monster objects: minotaur, orc, plant, rat, ogre, scorpion, skeleton, slime, snake, succubus, werewolf, zombie, skeleton, vampire, chimera, cerberus, spider, ghost, fairy, dragon.")
                my_monster = str(input("Type the name of a monster object: "))

                ## to do: connect to second monster type database that holds all the descriptions and stats of each type of monster 

                ## now we need to update the table of monster objects and 'place' the monster in the room 
                query = 'INSERT INTO mobs (name,health,atp_power,def_power,exp,room_id) VALUES ("{}",500,100,100,100,"{}")'.format(my_monster,self.current_room)
                self.c.execute(query)
            
                # Debugging stuff here ...
                self.c.execute("SELECT name FROM mobs WHERE room_id={}".format(self.current_room))
                monster = self.c.fetchone()[0] 
                print("You've spawned a {}.".format(monster))
             

            elif words[0] == 'take':
                # we only allow one object per room 
                # get the name of the loot available in this room 
                self.c.execute("SELECT loot FROM rooms WHERE id={}".format(self.current_room))
                item = self.c.fetchone()[0] 

                print("Are you sure you want to take {}?".format(str(item)))  
                answer = int(input("Press 1 to confirm: "))
        
                if answer == 1:
                    # insert item into inventory 
                    query = 'INSERT INTO inventory (name) VALUES ("{}")'.format(item)
                    self.c.execute(query) 

                    print("You took {}!".format(item))
                    # remove loot from the room (update table)
                    self.c.execute("UPDATE rooms SET loot = 'none' WHERE id={}".format(self.current_room))
                continue 

                
            elif words[0] == 'view':
                # view player stats 
                print("STATS")

                ## HEALTH 
                self.c.execute("SELECT health from stats")
                print("     Health : ",end='')
                print("{}".format(self.c.fetchone()[0]))

                ## STATE 
                self.c.execute("SELECT state from stats")
                print("     State : ",end='')
                print("{}".format(self.c.fetchone()[0]))

                ## WEAPON
                self.c.execute("SELECT weapon from stats")
                print("     Weapon : ",end='')
                print("{}".format(self.c.fetchone()[0]))

                ## ARMOR
                self.c.execute("SELECT armor from stats")
                print("     Armor : ",end='')
                print("{}".format(self.c.fetchone()[0]))

                ## CLASS
                self.c.execute("SELECT class from stats")
                print("     Class : ",end='')
                print("{}".format(self.c.fetchone()[0]))

                ## ATP_POWER
                self.c.execute("SELECT atp_power from stats")
                print("     Attack_power : ",end='')
                print("{}".format(self.c.fetchone()[0]))


                ## DEF_POWER
                self.c.execute("SELECT def_power from stats")
                print("     Defense_power : ",end='')
                print("{}".format(self.c.fetchone()[0]))

                ## EXP 
                self.c.execute("SELECT exp from stats")
                print("     Exp : ",end='')
                print("{}".format(self.c.fetchone()[0]))

                continue

            elif words[0] == 'check':
                # check inventory for object 
                self.c.execute("SELECT name FROM inventory") 
                count = 0 

                for item in self.c.fetchall():
                    print("You have in your inventory: ",end='')
                    print("{} ".format(item[0]), end='')
                    count = count + 1 

                if count == 0:
                    print("There's nothing in your inventory, you poor penniless pauper!", end='')
                
                print("")

            elif words[0] == 'place':
                # place loot command 
                item = str(input("Choose an item from your inventory: "))
                # update the room with the chosen loot 
                self.c.execute("SELECT name FROM inventory") 
                has_item = False 

                for x in self.c.fetchall():
                    if str(x[0]) == item: 
                        has_item = True 

                if has_item == False:
                    print("You don't have a {} in your inventory. Use 'check' to survey your current inventory.".format(item))
                    continue 
                else: 
                    query = 'UPDATE rooms SET loot = ("{}") WHERE id=("{}")'.format(item,self.current_room)
                    self.c.execute(query) 
                    print("You've placed {} in the room.".format(item))
                
                    ## remove this item from our inventory now 
                    ## right now we are assuming that user will only ask to place an item
                    ## that is actually in their inventory 
                    query = 'DELETE FROM inventory WHERE name=("{}")'.format(item)
                    self.c.execute(query)

            # todo: if player ends turn in a room with a hostile mob
            # figure out how to handle combat.
            elif words[0] == 'fight': 
                self.c.execute("SELECT name FROM mobs WHERE room_id={}".format(self.current_room))
                if str(self.c.fetchone()) == 'None':
                    print("There are no monsters in this room.")
                else:
                    self.c.execute("SELECT name FROM mobs WHERE room_id={}".format(self.current_room))
                    monster = self.c.fetchone()[0] 
                    print("Get ready to fight {} (ง •̀_•́)ง ".format(monster))

                ## STATE 
                self.c.execute("SELECT state from stats")
                state = self.c.fetchone()[0]

                if state == 'dead':
                    print("You are dead! Game over.")
                    break

            else:
                print("unknown command {}".format(words[0]))

        # all done, clean exit
        print("------------------------------------------------------------------------------------------------")
        self.db.commit()
        self.db.close()

    # describe this room and its exits
    def doLook(self,force_florid):
        # We show the florid description only the first time we visit
        # a room, or if someone types "look" explicitly (so will
        # probably want a force_florid optional parameter to this function) 

        if force_florid == 0:
            ## Determine if we've already visited this room or not. 
            self.c.execute("SELECT visit FROM rooms WHERE id={}".format(self.current_room))
            status = self.c.fetchone()[0]

            if status == 0:        
                ## we have not visited this room yet—give florid description
                self.c.execute("SELECT florid_desc FROM rooms WHERE id={}".format(self.current_room))
                print(self.c.fetchone()[0])

                ## read off the available loot
                self.c.execute("SELECT loot FROM rooms WHERE id={}".format(self.current_room))
                item = str(self.c.fetchone()[0])

                if item != 'none':
                    print("This room contains a {}.".format(item)) 
                else:
                    print("No items in this room.") 

                ## inform visitor of monsters, if any 
                self.c.execute("SELECT name FROM mobs WHERE room_id={}".format(self.current_room))
                if str(self.c.fetchone()) == 'None':
                    pass
                else:
                    self.c.execute("SELECT name FROM mobs WHERE room_id={}".format(self.current_room))
                    monster = self.c.fetchone()[0] 
                    print("There's a {} in this room (ง •̀_•́)ง ".format(monster))

                ## update visit integer mark this room as visited
                self.c.execute("UPDATE rooms SET visit = 1 WHERE id={}".format(self.current_room))

            else:                   
                ## we've visited this room already—give simple description
                self.c.execute("SELECT short_desc FROM rooms WHERE id={}".format(self.current_room))
                print(self.c.fetchone()[0])

                ## read off the available loot
                self.c.execute("SELECT loot FROM rooms WHERE id={}".format(self.current_room))
                item = str(self.c.fetchone()[0]) 

                if item != 'none':
                    print("This room contains a {}.".format(item)) 
                else:
                    print("No items in this room.") 

                # inform visitors of monsters, if any
                self.c.execute("SELECT name FROM mobs WHERE room_id={}".format(self.current_room))
                if str(self.c.fetchone()) == 'None':
                    pass
                else:
                    self.c.execute("SELECT name FROM mobs WHERE room_id={}".format(self.current_room))
                    monster = self.c.fetchone()[0] 
                    print("There's a {} in this room (ง •̀_•́)ง ".format(monster))


        ## Give the full-description since force-florid is switched on. 
        else: 
            self.c.execute("SELECT florid_desc FROM rooms WHERE id={}".format(self.current_room))
            print(self.c.fetchone()[0])

        ## Present the available exits, if any 
        self.c.execute("SELECT dir FROM exits WHERE from_room={}".format(self.current_room))
        print("There are exits in these directions: ", end='')
        count = 0 
        for exit in self.c.fetchall():
            print("{} ".format(exit[0]), end='')
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
            self.c.execute("DROP TABLE if exists inventory")
            self.c.execute("DROP TABLE if exists loot")
            self.c.execute("DROP TABLE if exists exits")
            self.c.execute("DROP TABLE if exists stats")  
            ## API: rooms will keep track of the name of the loot item that they contain, if any 
            self.c.execute("CREATE TABLE rooms (id INTEGER PRIMARY KEY AUTOINCREMENT, short_desc TEXT, florid_desc TEXT, visit INTEGER, loot TEXT)")
            self.c.execute("CREATE TABLE mobs (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, health INTEGER,atp_power INTEGER,def_power INTEGER,exp INTEGER,room_id INTEGER)")
            self.c.execute("CREATE TABLE exits (from_room INTEGER, to_room INTEGER, dir TEXT)")
            # table for stats 
            self.c.execute("CREATE TABLE stats (health INTEGER,state TEXT,weapon TEXT,armor TEXT,class TEXT,atp_power INTEGER,def_power INTEGER,exp INTEGER)")
            self.c.execute("INSERT INTO stats (health,state,weapon,armor,class,atp_power,def_power,exp) VALUES (100,'normal','none','none','hero',10,10,0)")

            # table for loot items
            self.c.execute("CREATE TABLE loot (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, des TEXT, available INTEGER)")
            # table for inventory 
            self.c.execute("CREATE TABLE inventory (name TEXT)")
            ## create entrance
            self.c.execute("INSERT INTO rooms (florid_desc, short_desc,visit,loot) VALUES ('You are standing at the entrance of what appears to be a vast, complex cave.', 'entrance',0,'none')")

            self.db.commit()

        # now we know the db exists - fetch the first room, which is
        # the entrance
        self.c.execute("SELECT MIN(id) FROM rooms")
        entrance_p = self.c.fetchone()
        
        brief = "shovel room"
        florid = "You are in a small, darkly-lit room."
        loot = "shovel"
        query = 'INSERT INTO rooms (short_desc, florid_desc,visit,loot) VALUES ("{}", "{}","{}","{}")'.format(brief,florid,0,loot)
        self.c.execute(query)
        new_room_id = self.c.lastrowid
        # now add tunnels in both directions
        query = 'INSERT INTO exits (from_room, to_room, dir) VALUES ({}, {}, "{}")'.format(entrance_p[0], new_room_id,"n")
        self.c.execute(query) 
        query = 'INSERT INTO exits (from_room, to_room, dir) VALUES ({}, {}, "{}")'.format(new_room_id, entrance_p[0],"s")
        self.c.execute(query)

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
    print("Use 'check' to survey your inventory, 'take' to steal loot, 'place' to leave loot behind,")
    print("'view' to check your stats, 'spawn' to create monsters, and 'fight' to engage in combat.")
    d.repl()
