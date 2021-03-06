SQLite Dungeon
==============
<img src="https://66.media.tumblr.com/d471e4f3dee7aca7d07468ae89225edb/tumblr_ppnk1hKli51tk06jno1_540.jpg" align="right"> 
Adapted from <a href="https://github.com/dylanmc/SQLiteDungeon">Dylan's Dungeon</a> code from Spring 2019 Operating systems. 
Written in Python with SQLite3 as back-end. Image on right from RPG Maker VX with my character sprite in a designed dungeon map.  This dungeon has rooms and exits. You can <i>spawn</i> a monster, <i>place</i>  loot, <i>take</i>  loot, and engage in combat with the monsters inside the dungeon. You can <i>purchase</i> stats upgrades with gold, <i>equip</i> yourself with weapons and armors, <i>join</i> a guild for state and class changes and item bonuses. Users with a shovel in their inventory can <i>dig</i> rooms. Users with a <i>crystal</i> can spawn monsters.  There are <b>6</b> Guilds, <b>16</b> states, <b>6</b> classes,<b>5</b> skills, <b>40+</b> monsters, <b>50+</b> items, and <b>30+</b> rooms in the Erebor dungeon.  
Choosing a skill provides a temporary boost to your stats during the battle, and this boost is increased by 5% for every experience (exp) point you have. Similarly, the weapons you choose to equip provide a boost to your character. 

`Monsters:` minotaur, orc, plant, rat, ogre, scorpion, skeleton, giant-ant🐜 ,bat🦇,slime, snake🐍,werewolf, zombie, vampire, chimera, cerberus, spider, ghost,taco 🌮,fairy, dragon 🐉,
dinosaur-of-yore🦕, bee-of-disproportionate-size🐝, mostly-friendly-wolf🐺, pineapple🍍,
kleptomaniac-squirrel-of-doom🐿, the-great-mage, apprentice, merman🧜, elf🧝, unicorn🦄, owl🦉, whale🐳, dolphin🐬, magical-fish-out-of-water 🐟, blowfish 🐡, octopus 🐙, caterpillar-of-phenomenal-power🐛,zombie🧟, monarch-butterfly🦋, evil-shrimp🦐, alien🛸, time⏱, bad-weather⛈, god-of-north-wind 🌬, umbrella🌂, fire🔥, jack-o-lantern🎃

`Loot/Items:` plain-chest, golden-chest, steel-chest, mini-chest, potion, blue-book📘, green-book📗, orange-book📙, tome 📖, ring, herb, shield, crystal,crown-of-awesome👑, apple🍎, beer🥃, ramen🍜, ISS🛰 (the international space station), tent⛺️, crystal-ball🔮,portal🌀,flower🌸, wheat🌾, herb🌿, mushroom🍄, tulip🌷, beer🥃, 
candle🕯, bed🛌, revival-dove 🕊, shell 🐚, grapes 🍇,  banana 🍌, lemon 🍋, watermelon 🍉, peach🍑
cherry🍒, strawberry🍓, kiwi🥝, corn🌽, popcorn 🍿, chinese-takeout 🥡, salt-and-straw-icecream🍨, grandma's-pie 🥧, honey🍯, tea🍵, wine🍷, amphora-of-the-ancients🏺, the-world🌍, volcanic-mountain🌋, paradise-island🏝, 
Athens🏛 , the-american-dream🏠, the-Federal-Reserve🏦, hospital🏥, statue-of-liberty🗽, money-bag💰 

`Weapons:` sword, pick-axe,bow 🏹 ,dagger🗡,spear,claw,crossbow, hammer 🔨, wand

`Guilds:`  Guild-of-Mages, Guild-of-The-Dark-Arts👾, Guild-of-Chronic-Procrastinators, Guild-of-the-Learned, 
Guild-of-the-Ancients (a *secret* guild), Guild-of-Champions🏆 (a *secret* guild)  

`Classes:`  hero, warrior, mage, priest, scholar, necromancer

`Skills:` attack, guard, double-attack,triple-attack,heal

`States:`  knockout😖, rage 😡, confusion 😖, fear 😱, asleep😴, immortal😎, blind😵, normal, dead🤯
extremely-intellectual🧐, unbearably-cool🤠, sick🤒, cat😼, not-ready-for-adult-life🧖‍♀️, snail🐌, on-spring-break🍹

Items include their possible uses in the description. As an example, you can read a `green-book`📗,`blue-book`📘, or `orange-book`📙 to increase your player skills. Eating an `apple`🍎 increases your health. See full documentation of item and monster databases below. 

Rooms are connected to each other by exits. An exit from a room has a
direction, which can be any single word, but should be something that
sounds like a direction (e.g., north, south, up, down, northeast,
etc.). Exits are uni-directional.

A player has a collection of stats: a weapon, an armor item of choice, a health parameter (mana),a state, and a class. If the player loses all her mana she will not be able to move around the dungeon anymore. The default class is `hero`. You can only change your class
by finding certain items. Note that when <b>placing</b> an item and typing the name of the item in your inventory as input you must include the entire name of the item, which often includes an emoji with no spaces. Be precise and the code will work just fine! 

Combat is simple: the player has an *attack-power* (ATP) level and a *defend-power* (DEF) level. You can increase either one through combat experience or by gaining items in the rooms.  

Only users with a `crystal` in their inventory can spawn monsters. Similarly, a player must have a shovel in her inventory to dig 
new rooms. <img src="https://66.media.tumblr.com/c3dee66743dcae9b27be041078173276/tumblr_pq8129ihmp1tk06jno1_250.png" height="100" width="70" align="right">

Multi-player feature has not been implemented because I have a lifelong hatred of multi-player games. Probably because I didn't go to kindergarten and thus never learned how to play well with the other kids (‾▿‾)

To run the dungeon I've created named <b>Erebor</b>, use `python3 erebor.py | python3 dungeon.py`. 

All graphics are credited to <a href="http://www.rpgmakerweb.com/products/programs/rpg-maker-vx">RPG Maker VX</a>, excluding (naturally) the original drawings. 

## Remaining Implementation/Tweaks 
- [ ] *Danger warning:* Some objects still produce Nonetype error, which is related to the emojis. Not all items/monsters have been tested.


## Completed Implementation/Tweaks
- [x] set `force_florid` back on after running build Erebor code
> Now running the build Erebor code will call superuser privileges (as before) but will also remove superuser privileges at the end of the code. Whenever `doLook()` with superuser privileges is called, the typical `visit = 1` code is skipped. This ensures that the players running dungeon code after building Erebor will be able to see all the florid descriptions in their initial exploration of the pre-made dungeon.

- [x] seems to be some error with `spawn` function! fix — (you should not be able to spawn if a monster already exists) 
> Now users can only spawn monsters in rooms without a monster. Also, users cannot place items (loot) in a room that already contains loot. 

- [x] implement flee
- [x] fetch the monster stats from the monster database
> Now the stats of spawned monsters is actually fetched from the monster description database, as was intended. `buildMonsterTable` was the existing command that builds this monster description database at dungeon creation. When a user spawns a monster, like `jack-o-lantern🎃`, the monster's stats are fetched from the table. Then the monster is placed in the dungeon in the current room.

- [x] unequipping weapons is now supported
- [x] starting player stats too high based on monster objects chosen for Erebor current rooms
> Lowered starter player stats to <i>attack_power</i>: 150 and <i>defense_power</i>: 150. 
- [x] dead state fix

> Dead state now makes it impossible for user to purchase stats, equip armor, move around the room, etc. You get the point: if you are dead, you are dead. Game over. There was a bug with the addition of the comprehensive dead state involving doLook(), which is now fixed. 



## Running the Code
Build Erebor with the code `python3 erebor.py | python3 Dungeon.py`. Then run `python3 Dungeon.py` to play inside the dungeon.

Warning: If you make reference to an item or monster with an emoji, an emoji must be used. We provide a code example below.
```
You have in your inventory: revival-dove🕊  mini-chest  money-bag💰  plain-chest  golden-chest  steel-chest  crown-of-awesome👑  
Type the name of the item you would like to see the description of: money-bag💰
    Not sure where this came from. It is best not to look into such things.
```
   
  User must copy-and-paste emoji 💰 when asking for the item description of money-bag. Forgetting to do so will break the code.
  
  ```
  > use
Choose an item from your inventory: money-bag💰
Your gold has increased by 100000.
  ```
Again, in order to use money-bag💰, user must copy and paste emoji with no space. 

Finally, in order to spawn a monster with an attached emoji, the emoji must be provided. Many examples of this are given in `erebor.py`. 

```
print("dig s n | room of artemis | There are nine women in this forested room holding bows and glaring at you menacingly. | bow🏹") 
print("s") # inside room of artemis
print("spawn")
print("snake🐍")
```

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
Use 'check' to survey your inventory, 'take' to steal loot, 'place' to leave loot behind,
'view' to check your stats, 'use' to employ an item and 'fight' to engage in combat.
To join a guild, type 'join' & select a Guild. Some guilds can only be joined via events.
If you have a crystal in your inventory you can spawn a monster: type 'spawn.'
Type 'purchase' to use your gold to upgrade stats like health, atk_power, and def_power.
Type 'equip' to equip yourself with weapons and armor from your inventory.
entrance
No items in this room.
There's a dinosaur-of-yore🦕 in this room (ง •̀_•́)ง
    Show this dinosaur there is a reason his species went extinct! Send him back to yore, o noble adventurer.
    Health: 160
    Attack_power : 200
    Defense_power : 100
    Exp : 230
There are exits in these directions: e w s 
> fight
Get ready to fight dinosaur-of-yore🦕 (ง •̀_•́)ง 
Type 'flee' at any point during the battle to stop fighting.
You may only use the skills double-attack and/or triple-attack once per battle.
The triple-attack skills lowers your health by 100, and the double-attack skill
lowers your health by 50.
╔╗ ╔═╗╔╦╗╔╦╗╦  ╔═╗  ╔╗ ╔═╗╔═╗╦╔╗╔
╠╩╗╠═╣ ║  ║ ║  ║╣   ╠╩╗║╣ ║ ╦║║║║
╚═╝╩ ╩ ╩  ╩ ╩═╝╚═╝  ╚═╝╚═╝╚═╝╩╝╚╝
Possible skills are attack, guard, double-attack, triple-attack,heal.
Choose a skill to use : triple-attack
You attack the dinosaur-of-yore🦕 using skill triple-attack, dealing 550.0 damage.
dinosaur-of-yore🦕 has died. You've won the battle.
╔╗ ╔═╗╔╦╗╔╦╗╦  ╔═╗  ╔═╗╔╗╔╔╦╗
╠╩╗╠═╣ ║  ║ ║  ║╣   ║╣ ║║║ ║║
╚═╝╩ ╩ ╩  ╩ ╩═╝╚═╝  ╚═╝╝╚╝═╩╝
You've gained 100 experience.
> look
You are standing at the entrance of what appears to be a vast, complex cave.
No items in this room.
There are exits in these directions: e w s 
> s
room of darkness
No items in this room.
There's a owl🦉 in this room (ง •̀_•́)ง
    OooooooooOOOOOOOOooooooooooooooooo
    Health: 160
    Attack_power : 200
    Defense_power : 100
    Exp : 90
There are exits in these directions: n e w s 
> check
You have in your inventory: money-bag💰  
Type the name of the item you would like to see the description of: money-bag💰
    Not sure where this came from. It is best not to look into such things.
> s
explosive room
This room contains a shield.
There's a jack-o-lantern🎃 in this room (ง •̀_•́)ง
    He is smirking at you. Go get him.
    Health: 200
    Attack_power : 30
    Defense_power : 200
    Exp : 45
There are exits in these directions: n e s 
> take
Are you sure you want to take shield?
Press 1 to confirm: 1
You took shield!
> fight
Get ready to fight jack-o-lantern🎃 (ง •̀_•́)ง 
Type 'flee' at any point during the battle to stop fighting.
You may only use the skills double-attack and/or triple-attack once per battle.
The triple-attack skills lowers your health by 100, and the double-attack skill
lowers your health by 50.
╔╗ ╔═╗╔╦╗╔╦╗╦  ╔═╗  ╔╗ ╔═╗╔═╗╦╔╗╔
╠╩╗╠═╣ ║  ║ ║  ║╣   ╠╩╗║╣ ║ ╦║║║║
╚═╝╩ ╩ ╩  ╩ ╩═╝╚═╝  ╚═╝╚═╝╚═╝╩╝╚╝
Possible skills are attack, guard, double-attack, triple-attack,heal.
Choose a skill to use : double-attack
You attack the jack-o-lantern🎃 using skill double-attack, dealing 540.0 damage.
jack-o-lantern🎃 has died. You've won the battle.
╔╗ ╔═╗╔╦╗╔╦╗╦  ╔═╗  ╔═╗╔╗╔╔╦╗
╠╩╗╠═╣ ║  ║ ║  ║╣   ║╣ ║║║ ║║
╚═╝╩ ╩ ╩  ╩ ╩═╝╚═╝  ╚═╝╝╚╝═╩╝
You've gained 100 experience.
> view
STATS
     Health : 100
     State : normal
     Weapon : none
     Armor : none
     Class : hero
     Attack_power : 350
     Defense_power : 350
     Exp : 200
     Guild : none
     Gold : 50
> purchase
You currently have 50 in gold.
What stat would you like to upgrade?
Choose (1) health, (2) atk_power, (3) def_power: 1
It costs 1 piece of gold to upgrade your health by 1.
Type how much gold you would like to spend to increase your health: 50
You've increased your health power by 50
> join
Select a guild to join: Guild-of-Mages(0), Guild-of-The-Dark-Arts👾(1), Guild-of-Chronic-Procrastinators(2),Guild-of-the-Learned(3). 2
You have joined the Guild of Chronic Procrastinators!
As a welcome gift, you have received tent⛺️, beer🥃, ramen🍜, popcorn, wine, chinese-takeout, salt-and-straw-icecream, and bed.
Your new state is not-ready-for-adult-life🧖‍♀️.
Your new class is warrior.
> view
STATS
     Health : 150
     State : not-ready-for-adult-life🧖‍♀️
     Weapon : none
     Armor : none
     Class : warrior
     Attack_power : 350
     Defense_power : 350
     Exp : 200
     Guild : Guild-of-Chronic-Procrastinators
     Gold : 0
> s
amusement park room
This room contains a the-american-dream🏠.
There's a unicorn🦄 in this room (ง •̀_•́)ง
    She is shiny, she is pink, and she is going to knock you down with that horn unless you pull yourself out of your stupor and fight.
    Health: 500
    Attack_power : 800
    Defense_power : 200
    Exp : 100
There are exits in these directions: n e s 
> take
Are you sure you want to take the-american-dream🏠?
Press 1 to confirm: 1
You took the-american-dream🏠!
> q
bye!
------------------------------------------------------------------------------------------------
```

## About Erebor
<br><i>Welcome to the Kingdom of Erebor. All who choose to play this game: tread cautiously, brave adventurers of the deep. Beyond these gates is the unknown.</i>
<center><img src="https://66.media.tumblr.com/86a83a69e2114c4419b2008017c50f74/tumblr_pq8s3rDGQa1tk06jno1_1280.png" width="400" height="80"></center>

## Map of Erebor 
<img src="https://raw.githubusercontent.com/nikarichardson/CSCI393/master/dungeon/dungeon_map.jpg" height="750" width="600">
<img src="https://66.media.tumblr.com/66ed120fa237a32e7ccbef90b2ff7680/tumblr_prejnuMWJw1tk06jno1_1280.jpg" height="750" width="600">

## Item Database :
Has name of item, description, and use value. 
<br>- `plain-chest:` <i>Well, it is better than nothing. Right?!</i> Increases gold by <b>100</b>. 
<br>- `golden-chest:` <i>The best chest there is.</i> Increases gold by <b>500</b>. 
<br>- `steel-chest:` <i>Seems like it might be hard to open</i> Increases gold by <b>200</b>. 
<br>- `mini-chest:` <i>Just because it is tiny does not mean it's worthless. Oh, well, actually . . .</i> Increases gold by <b>10</b>. 
<br>- `mana-crystal:` <i>Use this to increase your health by +300.</i> Increases health by <b>300</b>. 
<br>- `pick-axe:` <i>A great medieval weapon. Which would be perfect, if you were living in medieval times. You are not.</i> Increases attack power by <b>30</b>. 
<br>- `potion:` <i>No, this potion does not come up with an ingredient list, silly. Just drink it or leave it. Time will tell.</i> Increases health by <b>100</b>. 
<br>- `blue-book📘:` <i>It's not perfect, but you suspect this blue book is better than the red book.</i> Increases exp by <b>50</b>. 
<br>- `green-book📗:` <i>Seriously, it is better than the red book. I think.</i> Increases exp by <b>100</b>. 
<br>- `orange-book📙:` <i>The red book does not even exist, ok? But this book exists. It might help you.</i> Increases exp by <b>300</b>.
<br>- `tome📖:` <i>Um, are you sure you want to read this? It looks long.</i> Increases exp by <b>1000</b>. 
<br>- `ring:` <i>This does not do anything, but it is shiny. Maybe bring it just in case a lovely lady comes along?</i>
<br>- `shield:` <i>The only shield available in this game, because the creator wants to abandon you in a dungeon of monsters with only one piece of armor available. What could go wrong?</i> Increases defense by <b>500</b>. 
<br>- `crystal:` <i>Use this to spawn any type of monster you want. Maybe it does not make sense to you why a crystal would spawn a monster. Stop trying to figure everything out, kid.</i> Spawns monster. 
<br>- `crown-of-awesome👑:` <i>Has absolutely no useful value, but, let us face it: it is awesome. Is not the awe-inspiring, effusive, magnificent power of awesome enough for you?</i>
<br>- `apple🍎:` <i>An apple a day, they say. .  .</i> Increases health by <b>100</b>. 
<br>- `beer🥃:` <i>End the day with some cold beer, and your problems will disappear. Just kidding. But. It tastes good.</i> Increases health by <b>250</b>. 
<br>- `ramen🍜:` <i>A primary food group.</i> Increases health by <b>70</b>. 
<br>- `ISS🛰:` <i>We do not know what this is doing here. Should not the International Space Station be...in space?</i> Increases power by <b>10000000</b>.
<br>- `tent⛺️:` <i>If everything is going wrong, you can always hide in this tent.</i>
<br>- `crystal-ball🔮:` <i>This ball shows you the future. Not just of your life, but of the entire cosmos. So yes, you can ask the crystal ball questions about the nature of time, but there are also pressing questions you can ask, like: what is for dinner?</i>
<br>- `portal🌀:` <i>Use this to teleport at will to any room. As long as you have the room id, that is.</i> Use for teleportation. 
<br>- `flower🌸:` <i>There is definitely something sinister about this flower. Might want to just put it down—that's it. Now back away.</i>
<br>- `wheat🌾:` <i>An agricultural relic.</i> Increases health by <b>50</b>. 
<br>- `herb🌿:` <i>Well, it is not exactly a salad, but it is better than nothing.</i> Increases health by <b>80</b>. 
<br>- `mushroom🍄:` <i>I wonder if eating this mysterious, possibly toxic mushroom that you found in the middle of a dungeon would be a fun thing to do.</i> Decreases health by <b>10000</b>.
<br>- `tulip🌷:` <i>Flowers are pretty, but they do not do much.</i>
<br>- `candle🕯:` <i>Very mysterious.</i>
<br>- `bed 🛌:` <i>Yawnnnn.</i> Increases health by <b>500</b>. 
<br>- `revival-dove🕊:` <i>Revives a dead-person.</i> Changes state from <b>dead</b> to <b>normal</b>. 
<br>- `shell🐚:` <i>I wonder how a shell came to be in a dungeon. The other items make sense, but: a shell? That does not make sense. The Federal Reserve, maybe.</i>
<br>- `banana🍌:` <i>Yuck.</i> Decreases health by <b>250</b>. 
<br>- `lemon🍋:` <i>Too sour to eat. Maybe if you had some water?</i>
<br>- `watermelon🍉:` <i>Watermelons are simply the best.</i> Increases health by <b>450</b>. 
<br>- `grapes🍇:` <i>One taste of these grapes leads to instant Dionysian reverie.</i> Increases health by <b>860</b>. 
<br>- `peach🍑:` <i>You are beautiful. Love, Peach.</i> Increases health by <b>60</b>. 
<br>- `cherry🍒:` <i>Hello, daddy. Hello, mom. I am your ch-ch-ch-cherry bomb!</i> Increases health by <b>350</b>. 
<br>- `strawberry🍓:` <i>If you keep my secret I will give you this strawberry.</i> Increases health by <b>50</b>. 
<br>- `kiwi🥝:` <i>Kiwi would be a cute name for a child, right? Anyway, this is not the child Kiwi. It is the fruit kiwi.</i> Increases health by <b>75</b>. 
<br>- `corn🌽:` <i>Some corn. Not much to say about corn, really.</i> Increases health by <b>30</b>.
<br>- `popcorn🍿:` <i>Do you think it is a good idea to have some popcorn and watch a movie in the middle of a dungeon rife with monsters?</i>
<br>- `chinese-takeout🥡:` <i>Nothing says I-hate-cooking as much as some Chinese takeout.</i> Decreases health by <b>250</b>. Increases attack power by <b>300</b>. 
<br>- `salt-and-straw-icecream 🍨:` <i>Good thing you got this somehow. The lines are too long; there is no point in battling for ice cream when you have monsters to battle.</i> Increases health by <b>1000</b>. 
<br>- `grandmas-pie🥧:` <i>Smells good! Eat an entire pie by yourself. You are an adult, after all. </i> Increases health by <b>500</b>.
<br>- `honey🍯:` <i>Belongs to Pooh Bear. On temporary loan to Erebor dungeon.</i> Increases health by <b>150</b>. 
<br>- `tea🍵 :` <i>You just know that the pretentious tea drinkers among us are going to kill us for not specifying the type of tea here. Oh well. Tea people are not exactly the most ferocious. I will take my chances.</i> Increases health by <b>40</b>. 
<br>- `wine🍷:` <i>Drink up, me hearties, yo ho!</i> Increases health by <b>500</b>. 
<br>- `amphora-of-the-ancients🏺:` <i>There is writing on the outside of this amphora, but you cannot read Ancient Greek.</i>
<br>- `the-world🌍:` <i>It is so tiny, so round, so cute!! </i> Increases defense power by <b>10,000</b>. 
<br>- `volcanic-mountain🌋:` <i>You would prefer a chocolate lava, but hey.</i> 
<br>- `paradise-island🏝:` <i>What if you need a vacation, but your employer does not offer paid vacations? Use this paradise island in your inventory for an immediate escape.</i> Increases health by <b>12,000</b>. 
<br>- `Athens🏛:` <i>Some people love Greece so much they want to keep a relic of the Acropolis in their bag. Hey, to each to their own, right?</i>
<br>- `the-american-dream🏠:` <i>Hard to attain, harder to keep.</i> Increases gold by <b>50,000</b>.
<br>- `the-Federal-Reserve🏦:`  <i>Wait a second: if the Federal Reserve is in your inventory, who is running the monetary system right now?!</i> Increases gold by <b>500,000</b>. 
<br>- `hospital🏥:` <i>Why go to the hospital if you can keep one at all times in your bag?</i> Increases health by <b>10,000</b>. 
<br>- `statue-of-liberty🗽:` <i>Freedom is excellent, freedom is priceless. So do not be too disappointed that this statue does not do anything, k?</i>
<br>- `money-bag💰:` <i>Not sure where this came from. It is best not to look into such things.</i> Increases gold by <b>100,000</b>. 
<br>- `sword:` <i>A starter weapon</i>. Increases attack power by <b>100</b>. 
<br>- `bow🏹:` <i>You are obviously not Katniss, but it will still work.</i> Increases attack power by <b>200</b>. 
<br>- `dagger🗡:` <i>Great for stabbing friends (or political enemies) in the back. Et tu, Brute?</i> Increases attack power by <b>300</b>. 
<br>- `spear:` <i>It is not a wand.</i> Increases attack power by <b>400</b>. 
<br>- `claw:` <i>Nothing like a bear claw</i>. Increases attack power by <b>350</b>. 
<br>- `crossbow:` <i>You will get the hang of it.</i> Increases attack power by <b>450</b>. 
<br>- `hammer🔨:`<i>Probably better for fixing furniture.</i> Increases attack power by <b>60</b>. 
<br>- `wand:` <i>Magic is, after all, the ultimate power.</i> Increases attack power by <b>1000</b>. 

## Monster Database
Has name of monster, health, description, attack power, defense power, & exp gained from defeating monster. 
<br>`minotaur:`  <b>Health</b> 160. <i>Wait a second! I thought Theseus killed the Minotaur? Oh well. No point in debating it—that's definitely a minotaur, and he looks eager to fight.</i> <b>Attack power</b> 200. <b>Defense power</b> 100. <b>Exp</b> +90. 
<br>- `orc:`  <b>Health</b> 500. <i>This creature wandered all the way from Middle-Earth just to try and kill you. How nice!</i> <b>Attack power</b> 1000. <b>Defense power</b> 300. <b>Exp</b> +300. 
<br>- `plant:`  <b>Health</b> 40. <i>Show this plant the meaning of Darwinian selection. Survival of the fittest!!</i> <b>Attack power</b> 50. <b>Defense power</b> 0. <b>Exp</b> +30. 
<br>- `rat:`  <b>Health</b> 100. <i>Hmmm. It's a rat.</i> <b>Attack power</b> 30. <b>Defense power</b> 100. <b>Exp</b> +50. 
<br>- `ogre:`  <b>Health</b> 1000. <i>Looks like the Ogre from the Three Broomsticks has appeared, and he is here to spoil the ending of the next Harry Potter book. Better kill him before he does that. </i> <b>Attack power</b> 200. <b>Defense power</b> 100. <b>Exp</b> +90. 
<br>- `scorpion:`  <b>Health</b> 100. <i>Scorpionssssssss are sssssuppppppeeeerrrr scary.</i> <b>Attack power</b> 500. <b>Defense power</b> 10. <b>Exp</b> +40. 
<br>- `skeleton:`  <b>Health</b> 300. <i>Send this guy back to the grave!</i> <b>Attack power</b> 850. <b>Defense power</b> 40. <b>Exp</b> +200. 
<br>- `giant-ant🐜:`  <b>Health</b> 20. <i>This forager is out for blood.</i> <b>Attack power</b> 10000. <b>Defense power</b> 0. <b>Exp</b> +400. 
<br>- `bat🦇:`  <b>Health</b> 50. <i>Oooo, bats are spooky. Do you not think battling a bat is a perfect way to spend the fall semester?</i> <b>Attack power</b> 200. <b>Defense power</b> 30. <b>Exp</b> +50. 
<br>- `slime:`  <b>Health</b> 100. <i>This monster looks a bit like jello. Or play-doh. Or transparent clay. You get it. It is slime.</i> <b>Attack power</b> 0. <b>Defense power</b> 400. <b>Exp</b> +134. 
<br>- `snake🐍:`  <b>Health</b> 160. <i>Cmon, get ready to fight and send this snake back to the garden he came from!</i> <b>Attack power</b> 200. <b>Defense power</b> 100. <b>Exp</b> +90. 
<br>- `werewolf:`  <b>Health</b> 800. <i>Not sure why this werewolf is out on a night like this. No full moon in sight. Anyway, he is here, and it is probably a good idea to get your weapon out.</i> <b>Attack power</b> 400. <b>Defense power</b> 450. <b>Exp</b> +200. 
<br>- `zombie:`  <b>Health</b> 1000. <i>Yeah, zombiess are creepy, but he just wants a hug. Scary, but harmless.</i> <b>Attack power</b> 0. <b>Defense power</b> 100. <b>Exp</b> +60. 
<br>- `vampire:`  <b>Health</b> 1000. <i>By day, he is a vampire. By night, he works the night shift in the blood donation center. No one has ever determined how he has managed to come by so much blood . . .</i> <b>Attack power</b> 800. <b>Defense power</b> 340. <b>Exp</b> +200. 
<br>- `chimera:`  <b>Health</b> 450. <i>Is it too cheesy to suggest this monster might just be chimerical? Even the stats are suspect.</i> <b>Attack power</b> 450. <b>Defense power</b> 450. <b>Exp</b> +450. 
<br>- `cerberus:`  <b>Health</b> 430. <i>I do not think you can deal with a three-headed monster. You can't even deal with a one-headed monster.</i> <b>Attack power</b> 10,000. <b>Defense power</b> 330. <b>Exp</b> +240. 
<br>- `spider:`  <b>Health</b> 50. <i>It's a creepy spider, and you do not like it.</i> <b>Attack power</b> 200. <b>Defense power</b> 100. <b>Exp</b> +10. 
<br>- `ghost:`  <b>Health</b> 100. <i>One moment, he is there. The next, he is...where did he go?!</i> <b>Attack power</b> 300. <b>Defense power</b> 100000. <b>Exp</b> +500. 
<br>- `taco🌮:` <b>Health</b> 1000. <i>You want to fight the taco, but you also kinda wanna eat it. Friend or foe? Combat opponent or...lunch?
</i> <b>Attack power</b> 400. <b>Defense power</b> 0. <b>Exp</b> +340. 
<br>- `fairy🧚‍:`  <b>Health</b> 500. <i>Don not underestimate her tiny size.</i> <b>Attack power</b> 700. <b>Defense power</b> 40. <b>Exp</b> +600. 
<br>- `dragon🐉:` <b>Health</b> 10000. <i>There be dragons.</i> <b>Attack power</b> 1000. <b>Defense power</b> 800. <b>Exp</b> +480. 
<br>- `dinosaur-of-yore🦕:`  <b>Health</b> 160. <i>Show this dinosaur there is a reason his species went extinct! Send him back to yore, o noble adventurer.</i> <b>Attack power</b> 200. <b>Defense power</b> 100. <b>Exp</b> +230. 
<br>- `bee-of-disproportionate-size🐝:`  <b>Health</b> 700 <i>It is what it sounds like.</i> <b>Attack power</b> 12. <b>Defense power</b> 32. <b>Exp</b> +100. 
<br>- `mostly-friendly-wolf🐺:`  <b>Health</b> 100 <i>I do not want to encounter this guy when he's mostly unfriendly.</i> <b>Attack power</b> 300. <b>Defense power</b> 100. <b>Exp</b> +200. 
<br>- `pineapple🍍:`  <b>Health</b> 800. <i>You have encountered a pineapple. Yellow, large, and let us be honest: it is super spikey. A fearsome opponent. </i> <b>Attack power</b> 200. <b>Defense power</b> 100. <b>Exp</b> +260. 
<br>- `kleptomaniac-squirrel-of-doom🐿:`  <b>Health</b> 1000. <i>You have encountered the squirrel of doom. I hate to be the bearer of bad news, but this is the end for you, truly. Unless you happen to have an acorn in your inventory, the inevitable is coming. Let us just say there is 
a *reason* this little guy is called the kleptomaniac squirrel of doom. </i> <b>Attack power</b> 100. <b>Defense power</b> 10000000000. <b>Exp</b> +90. 
<br>- `the-great-mage:`  <b>Health</b> 10000. <i>Best to flee. A learned mage is a fearsome contender.</i> <b>Attack power</b> 1000. <b>Defense power</b> 1000. <b>Exp</b> +400. 
<br>- `apprentice:`  <b>Health</b> 5000. <i>He wants to be more like the great mage and less like himself.</i> <b>Attack power</b> 400. <b>Defense power</b> 300. <b>Exp</b> +150. 
<br>- `merman🧜:` <b>Health</b> 300. <i>Maybe we can distract him with a mermaid?</i> <b>Attack power</b> 800. <b>Defense power</b> 140. <b>Exp</b> +270. 
<br>- `elf🧝:`  <b>Health</b> 400. <i>Looks like Orlando Bloom.</i> <b>Attack power</b> 400. <b>Defense power</b> 200. <b>Exp</b> +300. 
<br>- `unicorn🦄:`  <b>Health</b> 500. <i>She is shiny, she is pink, and she is going to knock you down with that horn unless you pull yourself out of your stupor and fight.</i> <b>Attack power</b> 800. <b>Defense power</b> 200. <b>Exp</b> +100. 
<br>- `owl🦉:` <b>Health</b> 160. <i>OooooooooOOOOOOOOooooooooooooooooo</i> <b>Attack power</b> 200. <b>Defense power</b> 100. <b>Exp</b> +90. 
<br>- `whale 🐳:`  <b>Health</b> 300. <i>He is blowing bubbles to tease you. It is all fun and games until it is not fun and games.</i> <b>Attack power</b> 400. <b>Defense power</b> 100. <b>Exp</b> +240. 
<br>- `dolphin🐬:`  <b>Health</b> 400. <i>Awwww, it's a dolphin.</i> <b>Attack power</b> 200. <b>Defense power</b> 100. <b>Exp</b> +90. 
<br>- `magical-fish-out-of-water 🐟:`  <b>Health</b> 30. <i>What disturbs you more than seeing a fish out of water is seeing an alive fish out of water.</i> <b>Attack power</b> 0. <b>Defense power</b> 100. <b>Exp</b> +34. 
<br>- `blowfish🐡:`  <b>Health</b> 150. <i>Let us call him squishy.</i> <b>Attack power</b> 400. <b>Defense power</b> 200. <b>Exp</b> +180. 
<br>- `octopus🐙:`  <b>Health</b> 300. <i>It seems like an octopus could find a better occupation than monster. He could be a party planner or master organizer, for example.</i> <b>Attack power</b> 80. <b>Defense power</b> 120. <b>Exp</b> +50. 
<br>- `caterpillar-of-phenomenal-power🐛:`  <b>Health</b> 100. <i>This caterpillar is phenomenally powerful; you can feel it from afar.</i> <b>Attack power</b> 20000. <b>Defense power</b> 30. <b>Exp</b> +400. 
<br>- `zombie🧟:`  <b>Health</b> 300. <i>Enjoy your undead status while you still can.</i> <b>Attack power</b> 240. <b>Defense power</b> 230. <b>Exp</b> +220. 
<br>- `monarch-butterfly🦋:`  <b>Health</b> 50. <i>Yes, butterflies have numbered days and do not live for long. Do not feel too bad; your days are numbered too.</i> <b>Attack power</b> 30. <b>Defense power</b> 10. <b>Exp</b> +30. 
<br>- `evil-shrimp🦐:`  <b>Health</b> 200. <i>He has malicious intentions. Shrimp always do.</i> <b>Attack power</b> 200. <b>Defense power</b> 70. <b>Exp</b> +90. 
<br>- `alien🛸:`  <b>Health</b> 160. <i>Please be a conspiracy theory. Please be a conspiracy theory! You are not supposed to be real!</i> <b>Attack power</b> 700. <b>Defense power</b> 300. <b>Exp</b> +550. 
<br>- `time⏱:`  <b>Health</b> 100. <i>Our greatest enemy. We will see how true it is that you cannot be conquered.</i> <b>Attack power</b> 1000. <b>Defense power</b> 0. <b>Exp</b> +1000. 
<br>- `bad-weather⛈:`  <b>Health</b> 100. <i>Humans should be able to control the weather.</i> <b>Attack power</b> 40. <b>Defense power</b> 10. <b>Exp</b> 35. 
<br>- `god-of-north-wind🌬:`  <b>Health</b> 250. <i>He is kinda beautiful, but he keeps blowing a chilly breeze your way. You forgot to bring a sweater, so you are not going to tolerate that kind of behavior.</i> <b>Attack power</b> 800. <b>Defense power</b> 100. <b>Exp</b> +300. 
<br>- `umbrella🌂:`  <b>Health</b> 600. <i>An umbrella; it is notoriously hard to open. And to close.</i> <b>Attack power</b> 1000. <b>Defense power</b> 0. <b>Exp</b> +500. 
<br>- `fire🔥:`  <b>Health</b> 200 <i>Stop, drop and roll.</i> <b>Attack power</b>460. <b>Defense power</b> 0. <b>Exp</b> +200. 
<br>- `jack-o-lantern🎃:`  <b>Health</b> 200. <i>He is smirking at you. Go get him.</i> <b>Attack power</b> 30. <b>Defense power</b> 20. <b>Exp</b> +45. 

## Guilds 
<br>- `Guild of Mages`: Welcome pack has `revival-dove🕊`, `mini-chest`, `money-bag💰`, `plain-chest`, `golden-chest`, `steel-chest`, and `crown-of-awesome👑`. New class is `mage`. New state is `unbearably-cool🤠`. 
<br>- `Guild of The Dark Arts`: Welcome pack has `wand`, `potion`, `crystal-ball🔮`, and `portal🌀`. New state is `immortal`. New class is `necromancer`. 
<br>- `Guild of the Chronic Procrastinators`: Welcome pack has `tent⛺️`, `beer🥃`, `ramen`🍜, `popcorn🍿`, `wine🍷`, `chinese-takeout🥡`, `salt-and-straw-icecream🍨`, and `bed🛌`. New state is `not-ready-for-adult-life🧖‍`. New class is `warrior`.
<br>- `Guild of the Learned`: Welcome pack has `blue-book📘`, `green-book📗`, `orange-book📙`, `tome📖`. New class is `scholar`. New state is `extremely-intellectual🧐`.
<br>- `Guild of the Ancients`: Secret guild. 
<br>- `Guild of Champions`: Secret guild. 
