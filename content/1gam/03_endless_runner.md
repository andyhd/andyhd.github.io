Date: 2025-10-21 13:37
Title: Game #3: Eterniski
Save_as: 1gam/03_endless_runner/index.html
Url: 1gam/03_endless_runner
Summary: It's all downhill from here!
Friendly_Date: on a rainy Tuesday afternoon
Series: 1gam
Tags: gamedev, python, pygame, challenge, tutorial, 1gam


It's month 3 of my [one game a month challenge][1] and the compound interest is
already starting to pay off.  The utility functions I built for the first two
games have become a proto-toolkit. I can now focus less on boilerplate and more
on the fun parts - the gameplay and art.

This game will be an [endless runner][2]. Let's do a mini-[GDD][3]:


## Fresh Powder

![Concept sketch of Eterniski]({static}eterniski-concept.png){width=400px, style="float: right; margin: 0 0 1em 1em"}

You control a skiier slaloming down an endless mountain. The goal is
to get as far as possible without hitting an obstacle, or falling.

I want to capture the feeling of speed and "flow state", navigating the
obstacles with fluid, precise movements.

### The "Must-Have"s
  - Top-down view
  - The world view scrolls upwards continuously, with new obstacles appearing
    from the bottom of the screen
  - Player can steer the character left and right and slow down (and stop) or speed up (to
    a maximum speed) using keyboard or joystick controls
  - Moving objects sometimes appear from the left or right edges of the
    screen and travel horizontally at a constant speed
  - If the player collides with an obstacle or falls into the river, the game is over
  - Score based on distance travelled, slalom gates passed, and speed multiplier
  - Player sprite is animated:
    - directional facing - 45 degree increments
    - ski poles pushing at slow speeds when accelerating
    - aerodynamic tuck when speeding up
    - dying when colliding or falling in crevasse
  - Looping background music
  - Sound effects for skiing, getting hit, etc.

### The "Nice-to-Have"s
  - Extra lives - ie, player can get hit a certain number of times before game
    over
  - Different character skins to choose from
  - Power-ups that give temporary invincibility or speed boosts
  - Leaderboard to track high scores
  - Tricks - player can perform tricks for extra points


## Ski Wax

My growing stable of utility functions is already accelerating my development:

This game will have a few different screens (title, gameplay, high score entry
and leaderboard) so I will be using my [scene manager][4] from [Loco
Lift Rush](/pyweek-40-part-2-submission). I don't have to think about how to set
up the different screens or transition between them, I can just focus on the content.

My [asset loader][5] now manages the loading and caching of sprites
and sounds. I can just put the assets in a folder and reference them by name.
For this game, I think I'll need to extend it a bit to handle [spritesheets][7]
for the animations.

And my [input handler][6] enables handling joystick controls from the start,
which will be crucial to capturing the fluid, analogue "flow state" I'm aiming
for.


## Black Diamond

The first new challenge is animating the player character in multiple states,
which is a big change from the static sprites of Loco Lift Rush.  Learning from
that game, I will stay away from drawing pixel art, and stick to digitising
hand-drawn art. This should help me make decent-looking assets in a shorter
time.

Second, Music! I plan to use the simple sequencer [Bosca Ceoil][7], which I've
mentioned before. I have actually played around with it a bit, so I'm not
wasting time learning a new tool from scratch. The huge challenge will be
composing something that is pleasant and loops well, and doesn't drive me crazy
while playing the game!

Lastly, the technical challenge of generating the endless piste. While the scope
is (intentionally) limited to snowy mountains with trees and rocks, I still want
some variety in the obstacles and scenery to keep things interesting.  The
slalom gates also need to be fairly placed so that the player has a chance of
passing through them. The algorithm I come up with for this will need to balance
randomness with playability.


## Piste Map

To keep myself on track, I will break down the development into weekly goals:

 * **Week 1**. Player movement and basic scrolling world, obstacles, collision
   detection

 * **Week 2**. Scoring, animation, sound effects

 * **Week 3**. Music!

 * **Week 4**. Polish, bug fixing, extra features if time


## Après Ski

My goal for this month is not just to build a game, but to expand my toolkit for
building future games. I'm already feeling the benefits.  Growing the capital
of reusable code and honed processes means I can be more ambitious with each
game in this challenge.


[1]: /1gam
[2]: https://en.wikipedia.org/wiki/Endless_runner
[3]: https://en.wikipedia.org/wiki/Game_design_document
[4]: /a-change-of-scene
[5]: /cover-your-assets
[6]: /control-yourself
[7]: https://yurisizov.itch.io/boscaceoil-blue

