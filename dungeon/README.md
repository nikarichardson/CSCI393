SQLite Dungeon
==============
<img src="https://66.media.tumblr.com/d471e4f3dee7aca7d07468ae89225edb/tumblr_ppnk1hKli51tk06jno1_540.jpg" align="right"> 
Adapted from <a href="https://github.com/dylanmc/SQLiteDungeon">Dylan's Dungeon</a> code from Spring 2019 Operating systems. 
Written in Python with SQLite3 as back-end. Image on right from RPG Maker VX with my character sprite in a designed dungeon map. 

This dungeon has rooms and exits. You can <i>spawn</i> a monster, <i>place</i>  loot, <i>take</i>  loot, and engage in combat with the monsters inside the dungeon. Users with a shovel in their inventory can <i>dig</i>  rooms.  There are <b>6</b> Guilds, <b>16</b> states, <b>6</b> classes,<b>5</b> skills, <b>40+</b> monsters and <b>50+</b> items. 

`Monsters:` minotaur, orc, plant, rat, ogre, scorpion, skeleton, giant-ant 🐜 ,bat 🦇,slime, snake🐍,
succubus, werewolf, zombie, skeleton, vampire, chimera, cerberus, spider, ghost,taco 🌮,fairy🧚‍, dragon 🐉,
dinosaur-of-yore 🦕, bee-of-disproportionate-size 🐝, mostly-friendly-wolf 🐺, pineapple 🍍,
kleptomaniac-squirrel-of-doom 🐿, the-great-mage 🧙‍♂️ apprentice 🧙‍♀️, merman 🧜, mermaid 🧜‍♀️, elf 🧝, unicorn 🦄
owl 🦉, whale 🐳, dolphin 🐬, magical-fish-out-of-water 🐟, blowfish 🐡, octopus 🐙, caterpillar-of-phenomenal-power 🐛
zombie🧟, monarch-butterfly 🦋, evil-shrimp 🦐, alien 🛸, time ⏱, bad-weather ⛈, god-of-north-wind 🌬, umbrella 🌂, fire 🔥, jack-o-lantern 🎃

`Loot/Items:` plain-chest, golden-chest, steel-chest, mini-chest
mana-crystal, pick-axe, potion, blue-book 📘, green-book 📗, orange-book 📙, tome 📖, ring, herb, shield, crystal,
crown-of-awesome 👑, apple 🍎, beer 🥃, ramen 🍜, ISS 🛰 (the international
 space station), tent ⛺️, crystal-ball 🔮,portal 🌀, flower 🌸, wheat 🌾, herb 🌿, mushroom 🍄, tulip 🌷, beer 🥃, 
candle 🕯, bed 🛌, revival-dove 🕊, shell 🐚, grapes 🍇,  banana 🍌, lemon 🍋, watermelon 🍉, grapes 🍇, peach 🍑
cherry 🍒, strawberry 🍓, kiwi 🥝, corn 🌽, popcorn 🍿, chinese-takeout 🥡, salt-and-straw-icecream 🍨, grandma's-pie 🥧
honey 🍯, tea 🍵, wine 🍷, amphora-of-the-ancients 🏺, the-world 🌍, volcanic-mountain 🌋, paradise-island 🏝, 
Athens 🏛 , the-american-dream 🏠, the-Federal-Reserve 🏦, hospital 🏥, statue-of-liberty 🗽, money-bag 💰 

`Weapons:` sword, pick-axe,bow 🏹 ,dagger🗡,spear,claw,crossbow, hammer 🔨, wand

`Guilds:`  Guild-of-Mages, Guild-of-The-Dark-Arts 👾, Guild-of-Chronic-Procrastinators, Guild-of-the-Learned, 
Guild-of-the-Ancients (a *secret* guild), Guild-of-Champions 🏆 (a *secret* guild)  

`Classes:`  hero, warrior, mage, priest, scholar, necromancer

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

## Item Database :
Has name of item, description, and use value. 
<br>`plain-chest:` <i>Well, it's better than nothing. Isn't it?!</i> Increases gold by <b>100</b>. 
<br>`golden-chest:` <i>The best chest there is.</i> Increases gold by <b>500</b>. 
<br>`steel-chest:` <i>Seems like it might be hard to open</i> Increases gold by <b>200</b>. 
<br>`mini-chest:` <i>Just because it's tiny doesn't mean it doesn't contain a lot! Oh, well, actually . . .</i> Increases gold by <b>10</b>. 
<br>`mana-crystal:` <i>Use this to increase your health by +300.</i> Increases health by <b>300</b>. 
<br>`pick-axe:` <i>A great medieval weapon. Which would be perfect, if you were living in medieval times. You are not.</i> Increases attack power by <b>30</b>. 
<br>`potion:` <i>No, this potion doesn't come up with an ingredient list, silly. Just drink it or leave it. Time will tell.</i> Increases health by <b>100</b>. 
<br>`blue-book 📘:` <i>It's not perfect, but you suspect this blue book is better than the red book.</i> Increases exp by <b>50</b>. 
<br>`green-book 📗:` <i>Seriously, it's better than the red book. I think.</i> Increases exp by <b>100</b>. 
<br>`orange-book 📙:` <i>The red book does not even exist, ok? But this book exists. It might help you.</i> Increases exp by <b>300</b>.
<br>`tome 📖:` <i>Um, are you sure you want to read this? It looks long.</i> Increases exp by <b>1000</b>. 
<br>`ring:` <i>This doesn't do anything, but it's shiny. Maybe bring it just in case a lovely lady comes along?</i>
<br>`shield:` <i>The only shield available in this game, because the creator wants to abandon you in a dungeon of monsters with only one piece of armor available. What could go wrong?</i> Increases defense by <b>500</b>. 
<br>`crystal:` <i>Use this to spawn any type of monster you want. Maybe it doesn't make sense to you why a crystal would spawn a monster. Stop trying to figure everything out, kid.</i> Spawns monster. 
<br>`crown-of-awesome 👑:` <i>Has absolutely no useful value, but, let's face it: it's awesome. Isn't the awe-inspiring, effusive, magnificent power of awesome enough for you?</i>
<br>`apple 🍎:` <i>An apple a day, they say. .  .</i> Increases health by <b>100</b>. 
<br>`beer 🥃:` <i>End the day with some cold beer and your problems will disappear. Just kidding. But. It tastes good.</i> Increases health by <b>250</b>. 
<br>`ramen 🍜:` <i>A primary food group.</i> Increases health by <b>70</b>. 
<br>`ISS 🛰:` <i>We don't know what this is doing here. Shouldn't the International Space Station be...in space?</i> Increases power by <b>10000000</b>.
<br>`tent ⛺️:` <i>If everything is going wrong, you can always hide in this tent.</i>
<br>`crystal-ball 🔮:` <i>This ball shows you the future. Not just of your life, but of the entire cosmos. So yes, you can ask the crystal ball questions about the nature of time, but there are also pressing questions you can ask, like: what's for dinner?</i>
<br>`portal 🌀:` <i>Use this to teleport at will to any room. As long as you have the room id, that is.</i> Use for teleportation. 
<br>`flower 🌸:` <i>There's definitely something sinister about this flower. Might want to just put it down—that's it. Now back away.</i>
<br>`wheat 🌾:` <i>An agricultural relic.</i> Increases health by <b>50</b>. 
<br>`herb 🌿:` <i>Well, it's not exactly a salad, but it's better than nothing.</i> Increases health by <b>80</b>. 
<br>`mushroom 🍄:` <i>I wonder if you eating this mysterious, possibly toxic mushroom that you found in the middle of a dungeon would be a fun thing to do.</i> Decreases health by <b>10000</b>.
<br>`tulip 🌷:` <i>Flowers are pretty, but they don't do much.</i>
<br>`candle 🕯:` <i>Very mysterious, don't you think?</i>
<br>`bed 🛌:` <i>Yawnnnn.</i> Increases health by <b>500</b>. 
<br>`revival-dove 🕊:` <i>Revives a dead-person.</i> Changes state from <b>dead</b> to <b>normal</b>. 
<br>`shell 🐚:` <i>I wonder how a shell came to be in a dungeon. The other items make sense, but: a shell? That doesn't make sense. The Federal Reserve, maybe.</i>
<br>`banana 🍌:` <i>Yuck.</i> Decreases health by <b>250</b>. 
<br>`lemon 🍋:` <i>Too sour to eat. Maybe if you had some water?</i>
<br>`watermelon 🍉:` <i>Watermelons are simply the best.</i> Increases health by <b>450</b>. 
<br>`grapes 🍇:` <i>One taste of these leads to instant Dionysian reverie.</i> Increases health by <b>860</b>. 
<br>`peach 🍑:` <i>You are beautiful. Love, Peach.</i> Increases health by <b>60</b>. 
<br>`cherry 🍒:` <i>Hello, daddy. Hello, mom. I'm your ch-ch-ch-cherry bomb!</i> Increases health by <b>350</b>. 
<br>`strawberry 🍓:` <i>If you keep my secret I'll give you this strawberry.</i> Increases health by <b>50</b>. 
<br>`kiwi 🥝:` <i>Kiwi would be a cute name for a child, don't you think? Anyway, this isn't the child Kiwi. It's the fruit kiwi.</i> Increases health by <b>75</b>. 
<br>`corn 🌽:` <i>Some corn. Not much to say about corn, really.</i> Increases health by <b>30</b>.
<br>`popcorn 🍿:` <i>Do you think it's a good idea to have some popcorn and watch a movie in the middle of a dungeon rife with monsters?</i>
<br>`chinese-takeout 🥡:` <i>Nothing says i-hate-cooking as much as some Chinese takeout.</i> Decreases health by <b>250</b>. Increases attack power by <b>300</b>. 
<br>`salt-and-straw-icecream 🍨:` <i>Good thing you got this somehow. The lines are too long; there's no point in battling for ice cream when you have monsters to battle.</i> Increases health by <b>1000</b>. 
<br>`grandmas-pie 🥧:` <i>Smells good! Eat an entire pie by yourself, why don't you. You are an adult, after all. </i> Increases health by <b>500</b>.
<br>`honey 🍯:` <i>Belongs to Pooh Bear. On temporary loan to Erebor dungeon.</i> Increases health by <b>150</b>. 
<br>`tea 🍵 :` <i>You just know that the pretentious tea drinkers among us are going to kill us for not specifying the type of tea here. Oh well. Tea people aren't exactly the most ferocious. I'll take my chances.</i> Increases health by <b>40</b>. 
<br>`wine 🍷:` <i>Drink up, me hearties, yo ho!</i> Increases health by <b>500</b>. 
<br>`amphora-of-the-ancients 🏺:` <i>There's writing on the outside of this amphora, but you can't read Ancient Greek.</i>
<br>`the-world 🌍:` <i>It's so tiny, so round, so cute!! </i> Increases defense power by <b>10,000</b>. 
<br>`volcanic-mountain 🌋:` <i>You would prefer a chocolate lava, but hey.</i> 
<br>`paradise-island 🏝:` <i>What if you need a vacation, but your employer doesn't offer paid vacations? Use this paradise island in your inventory for an immediate escape.</i> Increases health by <b>12,000</b>. 
<br>`Athens 🏛:` <i>Some people love Greece so much they want to keep a relic of the Acropolis in their bag. Hey, to each to their own, right?</i>
<br>`the-american-dream 🏠:` <i>Hard to attain, harder to keep.</i> Increases gold by <b>500000</b>.
<br>`the-Federal-Reserve 🏦:`  <i>Wait a second: if the Federal Reserve is in your inventory, who's running the monetary system right now?!</i> Increases gold by <b>500,000</b>. 
<br>`hospital 🏥:` <i>Why go to the hospital if you can keep one at all times in your bag?</i> Increases health by <b>10,000</b>. 
<br>`statue-of-liberty🗽:` <i>Freedom is excellent, freedom is priceless. So don't be too disappointed that this statue doesn't do anything, k?</i>
<br>`money-bag 💰:` <i>Not sure where this came from. It's best not to look into such things.</i> Increases gold by <b>10000</b>. 

## Monster Database
Has name of monster, health, description, attack power, defense power, & exp gained from defeating monster. 
<br>`minotaur:`  <b>Health</b> 160. <i>Wait a second! I thought Theseus killed the Minotaur? Oh well. No point in debating it—that's definitely a minotaur, and he looks eager to fight.</i> <b>Attack power</b> 200. <b>Defense power</b> 100. <b>Exp</b> +90. 
<br>`orc:`  <b>Health</b> 500. <i>This creature wandered all the way from Middle-Earth just to try and kill you. How nice!</i> <b>Attack power</b> 1000. <b>Defense power</b> 300. <b>Exp</b> +300. 
<br>`plant:`  <b>Health</b> 40. <i>Show this plant the meaning of Darwinian selection. Survival of the fittest!!</i> <b>Attack power</b> 50. <b>Defense power</b> 0. <b>Exp</b> +30. 
<br>`rat:`  <b>Health</b> 160. <i>Wait a second! I thought Theseus killed the Minotaur? Oh well. No point in debating it—that's definitely a minotaur, and he looks eager to fight.</i> <b>Attack power</b> 200. <b>Defense power</b> 100. <b>Exp</b> +90. 
<br>`ogre:`  <b>Health</b>1000. <i>Looks like the Ogre from the Three Broomsticks has appeared, and he's here to spoil the ending of the next Harry Potter book. Better kill him before he does that. </i> <b>Attack power</b> 200. <b>Defense power</b> 100. <b>Exp</b> +90. 
<br>`scorpion:`  <b>Health</b> 100. <i>Scorpionssssssss are sssssuppppppeeeerrrr scary.</i> <b>Attack power</b> 500. <b>Defense power</b> 10. <b>Exp</b> +40. 
<br>`skeleton:`  <b>Health</b> 300. <i>Send this guy back to the grave!</i> <b>Attack power</b> 850. <b>Defense power</b> 40. <b>Exp</b> +200. 
<br>`giant-ant🐜:`  <b>Health</b> 20. <i>This forager is out for blood.</i> <b>Attack power</b> 10000. <b>Defense power</b> 0. <b>Exp</b> +400. 
<br>`bat🦇:`  <b>Health</b> 50. <i>Oooo, bats are spooky. Don't you think battling a bat is a perfect way to spend the fall semester?</i> <b>Attack power</b> 200. <b>Defense power</b> 30. <b>Exp</b> +50. 
<br>`slime:`  <b>Health</b> 100. <i>This monster looks a bit like jello. Or play-doh. Or transparent clay. You get it. It's slime.</i> <b>Attack power</b> 0. <b>Defense power</b> 400. <b>Exp</b> +134. 
<br>`snake🐍:`  <b>Health</b> 160. <i>C'mon, get ready to fight and send this snake back to the garden he came from!</i> <b>Attack power</b> 200. <b>Defense power</b> 100. <b>Exp</b> +90. 
<br>`succubus:`  <b>Health</b> 600. <i>She's beautiful but pure evil: be cautious.</i> <b>Attack power</b> 400. <b>Defense power</b> 250. <b>Exp</b> +200. 
<br>`werewolf:`  <b>Health</b> 800. <i>Not sure why this werewolf is out on a night like this. No full moon in sight. Anyway, he's here, and it's probably a good idea to get your weapon out.</i> <b>Attack power</b> 400. <b>Defense power</b> 450. <b>Exp</b> +200. 
<br>`zombie:`  <b>Health</b> 1000. <i>Yeah, zombiess are creepy, but he just wants a hug. Scary, but harmless.</i> <b>Attack power</b> 0. <b>Defense power</b> 100. <b>Exp</b> +60. 
<br>`vampire:`  <b>Health</b> 1000. <i>By day, he's a vampire. By night, he works the night shift in the blood donation center. No one has ever determined how he has managed to come by so much blood . . .</i> <b>Attack power</b> 800. <b>Defense power</b> 340. <b>Exp</b> +200. 
<br>`chimera:`  <b>Health</b> 450. <i>Is it too cheesy to suggest this monster might just chimerical? Even the stats are suspect.</i> <b>Attack power</b> 450. <b>Defense power</b> 450. <b>Exp</b> +450. 
<br>`cerberus:`  <b>Health</b> 430. <i>I don't think you can deal with a three-headed monster. You can't even deal with a one-headed monster.</i> <b>Attack power</b> 10,000. <b>Defense power</b> 330. <b>Exp</b> +240. 
<br>`spider:`  <b>Health</b> 50. <i>It's a creepy spider, and you don't like it.</i> <b>Attack power</b> 200. <b>Defense power</b> 100. <b>Exp</b> +10. 
<br>`ghost:`  <b>Health</b> 100. <i>One moment, he's there. The next, he's...where did he go?!</i> <b>Attack power</b> 300. <b>Defense power</b> 100000. <b>Exp</b> +500. 
<br>`taco🌮:` <b>Health</b> 1000. <i>You want to fight the taco, but you also kinda wanna eat it. Friend or foe? Combat opponent or...lunch?
</i> <b>Attack power</b> 400. <b>Defense power</b> 0. <b>Exp</b> +340. 
<br>`fairy🧚‍:`  <b>Health</b> 500. <i>Don't underestimate her tiny size.</i> <b>Attack power</b> 700. <b>Defense power</b> 40. <b>Exp</b> +600. 
<br>`dragon🐉:` <b>Health</b> 10000. <i>There be dragons.</i> <b>Attack power</b> 1000. <b>Defense power</b> 800. <b>Exp</b> +480. 
<br>`dinosaur-of-yore🦕:`  <b>Health</b> 160. <i>Show this dinosaur there's a reason his species went extinct! Send him back to yore, o noble adventurer.</i> <b>Attack power</b> 200. <b>Defense power</b> 100. <b>Exp</b> +230. 
<br>`bee-of-disproportionate-size🐝:`  <b>Health</b> 700 <i>It's what it sounds like.</i> <b>Attack power</b> 12. <b>Defense power</b> 32. <b>Exp</b> +100. 
<br>`mostly-friendly-wolf🐺:`  <b>Health</b> 100 <i>I don't want to encounter this guy when he's mostly unfriendly.</i> <b>Attack power</b> 300. <b>Defense power</b> 100. <b>Exp</b> +200. 
<br>`pineapple🍍:`  <b>Health</b> 800. <i>You've encountered a pineapple. Yellow, large, and let's be honest: it's super spikey. A fearsome opponent. </i> <b>Attack power</b> 200. <b>Defense power</b> 100. <b>Exp</b> +260. 
<br>`kleptomaniac-squirrel-of-doom🐿:`  <b>Health</b> 1000. <i>You've encountered the squirrel of doom. I hate to be the bearer of bad news, but this is the end for you, truly. Unless you happen to have an acorn in your inventory, the inevitable is coming. Let's just say there's 
a *reason* this little guy is called the kleptomaniac squirrel of doom. </i> <b>Attack power</b> 100. <b>Defense power</b> 10000000000. <b>Exp</b> +90. 
<br>`the-great-mage 🧙‍:`  <b>Health</b> 10000. <i>Best to flee. A learned mage is a fearsome contender.</i> <b>Attack power</b> 1000. <b>Defense power</b> 1000. <b>Exp</b> +400. 
<br>`apprentice 🧙‍:`  <b>Health</b> 5000. <i>He wants to be more like the great mage and less like himself.</i> <b>Attack power</b> 400. <b>Defense power</b> 300. <b>Exp</b> +150. 
<br>`merman🧜:` <b>Health</b> 300. <i>Maybe we can distract him with a mermaid?</i> <b>Attack power</b> 800. <b>Defense power</b> 140. <b>Exp</b> +270. 
<br>`elf🧝:`  <b>Health</b> 400. <i>Looks like Orlando Bloom.</i> <b>Attack power</b> 400. <b>Defense power</b> 200. <b>Exp</b> +300. 
<br>`unicorn🦄:`  <b>Health</b> 500. <i>She's shiny, she's pink, and she's going to knock you down with that horn unless you pull yourself out of your stupor and fight.</i> <b>Attack power</b> 800. <b>Defense power</b> 200. <b>Exp</b> +100. 
<br>`owl🦉:`  <b>Health</b> 160. <i></i> <b>Attack power</b> 200. <b>Defense power</b> 100. <b>Exp</b> +90. 
<br>`whale 🐳:`  <b>Health</b> 300. <i>He's blowing bubbles to tease you. It's all fun and games until it's not fun and games.</i> <b>Attack power</b> 400. <b>Defense power</b> 100. <b>Exp</b> +240. 
<br>`dolphin🐬:`  <b>Health</b> 400. <i>Awwww, it's a dolphin.</i> <b>Attack power</b> 200. <b>Defense power</b> 100. <b>Exp</b> +90. 
<br>`magical-fish-out-of-water 🐟:`  <b>Health</b> 30. <i>What disturbs you more than seeing a fish out of water is seeing an alive fish out of water.</i> <b>Attack power</b> 0. <b>Defense power</b> 100. <b>Exp</b> +34. 
<br>`blowfish🐡:`  <b>Health</b> 150. <i>Let's call him squishy.</i> <b>Attack power</b> 400. <b>Defense power</b> 200. <b>Exp</b> +180. 
<br>`octopus🐙:`  <b>Health</b> 300. <i>It seems like an octopus could find a better occupation than monster. He could be a party planner or master organizer, for example.</i> <b>Attack power</b> 80. <b>Defense power</b> 120. <b>Exp</b> +50. 
<br>`caterpillar-of-phenomenal-power🐛:`  <b>Health</b> 100. <i>This caterpillar is phenomenally powerful; you can feel it from afar.</i> <b>Attack power</b> 20000. <b>Defense power</b> 30. <b>Exp</b> +400. 
<br>`zombie🧟:`  <b>Health</b> 300. <i>Enjoy your undead status while you still can.</i> <b>Attack power</b> 240. <b>Defense power</b> 230. <b>Exp</b> +220. 
<br>`monarch-butterfly 🦋:`  <b>Health</b> 50. <i>Yes, butterflies have numbered days and do not live for long. Don't feel too bad; your days are numbered too.</i> <b>Attack power</b> 30. <b>Defense power</b> 10. <b>Exp</b> +30. 
<br>`evil-shrimp 🦐:`  <b>Health</b> 200. <i>He has malicious intentions. Shrimp always do.</i> <b>Attack power</b> 200. <b>Defense power</b> 70. <b>Exp</b> +90. 
<br>`alien 🛸:`  <b>Health</b> 160. <i>Please be a conspiracy theory. Please be a conspiracy theory! You are not supposed to be real!</i> <b>Attack power</b> 700. <b>Defense power</b> 300. <b>Exp</b> +550. 
<br>`time ⏱:`  <b>Health</b> 100. <i>Our greatest enemy. We will see how true it is that you cannot be conquered.</i> <b>Attack power</b> 1000. <b>Defense power</b> 0. <b>Exp</b> +1000. 
<br>`bad-weather ⛈:`  <b>Health</b> 160. <i>Wait a second! I thought Theseus killed the Minotaur? Oh well. No point in debating it—that's definitely a minotaur, and he looks eager to fight.</i> <b>Attack power</b> 200. <b>Defense power</b> 100. <b>Exp</b> +90. 
<br>`god-of-north-wind 🌬:`  <b>Health</b> 100. <i>He's kinda beautiful, but he keeps blowing a chilly breeze your way. You forgot to bring a sweater, so you are not going to tolerate that kind of behavior.</i> <b>Attack power</b> 800. <b>Defense power</b> 100. <b>Exp</b> +300. 
<br>`umbrella 🌂:`  <b>Health</b> 600. <i>An umbrella; it's notoriously hard to open. </i> <b>Attack power</b> 1000. <b>Defense power</b> 0. <b>Exp</b> +500. 
<br>`fire 🔥:`  <b>Health</b> 200 <i>Stop, drop and roll.</i> <b>Attack power</b>460. <b>Defense power</b> 0. <b>Exp</b> +200. 
<br>`jack-o-lantern 🎃:`  <b>Health</b> 200. <i>He's smirking at you. Go get 'im.</i> <b>Attack power</b> 30. <b>Defense power</b> 20. <b>Exp</b> +45. 

## Guilds 
<br>`Guild of Mages`: Welcome pack has `revival-dove`, `mini-chest`, `money-bag`, `plain-chest`, `golden-chest`, `steel-chest`, and `crown-of-awesome`. New class is `mage`. New state is `unbearably-cool 🤠`. 
<br>`Guild of The Dark Arts`: Welcome pack has `wand`, `potion`, `crystal-ball`, and `portal`. New state is `immortal`. New class is `necromancer`. 
<br>`Guild of the Chronic Procrastinators`: Welcome pack has `tent`, `beer`, `ramen`, `popcorn`, `wine`, `chinese-takeout`, `salt-and-straw-icecream`, and `bed`. New state is `not-ready-for-adult-life`. New class is `warrior`.
<br>`Guild of the Learned`: Welcome pack has `red-book`, `green-book`, 	`orange-book`, and `tome`. New class is `scholar`. New state is `extremely-intellectual🧐`.
<br>`Guild of the Ancients`: Secret guild. 
<br>`Guild of Champions`: Secret guild. 
