import sys
import os
import fileinput
import sqlite3
import readline

## Dungeon project built off Dylan's code. 
shovel = None
never_before = True  


class Dungeon:
    """
    """

    dungeon_map = "dungeon.map"
    prompt = '> '
   
    ## MONSTERS :  minotaur, orc, plant, rat, ogre, scorpion, skeleton, giant-ant 🐜 ,bat 🦇,slime, snake🐍,
    ## succubus, werewolf, zombie, skeleton, vampire, chimera, cerberus, spider, ghost,taco 🌮,fairy🧚‍, dragon 🐉,
    ## dinosaur-of-yore 🦕, bee-of-disproportionate-size 🐝, mostly-friendly-wolf 🐺, pineapple 🍍,
    ## kleptomaniac-squirrel-of-doom 🐿, the-great-mage 🧙‍♂️ apprentice 🧙‍♀️, merman 🧜, mermaid 🧜‍♀️, elf 🧝, unicorn 🦄
    ## owl 🦉, whale 🐳, dolphin 🐬, magical-fish-out-of-water 🐟, blowfish 🐡, octopus 🐙, caterpillar-of-phenomenal-power 🐛
    ## zombie🧟, monarch-butterfly 🦋, evil-shrimp 🦐, alien 🛸, time ⏱, bad-weather ⛈, god-of-north-wind 🌬, umbrella 🌂, fire 🔥
    ## jack-o-lantern 🎃

    ## LOOT / ITEMS : plain-chest, golden-chest, steel-chest, mini-chest
    ## mana-crystal, pick-axe, potion, blue-book 📘, green-book 📗, orange-book 📙, tome 📖, ring, herb, shield, crystal,
    ## crown-of-awesome 👑, apple 🍎, beer 🥃, ramen 🍜, ISS 🛰 (the international
    ## space station), tent ⛺️, crystal-ball 🔮,portal 🌀, flower 🌸, wheat 🌾, herb 🌿, mushroom 🍄, tulip 🌷, beer 🥃, 
    ## candle 🕯, bed 🛌, revival-dove 🕊, shell 🐚, grapes 🍇,  banana 🍌, lemon 🍋, watermelon 🍉, grapes 🍇, peach 🍑
    ## cherry 🍒, strawberry 🍓, kiwi 🥝, corn 🌽, popcorn 🍿, chinese-takeout 🥡, salt-and-straw-icecream 🍨, grandma's-pie 🥧
    ## honey 🍯, tea 🍵, wine 🍷, amphora-of-the-ancients 🏺, the-world 🌍, volcanic-mountain 🌋, paradise-island 🏝, 
    ## Athens 🏛 , the-american-dream 🏠, the-Federal-Reserve 🏦, hospital 🏥, statue-of-liberty 🗽, money-bag 💰 

    ## WEAPONS : sword, pick-axe,bow 🏹 ,dagger🗡,spear,claw,crossbow, hammer 🔨, wand 

    ## GUILDS:  Guild-of-Mages, Guild-of-The-Dark-Arts 👾, Guild-of-Chronic-Procrastinators, Guild-of-the-Learned, 
    ## Guild-of-the-Ancients (a *secret* guild), Guild-of-Champions 🏆  

    ## CLASSES : hero, warrior, mage, priest, scholar

    ## SKILLS : attack, guard, double-attack,triple-attack,heal

    ## STATES : knockout 😖, rage 😡, confusion 😖, fear 😱, asleep 😴, immortal 😎, blind 😵, normal, dead 🤯
    ## extremely-intellectual🧐, unbearably-cool 🤠, sick 🤒, cat 😼, not-ready-for-adult-life 🧖‍♀️, snail 🐌, on-spring-break 🍹

    def repl(self):
        cmd = ''
        global shovel
        global never_before

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

            # purchase stat upgrades
            elif words[0] == 'purchase':
                # get current amount of gold  
                self.c.execute("SELECT gold from stats") 
                my_gold = self.c.fetchone()[0] 
                self.c.execute("SELECT health from stats")
                curr_health = int(self.c.fetchone()[0]) 
                self.c.execute("SELECT atp_power from stats")
                curr_atk = int(self.c.fetchone()[0]) 
                self.c.execute("SELECT def_power from stats")
                curr_def = int(self.c.fetchone()[0]) 

                print("You currently have {} in gold.".format(my_gold)) 
                print("What stat would you like to upgrade?")  
                answer = int(input("Choose (1) health, (2) atp_power, (3) def_power: "))
                if answer == 1:
                    print("It costs 1 piece of gold to upgrade your health by 1.")
                    gold_to_spend = int(input("Type how much gold you would like to spend to increase your health: "))
                    if gold_to_spend > my_gold:
                        print("You can't afford that stat increase.")
                    else: 
                        query = 'UPDATE stats SET health = ("{}")'.format(curr_health+gold_to_spend)
                        self.c.execute(query)
                        print("You've increased your health power by {}".format(gold_to_spend)) 

                        # update your gold stat
                        calc = my_gold-gold_to_spend
                        query = 'UPDATE stats SET gold = ("{}")'.format(calc)
                        self.c.execute(query) 


                elif answer == 2:
                    print("It costs 5 piece of gold to upgrade your attack power by 1.")
                    gold_to_spend = int(input("Type how much gold you would like to spend to increase your attack power: "))
                    if gold_to_spend > my_gold:
                        print("You can't afford that stat increase.")
                    else: 
                        stat_add = gold_to_spend/5 
                        query = 'UPDATE stats SET atk_power = ("{}")'.format(curr_atk+stat_add)
                        self.c.execute(query) 
                        print("You've increased your attack power by {}".format(stat_add))

                        # update your gold stat
                        calc = my_gold-gold_to_spend
                        query = 'UPDATE stats SET gold = ("{}")'.format(calc)
                        self.c.execute(query) 

                elif answer == 3: 
                    print("It costs 5 piece of gold to upgrade your defense power by 1.")
                    gold_to_spend = int(input("Type how much gold you would like to spend to increase your defense power: "))
                    if gold_to_spend > my_gold:
                        print("You can't afford that stat increase.")
                    else: 
                        stat_add = gold_to_spend/5 
                        calc = curr_def + stat_add
                        query = 'UPDATE stats SET def_power = ("{}")'.format(calc)
                        self.c.execute(query) 
                        print("You've increased your defense power by {}".format(stat_add))

                        # update your gold stat
                        calc = my_gold-gold_to_spend
                        query = 'UPDATE stats SET gold = ("{}")'.format(calc)
                        self.c.execute(query) 


            # destroy the dungeon and start over
            elif words[0] == 'new':
                print("Type 1 to go forward with this operation, unless you've recognized the importance of preserving cultural artifacts like dungeons!") 
                answer = int(input("Are you sure? "))
                if answer == 1: 
                    self.c.execute("DROP TABLE rooms")
                    self.c.execute("DROP TABLE mobs")
                    self.c.execute("DROP TABLE Inventory")
                    self.c.execute("DROP TABLE loot")
                    self.c.execute("DROP TABLE monster_desc")
                    self.c.execute("DROP TABLE item_desc")
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

                # get current user status 
                self.c.execute("SELECT status from stats") 
                my_status = self.c.fetchone()[0] 

                # check inventory for a shovel 
                self.c.execute("SELECT name FROM inventory") 

                for item in self.c.fetchall():
                    if item[0] == 'shovel': 
                        yes_shovel = True 

                if yes_shovel == True or my_status == "super":  
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
                # only users with a shovel in their inventory can dig rooms
                yes_crystal = False
 
                # get current user status 
                self.c.execute("SELECT status from stats") 
                my_status = self.c.fetchone()[0] 

                # check inventory for a shovel 
                self.c.execute("SELECT name FROM inventory") 

                for item in self.c.fetchall():
                    if item[0] == 'crystal': 
                        yes_crystal = True 

                if yes_crystal == True or my_status == "super":
                    # to-do: only players with Monster Crystal can spawn a monster 
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

                else:
                    if (never_before == True):
                        print("I know, I know. It sounds like fun to just spawn a monster out of nothing. But there are limitations in life. I'd like to snap my hands and have all my wishes come true.")
                        print("This is the adult world, and in order to spawn a monster you need a crystal. So: go get a crystal, and then try again!")
                        never_before = False
                    else:
                        print("Come back when you have a monster crystal!!")

             

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

                ## GUILD
                self.c.execute("SELECT guild from stats")
                print("     Guild : ",end='')
                print("{}".format(self.c.fetchone()[0]))

                ## GOLD 
                self.c.execute("SELECT gold from stats")
                print("     Gold : ",end='')
                print("{}".format(self.c.fetchone()[0]))

                continue

            elif words[0] == 'equip':
                answer = int(input("Would you to like to equip yourself with (1) armor or (2) weapon? "))
                if answer == 1:
                    # EQUIP ARMOR 
                    armor = str(input("Choose armor to equip from your inventory: "))
                    self.c.execute("SELECT name FROM inventory") 
                    has_armor = False 

                    for x in self.c.fetchall():
                        if str(x[0]) == armor: 
                            has_armor = True 

                    if has_armor == False:
                        print("You don't have a {} in your inventory. Use 'check' to survey your current inventory.".format(armor))
                        continue 
                    else: 
                        query = 'UPDATE stats SET armor = ("{}")'.format(armor)
                        self.c.execute(query) 
                        print("You've equipped yourself with {}!".format(armor))
                        query = 'DELETE FROM inventory WHERE name=("{}")'.format(armor)
                        self.c.execute(query)

                elif answer == 2: 
                    # EQUIP WEAPON 
                    weapon = str(input("Choose a weapon to equip from your inventory: "))
                    self.c.execute("SELECT name FROM inventory") 
                    has_weapon = False 

                    for x in self.c.fetchall():
                        if str(x[0]) == weapon: 
                            has_weapon = True 

                    if has_weapon == False:
                        print("You don't have a {} in your inventory. Use 'check' to survey your current inventory.".format(weapon))
                        continue 
                    else: 
                        query = 'UPDATE stats SET weapon = ("{}")'.format(weapon)
                        self.c.execute(query) 
                        print("You've equipped yourself with {}!".format(weapon))
                        query = 'DELETE FROM inventory WHERE name=("{}")'.format(weapon)
                        self.c.execute(query)
        
                # check inventory for armor and weapons 
                # self.c.execute("SELECT name FROM inventory") 

                    #for item in self.c.fetchall():
                    #    if item[0] == 'crystal': 
                    #        yes_crystal = True 


            elif words[0] == 'set_status:super':
                query = 'UPDATE stats SET status = ("{}")'.format("super")
                self.c.execute(query) 
                print("You now have super-user privileges.")

            elif words[0] == 'join': 
                # join a guild for item bonuses 
                # make sure you are not in a guild already
                self.c.execute("SELECT guild from stats") 
                if (self.c.fetchone()[0] != 'none'):
                    print("Sorry, but you are already in the ",end='')
                    self.c.execute("SELECT guild from stats") 
                    print("{}".format(self.c.fetchone()[0]))
                    print("You may only join one guild at a time.")
                else: 
                    answer = int(input("Select a guild to join: Guild-of-Mages(0), Guild-of-The-Dark-Arts👾(1), Guild-of-Chronic-Procrastinators(2),Guild-of-the-Learned(3). "))  
                    if (answer == 0):
                        print("You have joined the Guild of Mages!")
                        print("As a welcome gift, you have received revival-dove, mini-chest, money-bag, plain-chest, golden-chest, steel-chest, and crown-of-awesome.")
                        query = 'UPDATE stats SET guild = ("{}")'.format("Guild-of-Mages")
                        self.c.execute(query) 

                        # Welcome pack: revival-dove, mini-chest, money-bag, plain-chest, golden-chest, steel-chest, crown-of-awesome.
                        #query = 'INSERT INTO inventory (name) VALUES ("{}")'.format(item)
                        #self.c.execute(query) 

                        # New class is `mage`.
                        query = 'UPDATE stats SET class = ("{}")'.format("mage")
                        self.c.execute(query) 
                        print("Your new class is mage.")

                        # New state is `unbearably cool`. 
                        query = 'UPDATE stats SET state = ("{}")'.format("unbearably-cool🤠")
                        self.c.execute(query) 
                        print("Your new state is unbearably-cool🤠.")


                    elif (answer == 1):
                        print("You have joined the Guild of The Dark Arts👾!")
                        print("As a welcome gift, you have received wand, potion, crystal-ball, and portal. ")
                        query = 'UPDATE stats SET guild = ("{}")'.format("Guild-of-the-Dark-Arts👾")
                        self.c.execute(query) 

                        # Welcome pack has wand, potion, crystal-ball, and portal. 
                        #query = 'INSERT INTO inventory (name) VALUES ("{}")'.format(item)
                        #self.c.execute(query) 

                        # New class is `necromancer`.
                        query = 'UPDATE stats SET class = ("{}")'.format("nercomancer")
                        self.c.execute(query) 
                        print("Your new class is necromancer.")

                         # New state is `immortal`. 
                        query = 'UPDATE stats SET state = ("{}")'.format("immortal")
                        self.c.execute(query) 
                        print("Your new state is immortal.")


                    elif (answer == 2):
                        print("You have joined the Guild of Chronic Procrastinators!")
                        print("As a welcome gift, you have received tent, beer, ramen, popcorn, wine, chinese-takeout, salt-and-straw-icecream, and bed.")
                        query = 'UPDATE stats SET guild = ("{}")'.format("Guild-of-Chronic-Procrastinators")
                        self.c.execute(query) 

                        # Welcome pack has tent, beer, ramen, popcorn, wine, chinese-takeout, salt-and-straw-icecream, and bed.
                        #query = 'INSERT INTO inventory (name) VALUES ("{}")'.format(item)
                        #self.c.execute(query)

                        # New state is `not-ready-for-adult-life`. 
                        query = 'UPDATE stats SET state = ("{}")'.format("not-ready-for-adult-life🧖‍♀️")
                        self.c.execute(query) 
                        print("Your new state is not-ready-for-aduralt-life🧖‍♀️.")

                        # New class is `scholar`.
                        query = 'UPDATE stats SET class = ("{}")'.format("warrior")
                        self.c.execute(query) 
                        print("Your new class is warrior.")


                    elif (answer == 3):
                        print("You have joined the Guild of the Learned!")
                        print("As a welcome gift, you have received red-book, green-book, orange-book, and tome.")
                        query = 'UPDATE stats SET guild = ("{}")'.format("Guild-of-the-Learned")
                        self.c.execute(query) 

                        # `Welcome pack has red-book, green-book, orange-book, tome.
                        #query = 'INSERT INTO inventory (name) VALUES ("{}")'.format(item)
                        #self.c.execute(query) 


                        # New class is `scholar`.
                        query = 'UPDATE stats SET class = ("{}")'.format("scholar")
                        self.c.execute(query) 
                        print("Your new class is scholar.")

                        # New state is extremely-intellectual🧐
                        query = 'UPDATE stats SET state = ("{}")'.format("extremely-intellectual🧐")
                        self.c.execute(query) 
                        print("Your new state is extremely-intellectual🧐.")


                    else:
                        print("That's not a valid guild number!")
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

                    ## STATS: health,state,weapon,armor,class,atp_power,def_power,exp,guild,gold
                    self.c.execute("SELECT health from stats")
                    curr_health = int(self.c.fetchone()[0]) 
                    self.c.execute("SELECT atp_power from stats")
                    curr_atk = int(self.c.fetchone()[0]) 
                    self.c.execute("SELECT def_power from stats")
                    curr_def = int(self.c.fetchone()[0]) 

                    if state == 'dead🤯':
                        print("You are dead! Game over.")
                        break

                    elif state == 'knockout😖':
                        ## Knockout decreases attack power by 200  
                        query = 'UPDATE stats SET atp_power = ("{}") WHERE id=("{}")'.format(curr_atk-100)
                        self.c.execute(query) 

                    elif state == 'rage😡': 
                        ## Rage gives attack power boost of 100 
                        query = 'UPDATE stats SET atp_power = ("{}") WHERE id=("{}")'.format(curr_atk+100)
                        self.c.execute(query)  

                    elif state == 'confusion😖': 
                        ## Confusion decreases attack power by 25 
                        query = 'UPDATE stats SET atp_power = ("{}") WHERE id=("{}")'.format(curr_atk-25)
                        self.c.execute(query)  

                    elif state == 'fear😱': 
                        ## Fear increases defense power by 100 
                        query = 'UPDATE stats SET def_power = ("{}") WHERE id=("{}")'.format(curr_def+100)
                        self.c.execute(query)  

                    elif state == 'asleep😴':  
                        ## Asleep decreases defense power by 200  
                        query = 'UPDATE stats SET def_power = ("{}") WHERE id=("{}")'.format(curr_def-200)
                        self.c.execute(query) 


                    elif state == 'immortal😎':  
                        ## Immortality increases defense power by 10,000 
                        query = 'UPDATE stats SET def_power = ("{}") WHERE id=("{}")'.format(curr_def+10000)
                        self.c.execute(query) 

                    elif state == 'blind😵':  
                        ## Blind decreases defense power by 400 
                        query = 'UPDATE stats SET def_power = ("{}") WHERE id=("{}")'.format(curr_def-400)
                        self.c.execute(query) 

                    elif state == 'extremely-intellectual🧐': 
                        ## Being extremely intellectual decreases health by 500 
                        query = 'UPDATE stats SET health = ("{}") WHERE id=("{}")'.format(health-500)
                        self.c.execute(query) 

                    elif state == 'unbearably-cool🤠': 
                        ## Being unbearably cool increases attack power by 10,000 
                        query = 'UPDATE stats SET atp_power = ("{}") WHERE id=("{}")'.format(curr_atk+10000)
                        self.c.execute(query) 

                    elif state == 'sick🤒':
                        ## Sickness decreases attack power by 60 
                        self.c.execute("SELECT atp_power from stats")
                        curr_atk = int(self.c.fetchone()[0]) 
                        query = 'UPDATE stats SET atp_power = ("{}") WHERE id=("{}")'.format(curr_atk-60)
                        self.c.execute(query) 

                    elif state == 'cat😼': 
                        ## Being a cat increases attack power by 500 
                        self.c.execute("SELECT atp_power from stats")
                        curr_atk = int(self.c.fetchone()[0]) 
                        query = 'UPDATE stats SET atp_power = ("{}") WHERE id=("{}")'.format(curr_atk+500)
                        self.c.execute(query) 

                    elif state == 'not-ready-for-adult-life🧖‍♀️': 
                        ## Not ready for adult life decreases defense power by 500
                        query = 'UPDATE stats SET def_power = ("{}") WHERE id=("{}")'.format(curr_def-500)
                        self.c.execute(query) 

                    elif state == 'snail🐌': 
                        ## Snail decreases defense power by 10,000,0000
                        query = 'UPDATE stats SET def_power = ("{}") WHERE id=("{}")'.format(curr_def-100000000)
                        self.c.execute(query) 

                    elif state == 'on-spring-break🍹': 
                        ## On spring break increases health by 500 
                        query = 'UPDATE stats SET health = ("{}") WHERE id=("{}")'.format(curr_health+500)
                        self.c.execute(query) 

                    else:
                        continue 

                    ## to do: increase stats based on weaponry and armors 
                    # ARMOR 


                    # 

                    # BEGIN BATTLE MECHANISM
                    while True:
                        ## CHOOSE SKILL TO USE 


                        ## INCREASE POWER OF SKILL BY ATTACK POWER 


                        ## LOWER DAMAGE DONE BY MONSTER BY DEENSE POWER 
                        break 

                    # END BATTLE MECHANISM 

                    # COLLECT LOOT 


                ## After battle, return player stats to original before boost/decrease from state 
                ##query = 'UPDATE stats SET health = ("{}") WHERE id=("{}")'.format(curr_health)
                ##self.c.execute(query)
                ##query = 'UPDATE stats SET def_power = ("{}") WHERE id=("{}")'.format(curr_def)
                ##self.c.execute(query)  
                ##query = 'UPDATE stats SET atp_power = ("{}") WHERE id=("{}")'.format(curr_atk)
                ##self.c.execute(query) 

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
        global shovel 

        if (db_exists == None):
            self.c.execute("DROP TABLE if exists rooms")
            self.c.execute("DROP TABLE if exists mobs")
            self.c.execute("DROP TABLE if exists inventory")
            self.c.execute("DROP TABLE if exists loot")
            self.c.execute("DROP TABLE if exists exits")
            self.c.execute("DROP TABLE if exists stats")  
            shovel = False
            ## API: rooms will keep track of the name of the loot item that they contain, if any 
            self.c.execute("CREATE TABLE rooms (id INTEGER PRIMARY KEY AUTOINCREMENT, short_desc TEXT, florid_desc TEXT, visit INTEGER, loot TEXT)")
            self.c.execute("CREATE TABLE mobs (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, health INTEGER,atp_power INTEGER,def_power INTEGER,exp INTEGER,room_id INTEGER)")
            self.c.execute("CREATE TABLE exits (from_room INTEGER, to_room INTEGER, dir TEXT)")
            # table for stats 
            self.c.execute("CREATE TABLE stats (health INTEGER,state TEXT,weapon TEXT,armor TEXT,class TEXT,atp_power INTEGER,def_power INTEGER,exp INTEGER,guild TEXT, gold INTEGER,status TEXT)")
            self.c.execute("INSERT INTO stats (health,state,weapon,armor,class,atp_power,def_power,exp,guild,gold,status) VALUES (100,'normal','none','none','hero',10,10,0,'none',1000,'normal')")

            # table for loot items 
            self.c.execute("CREATE TABLE loot (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, des TEXT, available INTEGER)")
            # table for inventory 
            self.c.execute("CREATE TABLE inventory (name TEXT)")
            ## create entrance
            self.c.execute("INSERT INTO rooms (florid_desc, short_desc,visit,loot) VALUES ('You are standing at the entrance of what appears to be a vast, complex cave.', 'entrance',0,'none')")

            # item description table
            self.c.execute("CREATE TABLE item_desc (name TEXT)")

            # monster description table
            self.c.execute("CREATE TABLE monster_desc (name TEXT)")

            ## populate the item table


            ## populate the monster description table 


            self.db.commit()

        # now we know the db exists - fetch the first room, which is
        # the entrance
        self.c.execute("SELECT MIN(id) FROM rooms")
        entrance_p = self.c.fetchone()

        if (shovel == False):
            self.c.execute("SELECT MIN(id) FROM rooms")
            brief = "shovel room"
            florid = "You are in a tiny, darkly-lit room."
            loot = "shovel"
            query = 'INSERT INTO rooms (short_desc, florid_desc,visit,loot) VALUES ("{}", "{}","{}","{}")'.format(brief,florid,0,loot)
            self.c.execute(query)
            new_room_id = self.c.lastrowid
            # now add tunnels in both directions
            query = 'INSERT INTO exits (from_room, to_room, dir) VALUES ({}, {}, "{}")'.format(entrance_p[0], new_room_id,"e")
            self.c.execute(query) 
            query = 'INSERT INTO exits (from_room, to_room, dir) VALUES ({}, {}, "{}")'.format(new_room_id, entrance_p[0],"w")
            self.c.execute(query)
            shovel = True 

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
    print("Welcome to the ( ͡° ͜ʖ ͡°) Try 'look' to see room descriptions, 'go' to use an exit,")
    print("'dig' to create a new room, and 'new' to start the dungeon creation process over again.")
    print("Use 'check' to survey your inventory, 'take' to steal loot, 'place' to leave loot behind,")
    print("'view' to check your stats, 'use' to employ an item and 'fight' to engage in combat.")
    print("To join a guild, type 'join' & select a Guild. Some guilds can only be joined via events.")
    print("If you have a crystal in your inventory you can spawn a monster: type 'spawn.'")
    print("Type 'purchase' to use your gold to upgrade stats like health, atp_power, and def_power.")
    print("Type 'equip' to equip yourself with weapons and armor from your inventory.")
    d.repl()
