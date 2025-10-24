Date: 2025-09-12 13:37
Title: Game #1: Pong
Save_as: 1gam/01_pong/index.html
Url: 1gam/01_pong/
Summary: Kicking off my "one game a month" challenge with a classic
Friendly_Date: during an early autumn deluge
Series: 1gam
Tags: gamedev, python, pygame, challenge, tutorial, 1gam, pong


Well, here we are. One game a month, game number one. An apt place to start is
[Pong](https://en.wikipedia.org/wiki/Pong). Allan Alcorn wrote it in 1972 as a
training exercise assigned to him by Atari founder Nolan Bushnell.

### Getting Started with Pygame

I'm already quite familiar with Pygame, but if someone is reading this (hello!)
and you are not, here's a quick intro to writing a game with Pygame.

I'm writing these games in Python, because I like it and I use it every day in
my job. I'll use Pygame, because it's popular and well-documented. There's also
a library called [pygbag](https://github.com/pygame-web) that lets you run
Pygame games in a web browser, but I'll save that for later.

First things first, I need to set up my development environment. I'm using
Python 3.13, which is the latest version at the time of writing (I'm not
counting 3.14, which is still pre-release). I write Python every day for work,
so I already have it installed.

I use the following commands to create a directory and set up a virtual
environment:

```bash
# Create a directory and change into it
mkdir 01_pong && cd $_

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

Next, I install Pygame. I prefer to use the community edition, `pygame-ce`,
which is a fork of the original Pygame library. It has some additional features
and is actively maintained.

```bash
pip install pygame-ce
```

Pygame is a fairly low-level framework which gives you the tools to create
windows, handle input, draw shapes and images, and play sounds. It's not a game
engine, and doesn't provide animation, player control systems or physics
simulation. But it does abstract away the finicky details of memory management
and line drawing algorithms and stuff while leaving everything else to you.

<a name="bare-bones-pygame-program"></a>
A bare-bones Pygame program looks like this:

```python
import pygame


# Initialize Pygame
pygame.init()

# Create a window to display the game
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Game loop
while True:

    # Loop through events (key presses, etc) recorded since the last frame
    for event in pygame.event.get():

        # If the user closes the window, exit the game
        if event.type == pygame.QUIT:
            exit()

    # Update game state (move objects, check collisions, etc)

    # Draw the game
    screen.fill("black")

    # Update the display (this is necessary to see the changes)
    pygame.display.update()
```

This sets up a window and enters a game loop that keeps running until the user
closes it.

Every game is built around this central game loop. On each iteration it does
three main things:

1.  **Handle input:** Check for key presses, mouse clicks, etc.
2.  **Update state:** Move objects, check for collisions, update scores, etc.
3.  **Render:** Draw everything to the screen.

Now that I have the basics set up, I can start building Pong.

### A Tiny GDD for Pong

Before jumping into coding, it's good to have a rough idea of what Pong is and how it
works. Game design documents (GDDs) are a common way to outline the core concepts
and mechanics of a game. They don't have to be long or complex, just enough to
get a clear picture of the game.

Here's a minimal GDD for Pong:

> #### Overview
> A 2D paddle-and-ball game where a player competes against a simple AI
> opponent.  Based on table-tennis, the player tries to hit a ball past the
> opponent's paddle to score points. The first player to reach a set score wins.
> 
> #### Game Mechanics
> - **Core Loop**
>     1. The ball is served from the center of the screen.
>     2. The player moves their paddle vertically to intercept the ball.
>     3. The ball bounces off the paddle.
>     4. The AI opponent attempts to return the ball.
>     5. If a player misses, the opponent scores a point and the ball resets.
>     6. The first player to 10 points wins.
> 
> - **Game Rules**
>     - The ball bounces realistically off the paddles and top and bottom walls.
>     - The ball's speed increases slightly after every successful paddle hit.
>     - The game ends when one side reaches 10 points.
> 
> - **Objects & Entities**
>     - Player Paddle: A white rectangle on the left side, with vertical movement
>       controlled by the player.
>     - AI Paddle: A white rectangle on the right side. Its vertical movement
>       tracks the ball's y-position.
>     - Ball: A white square that moves at a constant initial velocity.
> 
> - **Player Abilities**: Move the paddle up and down within the screen bounds.
>
> #### Controls
> - **Input Scheme**: Keyboard.
>     - Up Arrow: Move paddle up.
>     - Down Arrow: Move paddle down.
> 
> #### Art & Audio
> - **Visual Style**: Extremely minimalist. White geometric shapes (rectangles, square) on a black
>   background.
> 
> - **Sound Design**: Simple, synthesized sounds.
>     - A short beep for ball-paddle and ball-wall collisions.
>     - A distinct, slightly higher-pitched sound for scoring a point.
> 
> - **Music**: None.
> 
> #### Technical
> - **Engine/Framework**: Python 3 with the Pygame library.
> - **Platform(s)**: Desktop (Windows, macOS, Linux).
> 
> #### Scope
> - **Must Have**
>     - A functional game window.
>     - Player paddle controlled by keyboard input.
>     - A basic AI paddle that tracks the ball.
>     - Ball with correct collision physics for paddles and walls.
>     - A visible score display that updates correctly.
>     - A win condition that ends the game.
> 
> - **Nice to Have**
>     - A simple start screen (e.g., "Press Space to Start").
>     - Sound effects.
>     - A local two-player mode.

### The Plan of Attack

Alright, here's how I'm going to build this thing, piece by piece. This seems
like a sensible order, starting with the basics and adding complexity one step
at a time.

1. [Draw the Game Elements](#step-1)
2. [Implement Player Control](#step-2)
3. [Get the Ball Moving](#step-3)
4. [Collisions](#step-4)
5. [Keep Score](#step-5)
6. [A Worthy Opponent](#step-6)
7. [The Finish Line](#step-7)
8. [Polish](#step-8) or "The last 10% that takes 90% of the time"

### Draw the Game Elements {#step-1}

First, I'll get the basic shapes on the screen. This means creating
`pygame.Rect` objects for the player paddle, the opponent paddle, and the ball,
and then drawing them in the main loop. They won't move, but it's a start.
We'll have a black screen with three white rectangles.

Starting with the [bare-bones Pygame program](#bare-bones-pygame-program)
listed above, let's define the paddles as `pygame.Rect` instances. I'll add this
just before the start of the game loop:

```python
# Define player paddles
paddle = pygame.Rect(0, HEIGHT // 2 - 50, 20, 100)
players = [paddle, paddle.move_to(right=WIDTH)]
```

This creates the first player paddle as a 20 pixel wide, 100 pixel high
rectangle. The y position is set to half the screen height minus half the paddle
height (50 pixels), which will center the paddle vertically on the left of the
screen (x = 0).

Then it adds this to a list of players, with a copy moved to the
opposite side of the screen as the second player.

Next, I'll add the ball, which will start at the center of the screen:

```python
# Define ball
ball = pygame.Vector2(screen.get_rect().center)
```

Now to draw them all on each frame. Inside the game loop, just after the screen
is filled with black, I can draw the paddles and the ball with the `pygame.draw`
functions:

```python

    # Draw the paddles
    for player in players:
        pygame.draw.rect(screen, "white", player)

    # Draw the ball
    pygame.draw.circle(screen, "white", ball, radius=10)
```

Now when I run the program, I see a black window with two white paddles on
either side of the screen and a white ball in the center. Progress!

![Drawing the paddles and ball]({static}v1.png){width="100%"}

### Implement Player Control {#step-2}

Next, I'll make the player's paddle move. I'll read the keyboard state for the
up and down arrow keys inside the game loop and update the y-position of the
player's `Rect`. I'll also add bounds checking to make sure the paddle can't
go off the screen.

I don't want the game to run faster than 60 frames per second, or else the ball
will move too fast to be playable. So I'll add a clock to limit the frame rate.
This goes just after creating the game window:

```python
# Create a clock to limit the frame rate
clock = pygame.time.Clock()
```

As each frame is 1/60th of a second, the distance moved per frame is a fraction
of a pixel, so I need to update the paddles to use `pygame.FRect` instead of
`pygame.Rect`. I'll change the paddle definition to:

```python
paddle = pygame.FRect(0, HEIGHT // 2 - 50, 20, 100)
```

I'll define a mapping of control names to keyboard keys so that the handling
code is easier to read and they are easy to change later if needed. This goes
after the players are defined and before the game loop:

```python
# Define controls
controls = {
    "move_paddle_up": pygame.K_UP,
    "move_paddle_down": pygame.K_DOWN,
}
```

I'll also define a list to hold the vertical speed of each paddle:

```python
# Define player speeds
player_speeds = [0, 0]
```

Then, at the start of the game loop, I'll tick the clock to limit the frame rate
and get the time since the last frame in seconds:

```python
    # Limit frame rate to 60 FPS
    delta_time = clock.tick(60) / 1000
```

Then, inside the game loop, in the inner loop where I check for events, I'll
check for these key presses and set the paddle's velocity accordingly:

```python
        # If user presses a key, check if it's a control key
        if event.type == pygame.KEYDOWN:
            if event.key == controls["move_paddle_up"]:
                player_speeds[0] = -600
            elif event.key == controls["move_paddle_down"]:
                player_speeds[0] = 600

        # If user releases a key, stop moving the paddle
        if event.type == pygame.KEYUP:
            if event.key in (controls["move_paddle_up"], controls["move_paddle_down"]):
                player_speeds[0] = 0
```

Finally, after handling events but before drawing, I'll update the paddle's
position based on its speed and the time since the last frame. This makes:

```python
    for player, speed in zip(players, player_speeds):
        player.y = pygame.math.clamp(player.y + speed * delta_time, 0, HEIGHT - player.height)
```

I'm looping through each player so that I can easily add AI control for the
second paddle later. The `clamp` function ensures the paddle stays within the
screen bounds.

And that's it! Now I can move the left paddle up and down with the arrow keys.


### Get the Ball Moving {#step-3}

The paddle may move now, but the ball is tantalizingly frozen in the centre of
the screen - not much fun. I'll get the ball moving by giving it a velocity
vector and adding this to its position in each frame.  Then I'll implement the
top and bottom wall collisions, which just means reversing the ball's vertical
velocity if it hits the edge of the screen.

Earlier I used a `pygame.Vector2` to represent the ball, but I want to take
advantage of the API provided by `pygame.Rect`, so I'll change it to a
`pygame.FRect` (a floating-point version of `pygame.Rect`). It needs to be an
`FRect` because when the ball moves at an angle, its x and y velocities will be
fractions of its speed. For example, at a speed of 1 pixel per frame and a 45
degree angle, the ball will move _cos 45&deg;_ pixels horizontally and _sin
45&deg;_ pixels vertically (about 0.7 pixels each).  I will also need to store
the ball's radius, so that I can draw it and use it in collision detection.

```python
# Define ball
ball_radius = 8
ball = pygame.FRect(0, 0, ball_radius * 2, ball_radius * 2)
```

The ball also needs a velocity vector - this is initially set to zero.

```python
ball_velocity = pygame.Vector2(0, 0)
```

And I'll also store the speed at which the ball moves:

```python
ball_speed = 600  # pixels per second
```

Now to get the ball moving. If the ball's velocity is zero, I'll serve it from
the center of the screen at a random angle. I'll need a random number generator
function for this, so I need to import the `random` module at the top of the
file:

```python
import random
```

Then I'll add the check for zero velocity just after updating the paddle
positions:

```python
    # If the ball is stationary, serve it from the center at a random angle
    if not ball_velocity:
        ball.center = screen.get_rect().center
        ball_velocity = pygame.Vector2(ball_speed, 0).rotate(random.randint(0, 360))
```

Next I'll update the ball's position based on its velocity and the time since
the last frame:

```python
    # Update ball position
    ball.center += ball_velocity * delta_time
```

Finally, I'll add collision detection for the top and bottom walls. If the ball
hits either wall, I'll reverse its vertical velocity:

```python
    # Check for collision with top and bottom walls
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_velocity.y *= -1
```

Now when I run the program, the ball serves from the center at a random angle,
bouncing off the top and bottom walls. But it doesn't interact with the paddles
yet, so it will just go off the left or right edge of the screen and disappear.
Let's fix that next.

### Paddle and Ball Collisions {#step-4}

This is the core of the game. When the ball hits a paddle it needs to bounce
back. And it can't be a simple reflection like bouncing off the walls - that
would be boring. I need to make the bounce angle change depending on where the
ball hits the paddle, so that the player can control the ball's trajectory. This
won't be a perfect simulation of real-world physics, but it will be good enough
to give the player more agency and hopefully make the game fun.

Just after the check for wall collisions, I'll add the paddle collision
detection:

```python
    for player_on_right, player in enumerate(players):
        if ball.colliderect(player):

            # Get the normalized offset of the ball relative to the paddle center
            offset = (ball.centery - player.centery) / (player.height / 2 + ball_radius)

            # Set the ball angle based on the offset
            angle = offset * MAX_RETURN_ANGLE
            if player_on_right:
                angle = 180 - angle

            # Update ball velocity
            ball_velocity = pygame.Vector2(ball_speed, 0).rotate(angle)
```

This code loops through each paddle and checks if the ball collides with it. If
it does, it calculates the offset of the ball's center from the paddle's center,
normalizes it to a value between -1 and 1, and then uses that to set the angle
of the ball's new velocity vector. The `MAX_RETURN_ANGLE` constant defines the
maximum angle the ball can be returned at, which I'll define at the top of the
file:

```python
MAX_RETURN_ANGLE = 75  # degrees
```

I think this bounce angle calculation is close to how the original Pong worked,
but another way to do it would be to reverse the horizontal velocity, add a
fraction of the offset to the vertical velocity and then normalize the vector to
the ball's speed, eg:

```python
    for player in players:
        if ball.colliderect(player):
            offset = (ball.centery - player.centery) / (player.height / 2 + ball_radius)
            ball_velocity.x *= -1
            ball_velocity.y += offset * 0.5
            ball_velocity = ball_velocity.normalize() * ball_speed
```

This would give a more gradual change in angle, but doesn't limit the maximum
angle like the first approach. I think I prefer the greater control over the
ball that the first approach gives.

Now the ball bounces off the paddles at different angles depending on where it
hits.  It still goes off the left and right edges of the screen if it misses
either paddle, and nothing happens when that occurs. I'll fix that next.

### Keep Score {#step-5}

Let's avoid the game becoming unplayable when the ball leaves the screen. I'll
add checks for when the ball has gone past the left or right edge of the screen
and if it has, I'll increment the appropriate player's score, reset the ball to
the center, and serve it again. The score also needs to be displayed on the
screen.

To keep track of the score, I'll define a list to hold the scores for each
player:

```python
# Define score
score = [0, 0]
```

To display the score, I'll need to initialize a font. I'll do this next, just
using the default font at a large size:

```python
score_font = pygame.font.Font(None, 74)
```

Just after the screen is cleared, I'll render the score text and draw it to the
screen. Doing this before drawing the paddles and ball means the score will be
in the background. I'll center it at the top of the screen:

```python
    # Draw the score
    score_text = score_font.render(f"{score[0]}   {score[1]}", True, "white")
    screen.blit(score_text, score_text.get_rect(center=(WIDTH // 2, 50)))
```

Next, I'll add the checks for when the ball goes off the left or right edge of
the screen. This goes just after the paddle collision detection:

```python
    # Check for scoring
    if ball.right < 0 or ball.left > WIDTH:
        score[ball.right < 0] += 1
        ball_velocity = pygame.Vector2(0, 0)
```

If the ball's right edge is less than zero, it has gone off the left side of
the screen, so the right player scores a point. If the ball's left edge is
greater than the screen width, it has gone off the right side, so the left
player scores. The expression `score[ball.right < 0]` uses the boolean value
`ball.right < 0` as an index (0 or 1) to increment the correct player's score.
Finally, the ball's velocity is set to zero to stop it moving, which will cause
it to be served again from the center on the next frame.

Now the score is shown on the screen, it updates correctly when a player misses
the ball, and the ball is served again from the center. Next, I'll add the AI so
that the game isn't completely one-sided.


### A Worthy Opponent {#step-6}

Now to make the opponent paddle move. The AI will be simple: it will try to
keep its center aligned with the ball's center. To avoid making it too good,
I'll limit its speed so that it can't always catch the ball.

First, I'll define the AI paddle's speed at the top of the file:

```python
ai_paddle_speed = 400  # pixels per second
```

Then, inside the game loop, after updating the player's paddle position, I'll
add the AI logic to update the opponent's paddle position. We'll make it react
only when the ball is above or below the paddle. This should give it a slightly
delayed reaction time, hopefully making it easier for the player to score.

```python
    # Simple AI for the second paddle
    player_speeds[1] = ai_paddle_speed * (
        (ball.centery > players[1].bottom) - (ball.centery < players[1].top)
    )
```

That will do for now, but I think it could be improved. I would like to be able
to "wrong-foot" the AI by changing the ball's angle sharply, but that will
require adding acceleration to the paddles so they can't instantly change
direction.


### The Finish Line {#step-7}

For now, the game keeps going forever. Let's add a win condition. After each
point is scored, I'll check if either player has reached 10 points. If so, the
game ends. For now, we can just display a message on the screen and stop
updating the game loop.

First, I'll define the winning score and which player is the winner at the top
of the file:

```python
winning_score = 10
winner = None
```

Then, just after updating the score when a player misses the ball, I'll check
if either player has reached the winning score. If they have, I set the `winner`
and stop the ball moving:

```python
        # Check for winning condition
        if max(score) >= winning_score:
            winner = score.index(max(score)) + 1
            ball_velocity = pygame.Vector2(0, 0)
```

If we have a winner, I'll display a message on the screen. I'll do this after
all other drawing, so that it appears on top:

```python
    # Draw the winning message
    if winner:
        win_text = score_font.render(f"Player {winner} wins!", True, "white")
        screen.blit(win_text, win_text.get_rect(centerx=WIDTH // 2, y=HEIGHT // 2 - 100))
```

Finally, to stop the game from serving the ball again after someone has won,
I'll wrap the ball serving code in a check for `winner`:

```python
    # Initialize the ball if it's stationary
    if not ball_velocity:
        ball.center = screen.get_rect().center
        if not winner:
            ball_velocity = pygame.Vector2(ball_speed, 0).rotate(random.randint(0, 360))
```

And that's it! The game is playable from start to finish. But it still needs a
lot of work: once you win there's no way to restart, the AI is too good, there
are no sound effects, and it could do with a bit of polish. Also, I haven't done
all the things listed in the GDD, like gradually increase the speed of the ball.

### Polish {#step-8}

#### Sound Effects

If the core game is working, I'll add the sound effects from the GDD. A simple
beep for collisions will make the game feel much more responsive.

I created some simple sound effects using [Bfxr](https://www.bfxr.net/), which
is a great tool for making retro-style sound effects. I made three sounds:
- A "blip" sound for ball-paddle collisions
- A "bloop" sound for ball-wall collisions
- A "ping" sound for scoring a point

I saved these as WAV files in the same directory as my Python source file.
Then I load them at the top of the file, just after initializing Pygame. I will
use `pathlib.Path` to get the directory of the current script and ensure the
paths work on all platforms. So I need to import `pathlib` at the top:

```python
import pathlib
```

Then I can load the sounds:

```python
# Load sound effects
script_dir = pathlib.Path(__file__).parent
paddle_sound = pygame.mixer.Sound(script_dir / "blip.wav")
wall_sound = pygame.mixer.Sound(script_dir / "bloop.wav")
score_sound = pygame.mixer.Sound(script_dir / "ping.wav")
```

Then I play the appropriate sound effect at each event. For paddle collisions,
just after updating the ball velocity, eg:

```python
            # Play paddle hit sound
            paddle_sound.play()
```

For wall collisions, just after reversing the vertical velocity, and for
scoring, just after updating the score.

#### Restarting the Game

Once a player has won, there's no way to restart the game. I'll add a simple
restart mechanism: when the game is over, pressing the space bar will reset
the scores and start a new game. I'll also wait for the player to press space to
start the first game.

First, I'll add a new control for restarting the game:

```python
    "restart_game": pygame.K_SPACE,
```

I'll need a way to track whether the game is over, so I'll add a new variable:

```python
game_started = False
```

Then, in the event handling loop, I'll check for this key press and reset the
game state if the game is not already running:

```python
        if event.type == pygame.KEYDOWN:
            if event.key == controls["restart_game"] and not game_started:
                score = [0, 0]
                winner = None
                game_started = True
```

I'll need to tweak the ball serving code to only serve the ball if the game has
started:

```python
    # Initialize the ball if it's stationary
    if not ball_velocity:
        ball.center = screen.get_rect().center
        if game_started and not winner:
            ball_velocity = pygame.Vector2(ball_speed, 0).rotate(random.randint(0, 360))
```

And I need to make sure the game is marked as not started when someone wins:

```python
    # Check for winning condition
    if max(score) >= winning_score:
        winner = score.index(max(score)) + 1
        ball_velocity = pygame.Vector2(0, 0)
        game_started = False
```

Finally, I'll add a message to the screen prompting the player to press space to
start a game. I'll do this in the drawing section, just after drawing the
winning message:

```python
    # Draw the start message
    if not game_started:
        start_text = score_font.render("Press SPACE to start", True, "white")
        screen.blit(start_text, start_text.get_rect(centerx=WIDTH // 2, y=HEIGHT // 2 + 50))
```

### Publish!

Unbelievably, I am running out of time to get this game published within the
month, so I will stop polishing and call it done.

As I mentioned at the start, I will be using pygbag to publish to the web, so I
need to follow the [pygbag README](https://pygame-web.github.io/).

To get it working with pygbag, I need some changes:

#### Convert sound files to OGG

Pygbag only supports OGG files, so I need to convert my WAV files to OGG. I used
[FreeConvert](https://www.freeconvert.com/wav-to-ogg) to do this. I also moved
the code that loads the sound files to the top of the file, just after the
imports.

```python
# Load sound effects
assets = Path(__file__).parent
paddle_sound = pygame.mixer.Sound(assets / "blip.ogg")
wall_sound = pygame.mixer.Sound(assets / "bloop.ogg")
score_sound = pygame.mixer.Sound(assets / "ping.ogg")
```

#### Put all code into an asynchronous function

Pygbag requires the main game code to be in an async function. I'll need to run
this function using `asyncio.run()`, so I need to import the `asyncio` module at
the top of the file.

```python
import asyncio
```

I will move all the code into an asynchronous function definition:

```
async def main():

    # Initialize Pygame
    pygame.init()

    # ... all the code ...
```

The pygbag documentation says that the main loop needs to call
`asyncio.sleep(0)` once per frame to allow other tasks to run. So I'll add that
inside the game loop at the end:

```python
        # Allow other tasks to run
        await asyncio.sleep(0)
```

Finally, to run the game when the script is executed, I need to call
`asyncio.run(main())` at the end of the file:

```python
# Run the game
asyncio.run(main())
```

I also needed to change the `exit()` call to `return` to exit the `main()`
function:

```python
            if event.type == pygame.QUIT:
                return
```

#### Build with pygbag

Pygbag needs the game code to be in a file named `main.py`, so I created a
directory called `dist` and saved my code in `dist/main.py`. I also copied the
OGG sound files into the `dist` directory.

Now I can install pygbag in my virtual environment:

```bash
pip install pygbag
```

Then I can build the web version:

```bash
python -m pygbag --build dist
```

This creates the `dist/build` directory containing an `index.html` file and all the
other files needed to run the game in a web browser. I can test it locally by
running pygbag without the `--build` option and browsing to
`http://localhost:8000`:

```sh
python -m pygbag dist
```

Then I can upload the contents of the `build/web` directory to my web server and
you can play it right here!

[Play Pong](https://andydriver.net/pygame_pong/){.btn}

### Conclusion

And there we have it, my first game in the "one game a month" challenge. Pong is
a simple game, but it covers a lot of the basics of game development.

There's actually a bug where the ball can get stuck at the top or bottom of the
screen, so I'll need to fix that in a future update. I also want to tweak the AI
because it is a bit too good to be fun. But overall, I'm quite pleased that I've
managed to actually publish a game within the month in spite of a busy day job,
parenting duties, and my perennial struggle with procrastination!
