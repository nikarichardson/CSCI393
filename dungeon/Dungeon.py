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
	## werewolf, zombie, skeleton, vampire, chimera, cerberus, spider, ghost,taco 🌮,fairy🧚‍, dragon 🐉,
	## dinosaur-of-yore 🦕, bee-of-disproportionate-size 🐝, mostly-friendly-wolf 🐺, pineapple 🍍,
	## kleptomaniac-squirrel-of-doom 🐿, the-great-mage 🧙‍♂️ apprentice 🧙‍♀️, merman 🧜 elf 🧝, unicorn 🦄
	## owl 🦉, whale 🐳, dolphin 🐬, magical-fish-out-of-water 🐟, blowfish 🐡, octopus 🐙, caterpillar-of-phenomenal-power 🐛
	## zombie🧟, monarch-butterfly 🦋, evil-shrimp 🦐, alien 🛸, time ⏱, bad-weather ⛈, god-of-north-wind 🌬, umbrella 🌂, fire 🔥
	## jack-o-lantern 🎃

	## LOOT / ITEMS : plain-chest, golden-chest, steel-chest, mini-chest, mana-crystal, pick-axe, potion, blue-book 📘, 
	## green-book 📗, orange-book 📙, tome 📖, ring, shield, crystal, crown-of-awesome 👑, apple 🍎, beer 🥃, ramen 🍜, 
	## ISS 🛰 (the international space station), tent ⛺️, crystal-ball 🔮,portal 🌀, flower 🌸, wheat 🌾, herb 🌿, 
	## mushroom 🍄, tulip 🌷, beer 🥃, candle 🕯, bed 🛌, revival-dove 🕊, shell 🐚, grapes 🍇,  banana 🍌, lemon 🍋, 
	## watermelon 🍉, grapes 🍇, peach 🍑, cherry 🍒, strawberry 🍓, kiwi 🥝, corn 🌽, popcorn 🍿, chinese-takeout 🥡,
	## salt-and-straw-icecream 🍨, grandma's-pie 🥧, honey 🍯, tea 🍵, wine 🍷, amphora-of-the-ancients 🏺, the-world 🌍,
	## volcanic-mountain 🌋, paradise-island 🏝, Athens 🏛 , the-american-dream 🏠, the-Federal-Reserve 🏦, hospital 🏥, 
	## statue-of-liberty 🗽, money-bag 💰 

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
				self.c.execute("SELECT atk_power from stats")
				curr_atk = int(self.c.fetchone()[0]) 
				self.c.execute("SELECT def_power from stats")
				curr_def = int(self.c.fetchone()[0]) 

				print("You currently have {} in gold.".format(my_gold)) 
				print("What stat would you like to upgrade?")  
				answer = int(input("Choose (1) health, (2) atk_power, (3) def_power: "))
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
				# make sure we have the first, firstly 
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
					## user has the item 
					## call getItem function 
					self.useItem(item) 

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
					print("You can spawn the following monster objects: minotaur, orc, plant, rat, ogre, scorpion, skeleton, slime, snake, werewolf, zombie, skeleton, vampire, chimera, cerberus, spider, ghost, fairy, dragon.")
					my_monster = str(input("Type the name of a monster object: "))

					## to do: connect to second monster type database that holds all the descriptions and stats of each type of monster 

					## now we need to update the table of monster objects and 'place' the monster in the room 
					query = 'INSERT INTO mobs (name,health,atk_power,def_power,exp,room_id) VALUES ("{}",500,100,100,100,"{}")'.format(my_monster,self.current_room)
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

				## ATK_POWER
				self.c.execute("SELECT atk_power from stats")
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
						print("As a welcome gift, you have received revival-dove🕊, mini-chest, money-bag, plain-chest, golden-chest, steel-chest, and crown-of-awesome👑.")
						query = 'UPDATE stats SET guild = ("{}")'.format("Guild-of-Mages")
						self.c.execute(query) 

						# Welcome pack: revival-dove🕊, mini-chest, money-bag💰, plain-chest, golden-chest, steel-chest, crown-of-awesome👑.
						query = 'INSERT INTO inventory (name) VALUES ("{}")'.format("revival-dove🕊")
						self.c.execute(query) 
						query = 'INSERT INTO inventory (name) VALUES ("{}")'.format("mini-chest")
						self.c.execute(query) 
						query = 'INSERT INTO inventory (name) VALUES ("{}")'.format("money-bag💰")
						self.c.execute(query) 
						query = 'INSERT INTO inventory (name) VALUES ("{}")'.format("plain-chest")
						self.c.execute(query) 
						query = 'INSERT INTO inventory (name) VALUES ("{}")'.format("golden-chest")
						self.c.execute(query) 
						query = 'INSERT INTO inventory (name) VALUES ("{}")'.format("steel-chest")
						self.c.execute(query) 
						query = 'INSERT INTO inventory (name) VALUES ("{}")'.format("crown-of-awesome👑")
						self.c.execute(query) 

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
						print("As a welcome gift, you have received wand, potion, crystal-ball🔮, and portal🌀. ")
						query = 'UPDATE stats SET guild = ("{}")'.format("Guild-of-the-Dark-Arts👾")
						self.c.execute(query) 

						# Welcome pack has wand, potion, crystal-ball, and portal🌀. 
						query = 'INSERT INTO inventory (name) VALUES ("{}")'.format("wand")
						self.c.execute(query) 
						query = 'INSERT INTO inventory (name) VALUES ("{}")'.format("potion")
						self.c.execute(query) 
						query = 'INSERT INTO inventory (name) VALUES ("{}")'.format("crystal-ball🔮")
						self.c.execute(query) 
						query = 'INSERT INTO inventory (name) VALUES ("{}")'.format("portal🌀")
						self.c.execute(query) 

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
						print("As a welcome gift, you have received tent⛺️, beer🥃, ramen🍜, popcorn, wine, chinese-takeout, salt-and-straw-icecream, and bed.")
						query = 'UPDATE stats SET guild = ("{}")'.format("Guild-of-Chronic-Procrastinators")
						self.c.execute(query) 

						# Welcome pack has tent⛺️, beer🥃, ramen🍜, popcorn🍿, wine🍷, chinese-takeout🥡, salt-and-straw-icecream🍨, and bed🛌.
						query = 'INSERT INTO inventory (name) VALUES ("{}")'.format("tent⛺️")
						self.c.execute(query)
						query = 'INSERT INTO inventory (name) VALUES ("{}")'.format("beer🥃")
						self.c.execute(query)
						query = 'INSERT INTO inventory (name) VALUES ("{}")'.format("ramen🍜")
						self.c.execute(query)
						query = 'INSERT INTO inventory (name) VALUES ("{}")'.format("popcorn🍿")
						self.c.execute(query)
						query = 'INSERT INTO inventory (name) VALUES ("{}")'.format("wine🍷")
						self.c.execute(query)
						query = 'INSERT INTO inventory (name) VALUES ("{}")'.format("chinese-takeout🥡")
						self.c.execute(query)
						query = 'INSERT INTO inventory (name) VALUES ("{}")'.format("salt-and-straw-icecream🍨")
						self.c.execute(query)
						query = 'INSERT INTO inventory (name) VALUES ("{}")'.format("bed🛌")
						self.c.execute(query)

						# New state is `not-ready-for-adult-life🧖‍♀️`. 
						query = 'UPDATE stats SET state = ("{}")'.format("not-ready-for-adult-life🧖‍♀️")
						self.c.execute(query) 
						print("Your new state is not-ready-for-adult-life🧖‍♀️.")

						# New class is `scholar`.
						query = 'UPDATE stats SET class = ("{}")'.format("warrior")
						self.c.execute(query) 
						print("Your new class is warrior.")


					elif (answer == 3):
						print("You have joined the Guild of the Learned!")
						print("As a welcome gift, you have received blue-book📘, green-book📗, orange-book📙, and tome📖.")
						query = 'UPDATE stats SET guild = ("{}")'.format("Guild-of-the-Learned")
						self.c.execute(query) 

						# `Welcome pack has blue-book📘, green-book📗, orange-book📙, tome📖.
						query = 'INSERT INTO inventory (name) VALUES ("{}")'.format("blue-book📘")
						self.c.execute(query) 
						query = 'INSERT INTO inventory (name) VALUES ("{}")'.format("green-book📗")
						self.c.execute(query) 
						query = 'INSERT INTO inventory (name) VALUES ("{}")'.format("orange-book📙")
						self.c.execute(query) 
						query = 'INSERT INTO inventory (name) VALUES ("{}")'.format("tome📖")
						self.c.execute(query) 

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

				print("You have in your inventory: ",end='') 

				for item in self.c.fetchall():
					print("{}  ".format(item[0]), end='')
					count = count + 1 

				if count == 0:
					print("There's nothing in your inventory, you poor penniless pauper!", end='')
					print("")
				else: 
					print("")
					want = str(input("Type the name of the item you would like to see the description of: ")) 
					## print description of item 
					query = 'SELECT description FROM item_desc WHERE name = ("{}")'.format(want)
					self.c.execute(query)
					desc = str(self.c.fetchone()[0]) 
					print("    " + desc)
				

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

			elif words[0] == 'teleport':
				# teleport command 
				self.c.execute("SELECT name FROM inventory") 
				has_portal = False 

				for x in self.c.fetchall():
					if str(x[0]) == "portal🌀": 
						has_portal = True 
	

				if has_portal == False:
					print("You don't have a {} in your inventory. Use 'check' to survey your current inventory.".format("portal🌀"))
					continue 
				else: 
					room_id = int(input("Type in the room id of the room you want to teleport to: "))
					#self.c.execute("UPDATE rooms SET visit = 1 WHERE id={}".format(self.current_room))
					self.current_room = room_id
					#self.c.execute("SELECT id FROM rooms WHERE id={}".format(room_id))
					#entrance_p = self.c.fetchone()


			# fight monster in the room 
			elif words[0] == 'fight': 
				self.c.execute("SELECT name FROM mobs WHERE room_id={}".format(self.current_room))
				if str(self.c.fetchone()) == 'None':
					print("There are no monsters in this room.")
				else:
					self.c.execute("SELECT name FROM mobs WHERE room_id={}".format(self.current_room))
					monster = self.c.fetchone()[0] 
					print("Get ready to fight {} (ง •̀_•́)ง ".format(monster))

					## state 
					self.c.execute("SELECT state from stats")
					state = self.c.fetchone()[0]

					## my_stats: health,state,weapon,armor,class,atk_power,def_power,exp,guild,gold
					self.c.execute("SELECT health from stats")
					curr_health = int(self.c.fetchone()[0]) 
					self.c.execute("SELECT atk_power from stats")
					curr_atk = int(self.c.fetchone()[0]) 
					self.c.execute("SELECT def_power from stats")
					curr_def = int(self.c.fetchone()[0]) 
					self.c.execute("SELECT exp from stats")
					curr_exp = int(self.c.fetchone()[0]) 

					# monster_stats : health,atk_power,def_power,exp (amount of experience player gains by defeating)
					self.c.execute("SELECT name FROM mobs WHERE room_id={}".format(self.current_room))
					monster_name = self.c.fetchone()[0]
					self.c.execute("SELECT id FROM mobs WHERE room_id={}".format(self.current_room))
					monster_id = int(self.c.fetchone()[0]) 
					self.c.execute("SELECT atk_power FROM mobs WHERE room_id={}".format(self.current_room))
					monster_atk = int(self.c.fetchone()[0]) 
					self.c.execute("SELECT def_power FROM mobs WHERE room_id={}".format(self.current_room)) 
					monster_def = int(self.c.fetchone()[0]) 
					self.c.execute("SELECT health FROM mobs WHERE room_id={}".format(self.current_room))
					monster_health = int(self.c.fetchone()[0])
					self.c.execute("SELECT exp FROM mobs WHERE room_id={}".format(self.current_room))
					monster_exp = int(self.c.fetchone()[0])

					if state == 'dead🤯':
						print("You are dead! Game over.")
						break

					elif state == 'knockout😖':
						## Knockout decreases attack power by 200  
						calc = curr_atk-200
						query = 'UPDATE stats SET atk_power = ("{}")'.format(calc)
						self.c.execute(query) 

					elif state == 'rage😡': 
						## Rage gives attack power boost of 100 
						calc = curr_atk+100
						query = 'UPDATE stats SET atk_power = ("{}")'.format(calc)
						self.c.execute(query)  

					elif state == 'confusion😖': 
						## Confusion decreases attack power by 25 
						calc = curr_atk-25
						query = 'UPDATE stats SET atk_power = ("{}")'.format(calc)
						self.c.execute(query)  

					elif state == 'fear😱': 
						## Fear increases defense power by 100 
						calc = curr_def+100
						query = 'UPDATE stats SET def_power = ("{}")'.format(calc)
						self.c.execute(query)  

					elif state == 'asleep😴':  
						## Asleep decreases defense power by 200 
						calc = curr_def-200
						query = 'UPDATE stats SET def_power = ("{}")'.format(calc)
						self.c.execute(query) 


					elif state == 'immortal😎':  
						## Immortality increases defense power by 10,000 
						calc = curr_def+10000
						query = 'UPDATE stats SET def_power = ("{}")'.format(calc)
						self.c.execute(query) 

					elif state == 'blind😵':  
						## Blind decreases defense power by 400 
						calc = curr_def-400
						query = 'UPDATE stats SET def_power = ("{}")'.format(calc)
						self.c.execute(query) 

					elif state == 'extremely-intellectual🧐': 
						## Being extremely intellectual decreases health by 500 
						calc = curr_health-500
						query = 'UPDATE stats SET health = ("{}")'.format(calc)
						self.c.execute(query) 

					elif state == 'unbearably-cool🤠': 
						## Being unbearably cool increases attack power by 10,000 
						calc = curr_atk+10000
						query = 'UPDATE stats SET atk_power = ("{}")'.format(calc)
						self.c.execute(query) 

					elif state == 'sick🤒':
						## Sickness decreases attack power by 60 
						calc = curr_atk-60 
						query = 'UPDATE stats SET atk_power = ("{}")'.format(calc)
						self.c.execute(query) 

					elif state == 'cat😼': 
						## Being a cat increases attack power by 500 
						calc = curr_atk+500 
						query = 'UPDATE stats SET atk_power = ("{}")'.format(calc)
						self.c.execute(query) 

					elif state == 'not-ready-for-adult-life🧖‍♀️': 
						## Not ready for adult life decreases defense power by 500
						calc = curr_def-500 
						query = 'UPDATE stats SET def_power = ("{}")'.format(calc)
						self.c.execute(query) 

					elif state == 'snail🐌': 
						## Snail decreases defense power by 10,000,0000
						calc = curr_def-100000000
						query = 'UPDATE stats SET def_power = ("{}")'.format(calc)
						self.c.execute(query) 

					elif state == 'on-spring-break🍹': 
						## On spring break increases health by 500 
						query = 'UPDATE stats SET health = ("{}")'.format(calc)
						self.c.execute(query) 

					## increase stats based on weaponry and armors 
					# ARMOR 
					self.c.execute("SELECT armor FROM stats") 
					my_armor = self.c.fetchone()[0]
					if my_armor == 'shield':
						calc = curr_def+500
						query = 'UPDATE stats SET def_power = ("{}")'.format(calc)
						self.c.execute(query) 

					# WEAPON
					self.c.execute("SELECT weapon FROM stats") 
					my_weapon = self.c.fetchone()[0]

					if my_weapon == 'pick-axe':
						calc = curr_atk+30
						query = 'UPDATE stats SET atk_power = ("{}")'.format(calc)
						self.c.execute(query) 

					elif my_weapon == 'hammer🔨':
						calc = curr_atk+60
						query = 'UPDATE stats SET atk_power = ("{}")'.format(calc)
						self.c.execute(query) 

					elif my_weapon == 'sword': 
						calc = curr_atk+100
						query = 'UPDATE stats SET atk_power = ("{}")'.format(calc)
						self.c.execute(query) 

					elif my_weapon == 'bow🏹':
						calc = curr_atk+200
						query = 'UPDATE stats SET atk_power = ("{}")'.format(calc)
						self.c.execute(query) 

					elif my_weapon == 'dagger🗡':
						calc = curr_atk+300
						query = 'UPDATE stats SET atk_power = ("{}")'.format(calc)
						self.c.execute(query) 

					elif my_weapon == 'claw':
						calc = curr_atk+350
						query = 'UPDATE stats SET atk_power = ("{}")'.format(calc)
						self.c.execute(query) 

					elif my_weapon == 'spear': 
						calc = curr_atk+400
						query = 'UPDATE stats SET atk_power = ("{}")'.format(calc)
						self.c.execute(query) 


					elif my_weapon == 'crossbow':
						calc = curr_atk+450
						query = 'UPDATE stats SET atk_power = ("{}")'.format(calc)
						self.c.execute(query) 

					elif my_weapon == 'wand': 
						calc = curr_atk+1000
						query = 'UPDATE stats SET atk_power = ("{}")'.format(calc)
						self.c.execute(query) 
					
					print("Type 'flee' at any point during the battle to stop fighting.")

					print("You may only use the skills double-attack and/or triple-attack once per battle.")
					print("The triple-attack skills lowers your health by 100, and the double-attack skill")
					print("lowers your health by 50.")

					# begin battle code
					print("╔╗ ╔═╗╔╦╗╔╦╗╦  ╔═╗  ╔╗ ╔═╗╔═╗╦╔╗╔") 
					print("╠╩╗╠═╣ ║  ║ ║  ║╣   ╠╩╗║╣ ║ ╦║║║║")
					print("╚═╝╩ ╩ ╩  ╩ ╩═╝╚═╝  ╚═╝╚═╝╚═╝╩╝╚╝") 
		 
					## monster: monster_health, monster_def, monster_atk, monster_id, monster_name
					## me: curr_health, curr_def, curr_atk, curr_exp
					special_skill = False 
					won = False 

					while True:
						#  get all the information from the monster 
						## attack: choose skill to use
						print("Possible skills are attack, guard, double-attack, triple-attack,heal.")
						my_skill = str(input("Choose a skill to use : "))

						if my_skill == 'attack':
							curr_atk = curr_atk + 80 + .2*curr_exp

						elif my_skill == 'guard':
							curr_def = curr_def + 80 + .2*curr_exp

						elif my_skill == 'double-attack':
							if special_skill == False:
								curr_atk = curr_atk + 100 + .2*curr_exp
								special_skill = True
							else:
								print("You've already used a special skill once this battle.")
								my_skill = 'none' 


						elif my_skill == 'triple-attack': 
							if special_skill == False:
								curr_atk = curr_atk + 150 + .2*curr_exp
								special_skill = True
							else:
								print("You've already used a special skill once this battle.")
								my_skill = 'none' 

						elif my_skill == 'heal':
							curr_health = curr_health + 30 + .2*curr_exp

						else:
							print("Not a valid skill.")
							my_skill = 'none' 

						## attack: increase power of skill by attack_power and experience 
						damage_dealt = curr_atk + .2*curr_exp + monster_def*.5 
						monster_health = monster_health - damage_dealt 
						print("You attack the {} using skill {}, dealing {} damage.".format(monster_name,my_skill,damage_dealt)) 
						if monster_health <= 0:
							print("{} has died. You've won the battle.".format(monster_name))
							won = True 
							break 
						else:
							print("{} has health {} now.".format(monster_name,monster_health))

						## defend: protect yourself against monster attack with defense 
						damage_suffered = monster_atk + .5*curr_def + .2*curr_exp
						print("{} attacks you, dealing {} damage".format(monster_name,damage_suffered)) 
						curr_health = curr_health - damage_suffered
						if curr_health <= 0:
							print("You've died and lost the battle.")
							break 
						else: 
							print("You have health {} now.".format(curr_health)) 
						
						## update:
						## now subtract the temporary stat boost from the chosen skill for this round 
						if my_skill == 'attack':
							curr_atk = curr_atk - 80 - .5*curr_exp

						elif my_skill == 'guard':
							curr_def = curr_def - 80 - .5*curr_exp

						elif my_skill == 'double-attack':
							if special_skill == False:
								curr_atk = curr_atk - 100 - .5*curr_exp
								special_skill = True
								curr_health = curr_health - 50 
							else:
								print("You've already used a special skill once this battle.")


						elif my_skill == 'triple-attack': 
							if special_skill == False:
								curr_atk = curr_atk - 150 - .5*curr_exp
								special_skill = True
								curr_health = curr_health - 100 
							else:
								print("You've already used a special skill once this battle.")

						elif my_skill == 'heal':
							curr_health = curr_health - 30 - .5*curr_exp 
	
				   
					print("╔╗ ╔═╗╔╦╗╔╦╗╦  ╔═╗  ╔═╗╔╗╔╔╦╗")
					print("╠╩╗╠═╣ ║  ║ ║  ║╣   ║╣ ║║║ ║║")
					print("╚═╝╩ ╩ ╩  ╩ ╩═╝╚═╝  ╚═╝╝╚╝═╩╝")
					# end battle code 

					# collect loot 
					if won == True:
						# if monster dies then delete it from the room  
						query = 'DELETE FROM mobs WHERE room_id=("{}")'.format(self.current_room)
						self.c.execute(query)
						# increase experience 
						calc = curr_exp + monster_exp
						query = 'UPDATE stats SET exp = ("{}")'.format(calc)
						self.c.execute(query) 
						print("You've gained {} experience.".format(monster_exp)) 
					else:
						# New state is dead🤯
						query = 'UPDATE stats SET state = ("{}")'.format("dead🤯")
						self.c.execute(query) 
						print("Your new state is dead🤯.")

					# set stats back to normal from boost (weapon;armor;state)
					if my_weapon == 'pick-axe':
						calc = curr_atk-30
						query = 'UPDATE stats SET atk_power = ("{}")'.format(calc)
						self.c.execute(query) 

					elif my_weapon == 'hammer🔨':
						calc = curr_atk-60
						query = 'UPDATE stats SET atk_power = ("{}")'.format(calc)
						self.c.execute(query) 

					elif my_weapon == 'sword': 
						calc = curr_atk-100
						query = 'UPDATE stats SET atk_power = ("{}")'.format(calc)
						self.c.execute(query) 

					elif my_weapon == 'bow🏹':
						calc = curr_atk-200
						query = 'UPDATE stats SET atk_power = ("{}")'.format(calc)
						self.c.execute(query) 

					elif my_weapon == 'dagger🗡':
						calc = curr_atk-300
						query = 'UPDATE stats SET atk_power = ("{}")'.format(calc)
						self.c.execute(query) 

					elif my_weapon == 'claw':
						calc = curr_atk-350
						query = 'UPDATE stats SET atk_power = ("{}")'.format(calc)
						self.c.execute(query) 

					elif my_weapon == 'spear': 
						calc = curr_atk-400
						query = 'UPDATE stats SET atk_power = ("{}")'.format(calc)
						self.c.execute(query) 


					elif my_weapon == 'crossbow':
						calc = curr_atk-450
						query = 'UPDATE stats SET atk_power = ("{}")'.format(calc)
						self.c.execute(query) 

					elif my_weapon == 'wand': 
						calc = curr_atk-1000
						query = 'UPDATE stats SET atk_power = ("{}")'.format(calc)
						self.c.execute(query) 

			else:
				print("unknown command {}".format(words[0]))

		# all done, clean exit
		print("------------------------------------------------------------------------------------------------")
		self.db.commit()
		self.db.close()

	# describe this room and its exits
	def doLook(self,force_florid):
		# We show the florid description only the first time we visit
		# a room, or if someone types "look" explicitly
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
					monster = str(self.c.fetchone()[0])
					print("There's a {} in this room (ง •̀_•́)ง ".format(monster))
					## print description of monster 
					query = 'SELECT description FROM monster_desc WHERE name = ("{}")'.format(monster)
					self.c.execute(query)
					desc = str(self.c.fetchone()[0])
					print("    " + desc)
					query = 'SELECT health FROM monster_desc WHERE name = ("{}")'.format(monster)
					self.c.execute(query)
					monster_health = str(self.c.fetchone()[0])
					print("    Health: " + monster_health)
					query = 'SELECT atk_power FROM monster_desc WHERE name = ("{}")'.format(monster)
					self.c.execute(query)
					monster_atk = str(self.c.fetchone()[0])
					print("    Attack_power : " + monster_atk)
					query = 'SELECT def_power FROM monster_desc WHERE name = ("{}")'.format(monster)
					self.c.execute(query)
					monster_def = str(self.c.fetchone()[0])
					print("    Defense_power : " + monster_def)
					query = 'SELECT exp FROM monster_desc WHERE name = ("{}")'.format(monster)
					self.c.execute(query)
					monster_def = str(self.c.fetchone()[0])
					print("    Exp : " + monster_def)

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
					monster = str(self.c.fetchone()[0])  
					print("There's a {} in this room (ง •̀_•́)ง".format(monster)) 
					## print description of monster 
					query = 'SELECT description FROM monster_desc WHERE name = ("{}")'.format(monster)
					self.c.execute(query)
					desc = str(self.c.fetchone()[0])
					print("    " + desc)
					query = 'SELECT health FROM monster_desc WHERE name = ("{}")'.format(monster)
					self.c.execute(query)
					monster_health = str(self.c.fetchone()[0])
					print("    Health: " + monster_health)
					query = 'SELECT atk_power FROM monster_desc WHERE name = ("{}")'.format(monster)
					self.c.execute(query)
					monster_atk = str(self.c.fetchone()[0])
					print("    Attack_power : " + monster_atk)
					query = 'SELECT def_power FROM monster_desc WHERE name = ("{}")'.format(monster)
					self.c.execute(query)
					monster_def = str(self.c.fetchone()[0])
					print("    Defense_power : " + monster_def)
					query = 'SELECT exp FROM monster_desc WHERE name = ("{}")'.format(monster)
					self.c.execute(query)
					monster_def = str(self.c.fetchone()[0])
					print("    Exp : " + monster_def)


		## Give the full-description since force-florid is switched on. 
		else: 
			self.c.execute("SELECT florid_desc FROM rooms WHERE id={}".format(self.current_room))
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
				monster = str(self.c.fetchone()[0]) 
				print("There's a {} in this room (ง •̀_•́)ง ".format(monster))
				## print description of monster 
				query = 'SELECT description FROM monster_desc WHERE name = ("{}")'.format(monster)
				self.c.execute(query)
				desc = str(self.c.fetchone()[0]) 
				print("    " + desc)
				query = 'SELECT health FROM monster_desc WHERE name = ("{}")'.format(monster)
				self.c.execute(query)
				monster_health = str(self.c.fetchone()[0])
				print("    Health: " + monster_health)
				query = 'SELECT atk_power FROM monster_desc WHERE name = ("{}")'.format(monster)
				self.c.execute(query)
				monster_atk = str(self.c.fetchone()[0])
				print("    Attack_power : " + monster_atk)
				query = 'SELECT def_power FROM monster_desc WHERE name = ("{}")'.format(monster)
				self.c.execute(query)
				monster_def = str(self.c.fetchone()[0])
				print("    Defense_power : " + monster_def)
				query = 'SELECT exp FROM monster_desc WHERE name = ("{}")'.format(monster)
				self.c.execute(query)
				monster_def = str(self.c.fetchone()[0])
				print("    Exp : " + monster_def)

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

	# locate item in item table
	def useItem(self,name):
		## my_stats: health,state,weapon,armor,class,atk_power,def_power,exp,guild,gold
		self.c.execute("SELECT health from stats")
		curr_health = int(self.c.fetchone()[0]) 
		self.c.execute("SELECT atk_power from stats")
		curr_atk = int(self.c.fetchone()[0]) 
		self.c.execute("SELECT def_power from stats")
		curr_def = int(self.c.fetchone()[0]) 
		self.c.execute("SELECT exp from stats")
		curr_exp = int(self.c.fetchone()[0]) 
		self.c.execute("SELECT gold from stats")
		curr_gold = int(self.c.fetchone()[0]) 
					
		## we must check that item is in user's inventory before calling this function 
		if name == 'plain-chest':
			calc = curr_gold+100
			query = 'UPDATE stats SET gold = ("{}")'.format(calc)
			self.c.execute(query) 
			print("Your gold has increased by 100.")

		elif name == 'golden-chest':
			calc = curr_gold+500
			query = 'UPDATE stats SET gold = ("{}")'.format(calc)
			self.c.execute(query) 
			print("Your gold has increased by 500.")

		elif name == 'mini-chest': 
			calc = curr_gold+10
			query = 'UPDATE stats SET gold = ("{}")'.format(calc)
			self.c.execute(query) 
			print("Your gold has increased by 10.")

		elif name == 'steel-chest':
			calc = curr_gold+200
			query = 'UPDATE stats SET gold = ("{}")'.format(calc)
			self.c.execute(query) 
			print("Your gold has increased by 200.")

		elif name == 'mana-crystal':
			calc = curr_health+300
			query = 'UPDATE stats SET health = ("{}")'.format(calc)
			self.c.execute(query) 
			print("Your health has increased by 300.")

		elif name == 'potion':
			calc = curr_health+100
			query = 'UPDATE stats SET health = ("{}")'.format(calc)
			self.c.execute(query) 
			print("Your health has increased by 100.")

		elif name == 'blue-book📘':
			calc = curr_exp+50 
			query = 'UPDATE stats SET exp = ("{}")'.format(calc)
			self.c.execute(query) 
			print("Your experience has increased by 50.")

		elif name == 'green-book📗':
			calc = curr_exp+100
			query = 'UPDATE stats SET exp = ("{}")'.format(calc)
			self.c.execute(query) 
			print("Your experience has increased by 100.")

		elif name == 'orange-book📙':
			calc = curr_exp+300
			query = 'UPDATE stats SET exp = ("{}")'.format(calc)
			self.c.execute(query) 
			print("Your experience has increased by 300.")

		elif name == 'tome📖':
			calc = curr_exp+1000
			query = 'UPDATE stats SET exp = ("{}")'.format(calc)
			self.c.execute(query)
			print("Your experience has increased by 1000.")

		elif name == 'apple🍎':
			calc = curr_health+100
			query = 'UPDATE stats SET health = ("{}")'.format(calc)
			self.c.execute(query) 
			print("Your health has increased by 100.")

		elif name == 'beer🥃':
			calc = curr_health+250
			query = 'UPDATE stats SET health = ("{}")'.format(calc)
			self.c.execute(query) 
			print("Your gold has increased by 250.")

		elif name == 'ramen🍜':
			calc = curr_health+70
			query = 'UPDATE stats SET health = ("{}")'.format(calc)
			self.c.execute(query) 
			print("Your gold has increased by 70.")

		elif name == 'ISS🛰':
			calc = curr_atk+10000000
			query = 'UPDATE stats SET atk_power = ("{}")'.format(calc)
			self.c.execute(query) 
			print("Your attack power has increased by 10000000.")

		elif name == 'wheat🌾':
			calc = curr_health+50
			query = 'UPDATE stats SET health = ("{}")'.format(calc)
			self.c.execute(query) 
			print("Your health has increased by 50.")

		elif name == 'herb🌿':
			calc = curr_health+80
			query = 'UPDATE stats SET health = ("{}")'.format(calc)
			self.c.execute(query) 
			print("Your health has increased by 80.")
			#self.c.execute("SELECT health from stats")
			#curr_health = int(self.c.fetchone()[0]) 

		elif name == 'mushroom🍄':
			calc = curr_health-10000
			query = 'UPDATE stats SET health = ("{}")'.format(calc)
			self.c.execute(query) 
			print("Your health has decreased by 10000.")

		elif name == 'bed🛌':
			calc = curr_health+500
			query = 'UPDATE stats SET health = ("{}")'.format(calc)
			self.c.execute(query) 
			print("Your health has increased by 500.")

		elif name == 'revival-dove🕊': 
			## should change state from dead to normal 
			self.c.execute("SELECT state from stats")
			curr_state = str(self.c.fetchone()[0]) 
			if curr_state == "dead🤯":
				query = 'UPDATE stats SET state = ("{}")'.format("normal")
				self.c.execute(query) 
				print("Your state has changed from dead🤯 to normal.")
			else: 
				print("You are not dead. Oh well. Looks like the revival-dove🕊 is gone now.")


		elif name == 'grapes🍇':
			calc = curr_health+860
			query = 'UPDATE stats SET health = ("{}")'.format(calc)
			self.c.execute(query) 
			print("Your health has increased by 860.")

		elif name == 'banana🍌':
			calc = curr_health-250
			query = 'UPDATE stats SET health = ("{}")'.format(calc)
			self.c.execute(query) 
			print("Your health has decreased by 250.")

		elif name == 'watermelon🍉':
			calc = curr_health+450
			query = 'UPDATE stats SET health = ("{}")'.format(calc)
			self.c.execute(query) 
			print("Your health has increased by 450.")

		elif name == 'peach🍑 ':
			calc = curr_health+60
			query = 'UPDATE stats SET health = ("{}")'.format(calc)
			self.c.execute(query) 
			print("Your health has increased by 60.")

		elif name == 'cherry🍒':
			calc = curr_health+350
			query = 'UPDATE stats SET health = ("{}")'.format(calc)
			self.c.execute(query) 
			print("Your health has increased by 350.")

		elif name == 'strawberry🍓':
			calc = curr_health+50
			query = 'UPDATE stats SET health = ("{}")'.format(calc)
			self.c.execute(query) 
			print("Your health has increased by 50.")

		elif name == 'kiwi🥝':
			calc = curr_health+75
			query = 'UPDATE stats SET health = ("{}")'.format(calc)
			self.c.execute(query) 
			print("Your health has increased by 75.")

		elif name == 'corn🌽':
			calc = curr_health+30
			query = 'UPDATE stats SET health = ("{}")'.format(calc)
			self.c.execute(query) 
			print("Your health has increased by 30.")

		elif name == 'chinese-takeout🥡':
			calc = curr_health-250
			query = 'UPDATE stats SET health = ("{}")'.format(calc)
			self.c.execute(query) 
			calc = curr_atk+300
			query = 'UPDATE stats SET atk_power = ("{}")'.format(calc)
			self.c.execute(query) 
			print("Your health has decreased by 250, but your attack-power has increased by 300.")

		elif name == 'salt-and-straw-icecream🍨':
			calc = curr_health+1000
			query = 'UPDATE stats SET health = ("{}")'.format(calc)
			self.c.execute(query) 
			print("Your health has increased by 1000.")

		elif name == 'grandmas-pie🥧':
			calc = curr_health+500
			query = 'UPDATE stats SET health = ("{}")'.format(calc)
			self.c.execute(query) 
			print("Your health has increased by 500.")

		elif name == 'honey🍯':
			calc = curr_health+150
			query = 'UPDATE stats SET health = ("{}")'.format(calc)
			self.c.execute(query) 
			print("Your health has increased by 150.")

		elif name == 'tea🍵 ':
			calc = curr_health+40 
			query = 'UPDATE stats SET health = ("{}")'.format(calc)
			self.c.execute(query) 
			print("Your health has increased by 40.")

		elif name == 'wine🍷 ':
			calc = curr_health+500
			query = 'UPDATE stats SET health = ("{}")'.format(calc)
			self.c.execute(query) 
			print("Your health has increased by 500.")

		elif name == 'amphora-of-the-ancients🏺':
			## Join the Guild-of-The-Ancients
			self.c.execute("SELECT guild from stats") 
			if (self.c.fetchone()[0] == 'none'):
				print("You have joined the Guild of the Ancients !")
				print("As a welcome gift, you have received volcanic-mountain🌋, bow🏹 ,dagger🗡, candle🕯, revival-dove🕊, grapes🍇, and tome📖.")
				query = 'UPDATE stats SET guild = ("{}")'.format("Guild-of-the-Ancients")
				self.c.execute(query) 

				# Welcome pack: volcanic-mountain🌋,bow🏹 , dagger🗡, candle🕯,revival-dove🕊,grapes🍇, and tome📖.
				query = 'INSERT INTO inventory (name) VALUES ("{}")'.format("volcanic-mountain🌋")
				self.c.execute(query) 
				query = 'INSERT INTO inventory (name) VALUES ("{}")'.format("bow🏹")
				self.c.execute(query) 
				query = 'INSERT INTO inventory (name) VALUES ("{}")'.format("dagger🗡")
				self.c.execute(query) 
				query = 'INSERT INTO inventory (name) VALUES ("{}")'.format("candle🕯")
				self.c.execute(query) 
				query = 'INSERT INTO inventory (name) VALUES ("{}")'.format("revival-dove🕊")
				self.c.execute(query) 
				query = 'INSERT INTO inventory (name) VALUES ("{}")'.format("grapes🍇")
				self.c.execute(query) 
				query = 'INSERT INTO inventory (name) VALUES ("{}")'.format("tome📖")
				self.c.execute(query) 

				# New class is `priest`.
				query = 'UPDATE stats SET class = ("{}")'.format("mage")
				self.c.execute(query) 
				print("Your new class is priest.")

				# New state is `cat😼`. 
				query = 'UPDATE stats SET state = ("{}")'.format("cat😼")
				self.c.execute(query) 
				print("Your new state is cat 😼.")

		elif name == 'the-world🌍':
			calc = curr_def+10000
			query = 'UPDATE stats SET def_power = ("{}")'.format(calc)
			self.c.execute(query) 
			print("Your defense power has increased by 10000.")

		elif name == 'paradise-island🏝':
			calc = curr_health+12000
			query = 'UPDATE stats SET health = ("{}")'.format(calc)
			self.c.execute(query) 
			print("Your health has increased by 12000.")

		elif name == 'Athens🏛':
			## join Guild-of-Champions 🏆
			self.c.execute("SELECT guild from stats") 
			if (self.c.fetchone()[0] == 'none'):
				print("You have joined the Guild of the Champions!")
				print("As a welcome gift, you have received the-world🌍, the-Federal-Reserve🏦,ISS🛰,paradise-island🏝,and the-american-dream🏠.")
				query = 'UPDATE stats SET guild = ("{}")'.format("Guild-of-the-Champions")
				self.c.execute(query) 

				# Welcome pack: the-world 🌍, the-Federal-Reserve 🏦, ISS🛰, paradise-island🏝, and the-american-dream🏠.
				query = 'INSERT INTO inventory (name) VALUES ("{}")'.format("the-world🌍")
				self.c.execute(query)
				query = 'INSERT INTO inventory (name) VALUES ("{}")'.format("the-Federal-Reserve🏦")
				self.c.execute(query) 
				query = 'INSERT INTO inventory (name) VALUES ("{}")'.format("ISS🛰")
				self.c.execute(query) 
				query = 'INSERT INTO inventory (name) VALUES ("{}")'.format("paradise-island🏝")
				self.c.execute(query) 
				query = 'INSERT INTO inventory (name) VALUES ("{}")'.format("the-american-dream🏠")
				self.c.execute(query) 

				# New class is `warrior`.
				query = 'UPDATE stats SET class = ("{}")'.format("warrior")
				self.c.execute(query) 
				print("Your new class is warrior.")

				# New state is `immortal😎`. 
				query = 'UPDATE stats SET state = ("{}")'.format("immortal😎")
				self.c.execute(query) 
				print("Your new state is immortal😎.")

		elif name == 'the-american-dream🏠':
			calc = curr_gold+50000
			query = 'UPDATE stats SET gold = ("{}")'.format(calc)
			self.c.execute(query) 
			print("Your gold has increased by 50000.")

		elif name == 'the-Federal-Reserve🏦':
			calc = curr_gold+500000
			query = 'UPDATE stats SET gold = ("{}")'.format(calc)
			self.c.execute(query) 
			print("Your gold has increased by 500000.")

		elif name == 'hospital🏥':
			calc = curr_health+10000
			query = 'UPDATE stats SET health = ("{}")'.format(calc)
			self.c.execute(query) 
			print("Your gold has increased by 10000.")

		elif name == 'money-bag💰':
			calc = curr_gold+100000
			query = 'UPDATE stats SET gold = ("{}")'.format(calc)
			self.c.execute(query) 
			print("Your gold has increased by 100000.")


		## remove this item from our inventory now 
		query = 'DELETE FROM inventory'.format(name)
		self.c.execute(query)

	# build the monster description table 
	def buildMonsterTable(self):
		## populate the monster table with our monster descriptions and stats
		# minotaur 
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('minotaur',160,'Wait a second! I thought Theseus killed the Minotaur? Oh well. No point in debating it—that is definitely a minotaur, & he looks eager to fight!',200,100,90)
		self.c.execute(query)

		# orc
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('orc',500,'This creature wandered all the way from Middle-Earth just to try and kill you. How nice!',1000,300,300)
		self.c.execute(query) 

		# plant
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('plant',40,'Show this plant the meaning of Darwinian selection. Survival of the fittest!!',50,0,30)
		self.c.execute(query)

		# rat
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('rat',100,'Hmmm. It is a rat.',30,100,50)
		self.c.execute(query)

		# ogre
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('ogre',1000,'Looks like the Ogre from the Three Broomsticks has appeared, and he is here to spoil the ending of the next Harry Potter book. Better kill him before he does that.',200,100,90)
		self.c.execute(query)

		# scorpion
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('scorpion',300,'Scorpionssssssss are sssssuppppppeeeerrrr scary.',500,10,40)
		self.c.execute(query)

		# skeleton
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('skeleton',100,'Send this guy back to the grave!',850,40,200)
		self.c.execute(query)

		# giant-ant🐜
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('giant-ant🐜',20,'This forager is out for blood.',10000,0,400)
		self.c.execute(query)

		# bat🦇
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('bat🦇',50,'Oooo, bats are spooky. Do you not think battling a bat is a perfect way to spend the fall semester?',200,30,50)
		self.c.execute(query)

		# slime
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('slime',100,'This monster looks a bit like jello. Or play-doh. Or transparent clay. You get it. It is slime.',0,400,134)
		self.c.execute(query)

		# snake🐍
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('snake🐍',160,'Cmon, get ready to fight and send this snake back to the garden he came from!',200,100,90)
		self.c.execute(query)
	

		# werewolf
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('werewolf',800,'Not sure why this werewolf is out on a night like this. No full moon in sight. Anyway, he is here, and it is probably a good idea to get your weapon out.',400,450,200)
		self.c.execute(query)

		# zombie
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('zombie',1000,'Yeah, zombiess are creepy, but he just wants a hug. Scary, but harmless.',0,100,60)
		self.c.execute(query)

		# vampire
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('vampire',1000,'By day, he is a vampire. By night, he works the night shift in the blood donation center. No one has ever determined how he has managed to come by so much blood . . . ',800,340,200)
		self.c.execute(query)

		# chimera
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('chimera',450,'Is it too cheesy to suggest this monster might just be chimerical? Even the stats are suspect.',450,450,450)
		self.c.execute(query)

		# cerberus
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('cerberus',430,'I do not think you can deal with a three-headed monster. You cannot even deal with a one-headed monster.',10000,330,240)
		self.c.execute(query)

		# spider
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('spider',50,'It is a creepy spider and you do not like it.',200,100,10)
		self.c.execute(query)

		# ghost
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('ghost',100,'One moment, he is there. The next, he is...where did he go?!',300,100000,500)
		self.c.execute(query)

		# taco🌮
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('taco🌮',1000,' You want to fight the taco, but you also kinda wanna eat it. Friend or foe? Combat opponent or...lunch?',400,0,340)
		self.c.execute(query)

		# fairy🧚‍
		query = 'INSERT INTO  monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('fairy🧚‍',500,'Do not underestimate her tiny size.',700,40,600)
		self.c.execute(query)

		# dragon🐉
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('dragon🐉',10000,'There be dragons.',1000,800,480)
		self.c.execute(query)

		# dinosaur-of-yore🦕
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('dinosaur-of-yore🦕',160,'Show this dinosaur there is a reason his species went extinct! Send him back to yore, o noble adventurer.',200,100,230)
		self.c.execute(query)

		# bee-of-disproportionate-size🐝
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('bee-of-disproportionate-size🐝',700,'It is what it sounds like.',12,32,100)
		self.c.execute(query)

		# mostly-friendly-wolf🐺
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('mostly-friendly-wolf🐺',100,'I do not want to encounter this guy when he is mostly unfriendly.',300,100,200)
		self.c.execute(query)

		# pineapple🍍
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('pineapple🍍',800,'You have encountered a pineapple. Yellow, large, and let us be honest: it is super spikey. A fearsome opponent.',200,100,260)
		self.c.execute(query)

		# kleptomaniac-squirrel-of-doom🐿
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('kleptomaniac-squirrel-of-doom🐿',1000,'You have encountered the squirrel of doom. I hate to be the bearer of bad news, but this is the end for you, truly. Unless you happen to have an acorn in your inventory, the inevitable is coming. Let us just say there is a reason this little guy is called the kleptomaniac squirrel of doom.',100,10000000000,90)
		self.c.execute(query)

		# the-great-mage🧙‍ 
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('the-great-mage🧙‍',10000,'Best to flee. A learned mage is a fearsome contender.',1000,1000,40)
		self.c.execute(query)

		# apprentice🧙‍
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('apprentice🧙‍',5000,'He wants to be more like the great mage and less like himself.',400,300,150)
		self.c.execute(query)

		# merman🧜
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('merman🧜',300,'Maybe we can distract him with a mermaid?',800,140,270)
		self.c.execute(query)

		# elf🧝
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('elf🧝',400,'Looks like Orlando Bloom.',400,200,300)
		self.c.execute(query)

		# unicorn🦄
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('unicorn🦄',500,'She is shiny, she is pink, and she is going to knock you down with that horn unless you pull yourself out of your stupor and fight.',800,200,100)
		self.c.execute(query)

		# owl🦉
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('owl🦉',160,'OooooooooOOOOOOOOooooooooooooooooo',200,100,90)
		self.c.execute(query)

		# whale🐳
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('whale🐳',300,'He is blowing bubbles to tease you. It is all fun and games until it is not fun and games.',400,100,240)
		self.c.execute(query)

		# dolphin🐬
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('dolphin🐬',400,'Awwww, it is a dolphin.',200,100,90)
		self.c.execute(query)

		# magical-fish-out-of-water🐟
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('magical-fish-out-of-water🐟',30,'What disturbs you more than seeing a fish out of water is seeing an alive fish out of water.',0,100,90)
		self.c.execute(query)

		# blowfish🐡
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('blowfish🐡',150,' Let us call him squishy.',400,200,180)
		self.c.execute(query)

		# octopus🐙
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('octopus🐙',300,' It seems like an octopus could find a better occupation than monster. He could be a party planner or master organizer, for example.',80,120,50)
		self.c.execute(query)

		# caterpillar-of-phenomenal-power🐛
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('caterpillar-of-phenomenal-power🐛',100,'This caterpillar is phenomenally powerful; you can feel it from afar.',20000,30,400)
		self.c.execute(query)

		# zombie🧟
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('zombie🧟',300,'Enjoy your undead status while you still can.',240,230,220)
		self.c.execute(query)

		# monarch-butterfly🦋
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('monarch-butterfly🦋',50,'Yes, butterflies have numbered days and do not live for long. Do not feel too bad; your days are numbered too.',30,10,30)
		self.c.execute(query)

		# evil-shrimp🦐
		query = 'INSERT INTO  monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('evil-shrimp🦐',200,'He has malicious intentions. Shrimp always do.',200,70,90)
		self.c.execute(query)

		# alien🛸
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('alien🛸',160,'Please be a conspiracy theory. Please be a conspiracy theory! You are not supposed to be real!',700,300,550)
		self.c.execute(query)

		# time⏱
		query = 'INSERT INTO  monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('time⏱',100,'Our greatest enemy. We will see how true it is that you cannot be conquered.',1000,0,1000)
		self.c.execute(query)

		# bad-weather⛈
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('bad-weather⛈',100,'Humans should be able to control the weather.',40,10,35)
		self.c.execute(query)

		# god-of-north-wind🌬
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('god-of-north-wind🌬',250,'He is kinda beautiful, but he keeps blowing a chilly breeze your way. You forgot to bring a sweater, so you are not going to tolerate that kind of behavior.',200,100,300)
		self.c.execute(query)

		# umbrella🌂
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('umbrella🌂',600,'An umbrella; it is notoriously hard to open. And to close.',200,0,500)
		self.c.execute(query)

		# fire🔥
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('fire🔥',200,'Stop, drop and roll.',460,0,200)
		self.c.execute(query)

		# jack-o-lantern🎃
		query = 'INSERT INTO monster_desc (name,health,description,atk_power,def_power,exp) VALUES ("{}",{},"{}",{},{},{})'.format('jack-o-lantern🎃',200,'He is smirking at you. Go get him.',30,200,45)
		self.c.execute(query)
	

																										

	def buildItemTable(self): 
		# query = 'INSERT INTO exits (from_room, to_room, dir) VALUES ({}, {}, "{}")'.format(new_room_id, entrance_p[0],"w")
		# self.c.execute(query)
		# plain-chest

		query = 'INSERT INTO item_desc (name, description) VALUES ("{}", "{}")'.format("plain-chest", "Well it is better than nothing. Right?!")
		self.c.execute(query)

		# golden-chest
		query = 'INSERT INTO item_desc (name, description) VALUES ("{}", "{}")'.format("golden-chest","The best chest there is.")
		self.c.execute(query)

		# steel-chest
		query = 'INSERT INTO item_desc (name, description) VALUES ("{}", "{}")'.format('steel-chest','Seems like it might be hard to open.')
		self.c.execute(query)

		# mini-chest
		query = 'INSERT INTO item_desc (name, description) VALUES ("{}", "{}")'.format('mini-chest','Just because it is tiny does not mean it is worthless. Oh, well, actually...')
		self.c.execute(query)

		# mana-crystal
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('mana-crystal','Use this to increase your health by +300.')
		self.c.execute(query)

		# pick-axe
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('pick-axe','A great medieval weapon. Which would be perfect, if you were living in medieval times. You are not.')
		self.c.execute(query)

		# potion
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('potion','No, this potion does not come up with an ingredient list, silly. Just drink it or leave it.')
		self.c.execute(query)

		# blue-book📘
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('blue-book📘','It is not perfect, but you suspect this blue book is better than the red book.')
		self.c.execute(query)

		# green-book📗
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('green-book📗','Seriously, it is better than the red book. I think.')
		self.c.execute(query)

		# orange-book📙
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('orange-book📙','The red book does not even exist, ok? But this book exists. It might help you. ')
		self.c.execute(query)

		# tome 📖
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('tome📖','Um, are you sure you want to read this? It looks long.')
		self.c.execute(query)

		# ring
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('ring','This does not do anything, but it is shiny. Maybe bring it just in case a lovely lady comes along?')
		self.c.execute(query)

		# shield 
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('shield','The only shield available in this game, because the creator wants to abandon you in a dungeon of monsters with only one piece of armor available. What could go wrong?')
		self.c.execute(query)

		# crystal
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('crystal','Use this to spawn any type of monster you want. Maybe it does not make sense to you why a crystal would spawn a monster. Stop trying to figure everything out, kid.')
		self.c.execute(query)

		# crown-of-awesome👑
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('crown-of-awesome👑','Has absolutely no useful value, but, let us face it: it is awesome. Is not the awe-inspiring, effusive, magnificent power of awesome enough for you? ')
		self.c.execute(query)

		# apple🍎
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('apple🍎','An apple a day, they say...')
		self.c.execute(query)

		# beer🥃
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('beer🥃','End the day with some cold beer, and your problems will disappear. Just kidding. But. It tastes good.')
		self.c.execute(query)

		# ramen🍜
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('ramen🍜','A primary food group.')
		self.c.execute(query)

		# ISS🛰
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('ISS🛰','We do not know what this is doing here. Should not the International Space Station be...in space?')
		self.c.execute(query)

		# tent⛺️
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('tent⛺️','If everything is going wrong, you can always hide in this tent.')
		self.c.execute(query)

		# crystal-ball🔮
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('crystal-ball🔮','This ball shows you the future. Not just of your life, but of the entire cosmos. So yes, you can ask the crystal ball questions about the nature of time, but there are also pressing questions you can ask, like: what is for dinner?')
		self.c.execute(query)

		# portal🌀
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('portal🌀','Use this to teleport at will to any room. As long as you have the room id, that is.')
		self.c.execute(query)

		# flower🌸
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('flower🌸','There is definitely something sinister about this flower. Might want to just put it down. Now back away.')
		self.c.execute(query)

		# wheat🌾
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('wheat🌾','An agricultural relic.')
		self.c.execute(query)

		# mushroom🍄
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('mushroom🍄',' I wonder if eating this mysterious, possibly toxic mushroom that you found in the middle of a dungeon would be a fun thing to do.')
		self.c.execute(query)

		# tulip🌷
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('tulip🌷','Flowers are pretty, but they do not do much. ')
		self.c.execute(query)

		# candle🕯
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('candle🕯','Very mysterious. ')
		self.c.execute(query)

		# bed🛌
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('bed🛌','Yawnnnn.')
		self.c.execute(query)

		# revival-dove🕊
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('revival-dove🕊','Revives a dead-person.')
		self.c.execute(query)

		# shell🐚
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('shell🐚','I wonder how a shell came to be in a dungeon. The other items make sense, but: a shell? That does not make sense. The Federal Reserve, maybe.')
		self.c.execute(query)

		# banana🍌
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('banana🍌','Yuck.')
		self.c.execute(query)

		# lemon🍋
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('lemon🍋','Too sour to eat. Maybe if you had some water? ')
		self.c.execute(query)

		# watermelon🍉
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('watermelon🍉','Watermelons are simply the best.')
		self.c.execute(query)

		# grapes🍇
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('grapes🍇','One taste of these grapes leads to instant Dionysian reverie. ')
		self.c.execute(query)

		# peach🍑
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('peach🍑','You are beautiful. Love, Peach.')
		self.c.execute(query)

		# cherry🍒
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('cherry🍒','Hello, daddy. Hello, mom. I am your ch-ch-ch-cherry bomb!')
		self.c.execute(query)

		# strawberry🍓
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('strawberry🍓','If you keep my secret I will give you this strawberry.')
		self.c.execute(query)

		# kiwi🥝
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('kiwi🥝',' Kiwi would be a cute name for a child, right? Anyway, this is not the child Kiwi. It is the fruit kiwi.')
		self.c.execute(query)

		# corn🌽
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('corn🌽','Some corn.')
		self.c.execute(query)

		# popcorn🍿
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('popcorn🍿','Do you think it is a good idea to have some popcorn and watch a movie in the middle of a dungeon rife with monsters? ')
		self.c.execute(query)

		# chinese-takeout🥡
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('chinese-takeout🥡',' Nothing says I-hate-cooking as much as some Chinese takeout.')
		self.c.execute(query)

		# salt-and-straw-icecream🍨
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('salt-and-straw-icecream🍨','Good thing you got this somehow. The lines are too long; there is no point in battling for ice cream when you have monsters to battle.')
		self.c.execute(query)

		# grandmas-pie🥧
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('grandmas-pie🥧','Smells good! Eat an entire pie by yourself.')
		self.c.execute(query)

		# honey🍯
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('honey🍯','Belongs to Pooh Bear. On temporary loan to Erebor dungeon.')
		self.c.execute(query)

		# tea🍵
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('tea🍵','You just know that the pretentious tea drinkers among us are going to kill us for not specifying the type of tea here. Oh well. Tea people are not exactly the most ferocious. I will take my chances.')
		self.c.execute(query)

		# wine🍷
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('wine🍷','Drink up, me hearties, yo ho!')
		self.c.execute(query)

		# amphora-of-the-ancients🏺
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('amphora-of-the-ancients🏺','There is writing on the outside of this amphora, but you cannot read Ancient Greek. ')
		self.c.execute(query)

		# the-world🌍
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('the-world🌍','It is so tiny, so round, so cute!!')
		self.c.execute(query)

		# volcanic-mountain🌋
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('volcanic-mountain🌋','You would prefer a chocolate lava, but hey.')
		self.c.execute(query)

		# paradise-island🏝
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('paradise-island🏝','What if you need a vacation, but your employer does not offer paid vacations? Use this paradise island in your inventory for an immediate escape')
		self.c.execute(query)

		# Athens🏛
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('Athens🏛','Some people love Greece so much they want to keep a relic of the Acropolis in their bag. Hey, to each to their own, right?')
		self.c.execute(query)

		# the-american-dream🏠
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('the-american-dream🏠','Hard to attain, harder to keep.')
		self.c.execute(query)

		# the-Federal-Reserve🏦
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('the-Federal-Reserve🏦','Wait a second: if the Federal Reserve is in your inventory, who is running the monetary system right now?! ')
		self.c.execute(query)

		# hospital🏥
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('hospital🏥','Why go to the hospital if you can keep one at all times in your bag?')
		self.c.execute(query)

		# statue-of-liberty🗽
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('statue-of-liberty🗽','Freedom is excellent, freedom is priceless. So do not be too disappointed that this statue does not do anything, k?')
		self.c.execute(query)

		# money-bag💰
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('money-bag💰','Not sure where this came from. It is best not to look into such things.')
		self.c.execute(query)

		# sword 
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('sword','A starter weapon.')
		self.c.execute(query)

		# bow🏹
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('bow🏹','You are obviously not Katniss, but it will still work. ')
		self.c.execute(query)

		# dagger🗡
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('dagger🗡','Great for stabbing friends (or political enemies) in the back. Et tu, Brute?')
		self.c.execute(query)

		# spear
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('spear','It is not a wand.')
		self.c.execute(query)

		# claw
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('claw','Nothing like a bear claw.')
		self.c.execute(query)

		# crossbow
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('crossbow','You will get the hang of it.')
		self.c.execute(query)

		# hammer🔨
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('hammer🔨','Probably better for fixing furniture.')
		self.c.execute(query)

		# wand
		query = 'INSERT INTO item_desc (name,description) VALUES ("{}", "{}")'.format('wand','Magic is, after all, the ultimate power.')
		self.c.execute(query)

	
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
			self.c.execute("DROP TABLE if exists item_desc") 
			self.c.execute("DROP TABLE if exists monster_desc")    
			shovel = False
			## API: rooms will keep track of the name of the loot item that they contain, if any 
			self.c.execute("CREATE TABLE rooms (id INTEGER PRIMARY KEY AUTOINCREMENT, short_desc TEXT, florid_desc TEXT, visit INTEGER, loot TEXT)")
			self.c.execute("CREATE TABLE mobs (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, health INTEGER,atk_power INTEGER,def_power INTEGER,exp INTEGER,room_id INTEGER)")
			self.c.execute("CREATE TABLE exits (from_room INTEGER, to_room INTEGER, dir TEXT)")
			# table for stats 
			self.c.execute("CREATE TABLE stats (health INTEGER,state TEXT,weapon TEXT,armor TEXT,class TEXT,atk_power INTEGER,def_power INTEGER,exp INTEGER,guild TEXT, gold INTEGER,status TEXT)")
			self.c.execute("INSERT INTO stats (health,state,weapon,armor,class,atk_power,def_power,exp,guild,gold,status) VALUES (100,'normal','none','none','hero',350,350,0,'none',50,'normal')")

			# table for loot items 
			self.c.execute("CREATE TABLE loot (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, des TEXT, available INTEGER)")
			# table for inventory 
			self.c.execute("CREATE TABLE inventory (name TEXT)")
			## create entrance
			self.c.execute("INSERT INTO rooms (florid_desc, short_desc,visit,loot) VALUES ('You are standing at the entrance of what appears to be a vast, complex cave.', 'entrance',0,'none')")

			# item description table
			self.c.execute("CREATE TABLE item_desc (name TEXT, description TEXT)")

			# monster description table
			self.c.execute("CREATE TABLE monster_desc (name TEXT, health INTEGER, description TEXT,atk_power INTEGER,def_power INTEGER,exp INTEGER)")

			## populate the item table
			self.buildItemTable() 

			## populate the monster description table 
			self.buildMonsterTable() 
		
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
	print("Type 'purchase' to use your gold to upgrade stats like health, atk_power, and def_power.")
	print("Type 'equip' to equip yourself with weapons and armor from your inventory.")
	d.repl()
