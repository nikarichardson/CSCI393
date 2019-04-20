SQLite Dungeon
==============
<img src="https://66.media.tumblr.com/d471e4f3dee7aca7d07468ae89225edb/tumblr_ppnk1hKli51tk06jno1_540.jpg" align="right"> 
Adapted from <a href="https://github.com/dylanmc/SQLiteDungeon">Dylan's Dungeon</a> code from Spring 2019 Operating systems. 
Written in Python with SQLite3 as back-end. Image on right from RPG Maker VX with my character sprite in a designed dungeon map. 

This dungeon has rooms and exits. You can <i>spawn</i> a monster, <i>place</i>  loot, <i>take</i>  loot, and engage in combat with the monsters inside the dungeon. Users with a shovel in their inventory can <i>dig</i>  rooms. 

`Monsters:` minotaur, orc, plant, rat, ogre, scorpion, skeleton, giant-ant 🐜 ,bat 🦇,slime, snake🐍,
succubus, werewolf, zombie, skeleton, vampire, chimera, cerberus, spider, ghost,taco 🌮,fairy🧚‍, dragon 🐉,
dinosaur-of-yore 🦕, bee-of-disproportionate-size 🐝, mostly-friendly-wolf 🐺, pineapple 🍍,
kleptomaniac-squirrel-of-doom 🐿, the-great-mage 🧙‍♂️ apprentice 🧙‍♀️, merman 🧜, mermaid 🧜‍♀️, elf 🧝, unicorn 🦄
owl 🦉, whale 🐳, dolphin 🐬, magical-fish-out-of-water 🐟, blowfish 🐡, octopus 🐙, caterpillar-of-phenomenal-power 🐛
zombie🧟, monarch-butterfly 🦋, evil-shrimp 🦐, alien 🛸, time ⏱, bad-weather ⛈, god-of-north-wind 🌬, umbrella 🌂, fire 🔥, jack-o-lantern 🎃

`Loot/Items:` plain-chest, golden-chest, steel-chest, mini-chest
mana-crystal, pick-axe, potion, blue-book 📘, green-book 📗, orange-book 📙, tome 📖, ring, herb, shield, crystal,
crown of awesome 👑, apple 🍎, beer 🥃, ramen 🍜, ISS 🛰 (the international
 space station), tent ⛺️, crystal-ball 🔮,portal 🌀, flower 🌸, wheat 🌾, herb 🌿, mushroom 🍄, tulip 🌷, beer 🥃, 
candle 🕯, bed 🛌, revival-dove 🕊, shell 🐚, grapes 🍇,  banana 🍌, lemon 🍋, watermelon 🍉, grapes 🍇, peach 🍑
cherry 🍒, strawberry 🍓, kiwi 🥝, corn 🌽, popcorn 🍿, chinese-takeout 🥡, salt-and-straw-icecream 🍨, grandma's-pie 🥧
honey 🍯, tea 🍵, wine 🍷, amphora-of-the-ancients 🏺, the-world 🌍, volcanic-mountain 🌋, paradise-island 🏝, 
Athens 🏛 , the-american-dream 🏠, the-Federal-Reserve 🏦, hospital 🏥, statue-of-liberty 🗽, money-bag 💰 

`Weapons:` sword, pick-axe,bow 🏹 ,dagger🗡,spear,claw,crossbow, hammer 🔨

`Guilds:`  Guild-of-Mages, Guild-of-The-Dark-Arts 👾, Guild-of-Chronic-Procrastinators, Guild-of-the-Learned, 
Guild-of-the-Ancients (a *secret* guild), Guild-of-Champions 🏆  

`Classes:`  hero, warrior, mage, priest, scholar

`Skills:` attack, guard, double-attack,triple-attack,heal

`States:`  knockout 😖, rage 😡, confusion 😖, fear 😱, asleep 😴, immortal 😎, blind 😵, normal, dead 🤯
extremely-intellectual 🧐, unbearably-cool 🤠, sick 🤒, cat 😼, not-ready-for-adult-life 🧖‍♀️, snail 🐌, on-spring-break 🍹


Items include their possible uses in the description. As an example, you can read a `green-book` 📗,`blue-book`📘, or `orange-book` 📙 to increase your player skills. Eating an `apple` 🍎 increases your health. See full documentation of item and monster databases below. 

Rooms are connected to each other by exits. An exit from a room has a
direction, which can be any single word, but should be something that
sounds like a direction (e.g., north, south, up, down, northeast,
etc.). Exits are uni-directional.

A player has a collection of stats: a weapon, an armor item of choice, a health parameter (mana),a state, and a class. If the player
loses all her mana she will not be able to move around the dungeon anymore. The default class is `hero`. You can only change your class
by finding certain items. 

Combat is simple: the player has an *attack-power* (ATP) level and a *defend-power* (DEF) level. You can increase either one through combat experience or by gaining items in the rooms.  

Only users with a <b>Monster Crystal</b> in their inventory can spawn monsters. Similarly, a player must have a shovel in her inventory to dig 
new rooms. <img src="https://66.media.tumblr.com/c3dee66743dcae9b27be041078173276/tumblr_pq8129ihmp1tk06jno1_250.png" height="100" width="70" align="right">

Multi-player feature has not been implemented because I have a lifelong hatred of multi-player games. Probably because I didn't go to kindergarten
and thus never learned how to play well with the other kids (‾▿‾)

To run the dungeon I've created named <b>Erebor</b>, use `python3 erebor.py | python3 dungeon.py`. 

All graphics are credited to <a href="http://www.rpgmakerweb.com/products/programs/rpg-maker-vx">RPG Maker VX</a>. 

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
'view' to check your stats, 'spawn' to create monsters, and 'fight' to engage in combat.
You are standing at the entrance of what appears to be a vast, complex cave.
No items in this room.
There are exits in these directions: n 
> dig e w | library | A library? In the middle of a dungeon? How excellent, how unlikely! | tome
Sorry, only users with a shovel in their inventory can dig rooms.
> n
You are in a small, darkly-lit room.
This room contains a shovel.
There are exits in these directions: s 
> take
Are you sure you want to take shovel?
Press 1 to confirm: 1
You took shovel!
> check
You have in your inventory: shovel 
> dig e w | library | A library? In the middle of a dungeon? How excellent, how unlikely! | tome
> look
You are in a small, darkly-lit room.
There are exits in these directions: s e 
> e
A library? In the middle of a dungeon? How excellent, how unlikely!
This room contains a tome.
There are exits in these directions: w 
> place
Choose an item from your inventory: shovel
You've placed shovel in the room.
> place
Choose an item from your inventory: potion
You don't have a potion in your inventory. Use 'check' to survey your current inventory.
> fight
There are no monsters in this room.
> spawn
You can spawn the following monster objects: minotaur, orc, plant, rat, ogre, scorpion, skeleton, slime, snake, succubus, werewolf, zombie, skeleton, vampire, chimera, cerberus, spider, ghost, fairy, dragon.
Type the name of a monster object: chimera
You've spawned a chimera.
> look
There's a chimera in this room (ง •̀_•́)ง 
> fight
Get ready to fight chimera (ง •̀_•́)ง 
```

## About Erebor
<br><i>Welcome to the Kingdom of Erebor. All who choose to play this game: tread cautiously, brave adventurers of the deep. Beyond these gates is the unknown.</i>
<center><img src="https://66.media.tumblr.com/86a83a69e2114c4419b2008017c50f74/tumblr_pq8s3rDGQa1tk06jno1_1280.png" width="380" height="80"></center>

## Map of Erebor 
Coming soon 

## Item Database
Coming soon

## Monster Database
Coming soon 
