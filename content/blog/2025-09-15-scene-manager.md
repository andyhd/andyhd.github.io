Date: 2025-09-17 00:09
Title: A Change of Scene
Summary: Basic scene management in Pygame
Friendly_Date: just after midnight
Tags: gamedev, python, pygame


One of the things I've seen crop up a few times in the
[r/pygame](https://reddit.com/r/pygame) subreddit is people asking how to manage
multiple scenes or screens in their games. This is a common challenge for
beginners, and while there are many ways to approach it, I want to share a
simple method that I think works well for small to medium-sized projects.

We'll start with a bare-bones Pygame program:

```python
import pygame as pg


def run():
    pg.init()
    screen = pg.display.set_mode((800, 600))
    clock = pg.time.Clock()

    while True:
        delta_time = clock.tick(60) / 1000  # seconds since last frame
        events = pg.event.get()

        if any(event.type == pg.QUIT for event in events):
            break

        # Handle input, update game state and render
        screen.fill("black")

        pg.display.flip()

run()
```

Now let's say we want to add a separate title screen and game screen. To do this,
we can factor out the input handling, updating, and rendering into a separate
function for each scene. Each function will take the screen, input events, and
delta time as parameters. The function will return the next scene function to be
called, or return nothing to stay in the current scene.

We'll add these functions and modify the `run` function to allow switching
between them:

```python
import pygame as pg


def title_screen(screen, events, delta_time):
    if any(event.type == pg.KEYDOWN for event in events):
        return play_game

    screen.fill("blue")
    font = pg.Font(None, 30)
    title_text = font.render("Press any key to start", True, "white")
    screen.blit(title_text, title_text.get_rect(center=screen.get_rect().center))


def play_game(screen, events, delta_time):
    if any(event.type == pg.KEYDOWN for event in events):
        return title_screen

    screen.fill("green")


def run(initial_scene):
    pg.init()
    screen = pg.display.set_mode((800, 600))
    clock = pg.time.Clock()
    scene = initial_scene

    while True:
        delta_time = clock.tick(60) / 1000  # seconds since last frame
        events = pg.event.get()

        if any(event.type == pg.QUIT for event in events):
            break

        # Call the current scene function to handle input, update game state,
        # and render to the screen
        next_scene = scene(screen, events, delta_time)

        # Switch to next scene is one was returned
        if next_scene:
            scene = next_scene

        pg.display.flip()

run(title_screen)
```

Now we have a simple scene manager! The `run` function keeps track of the
current scene function and calls it each frame. Each scene function can return
the next scene function to switch to, or return nothing to stay in the current
scene.

This works, but there's a problem. Let's take a closer look at the
`title_screen` function. We're creating a new font object and rendering a new
text surface every time this function is called - which is 60 times per second!
This is really inefficient. We should create the font and text surface only once
when the scene is initialized, and then reuse them every frame. But how?

### Using Closures for Scene State

Instead of our scene functions doing work on every frame, we can split them into
two parts: an outer "factory" function that runs expensive setup code just once,
and an inner function that becomes the actual scene, running every frame.

The inner function, a "closure", can remember and use the variables from the
outer function. You can imagine it as though the inner function packs the scene's
assets and variables into a backpack that it carries around and can use those
variables whenever it needs them.

Let's refactor the code to use this pattern. We'll also add some simple player
movement to the `play_game` scene to make it more interesting:

```python
import pygame as pg


def title_screen():
    font = pg.Font(None, 30)
    title_text = font.render("Press any key to start", True, "white")
    title_rect = title_text.get_rect()

    def _scene(screen, events, delta_time):
        if any(event.type == pg.KEYDOWN for event in events):
            return play_game()

        screen.fill("blue")
        title_rect.center = screen.get_rect().center
        screen.blit(title_text, title_rect)

    return _scene


def play_game():
    player = pg.Rect(400, 300, 50, 50)
    velocity = pg.Vector2(0, 0)

    def _scene(screen, events, delta_time):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return title_screen()
                if event.key == pg.K_LEFT:
                    velocity.x = -200
                if event.key == pg.K_RIGHT:
                    velocity.x = 200
            if event.type == pg.KEYUP and event.key in (pg.K_LEFT, pg.K_RIGHT):
                velocity.x = 0

        player.x += velocity.x * delta_time

        screen.fill("black")
        pg.draw.rect(screen, "white", player)

    return _scene


def run(initial_scene):
    pg.init()
    screen = pg.display.set_mode((800, 600))
    clock = pg.time.Clock()
    scene = initial_scene

    while True:
        delta_time = clock.tick(60) / 1000
        events = pg.event.get()

        if any(event.type == pg.QUIT for event in events):
            break

        # Delegate input handling, game state update and rendering to the
        # current scene function
        next_scene = scene(screen, events, delta_time)

        if next_scene:
            scene = next_scene

        pg.display.flip()


run(title_screen())
```

Our `title_screen` and `play_game` functions now act as factories. They create
the necessary assets and state variables once only, and then return the
inner `_scene` function. The main `run` loop then calls that returned function
every frame.

We also change the way we start the game to *call* `title_screen()` to get the
actual scene function, which has already packed its "backpack" with the font and
text surface, and pass that into `run`. This is much more efficient.

### Sharing State Between Scenes

The scene manager is working well, but what if we need to share information
between scenes? A simple example is a high score that is set in the play scene
and displayed on the title screen. Our current structure doesn't allow for this,
as each scene is completely isolated.

We can solve this by creating a `shared_state` dictionary in our main `run`
function. We can then pass this dictionary as an argument to every scene
function, allowing them to read and write from a common pool of data.

Here is the complete code, updated to include a high score system. You can see
how the `run` function now creates a `shared_state` dictionary and passes it to
the scenes, and how the scenes themselves are updated to use it.

```python
import pygame as pg


def title_screen():
    font = pg.Font(None, 30)
    title_text = font.render("Press any key to start", True, "white")
    title_rect = title_text.get_rect()

    def _scene(screen, events, delta_time, shared_state):
        if any(event.type == pg.KEYDOWN for event in events):
            return play_game()

        screen.fill("blue")
        title_rect.center = screen.get_rect().center
        screen.blit(title_text, title_rect)

        score_text = font.render(f"High Score: {shared_state['high_score']}", True, "white")
        score_rect = score_text.get_rect(centerx=title_rect.centerx, top=title_rect.bottom + 50)
        screen.blit(score_text, score_rect)

    return _scene


def play_game():
    player = pg.Rect(400, 300, 50, 50)
    velocity = pg.Vector2(0, 0)
    font = pg.Font(None, 30)
    scene_state = {"score": 0}

    def _scene(screen, events, delta_time, shared_state):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    scene_state["score"] += 10
                if event.key == pg.K_ESCAPE:
                    shared_state["high_score"] = max(shared_state["high_score"], scene_state["score"])
                    return title_screen()
                if event.key == pg.K_LEFT:
                    velocity.x = -200
                if event.key == pg.K_RIGHT:
                    velocity.x = 200
            if event.type == pg.KEYUP and event.key in (pg.K_LEFT, pg.K_RIGHT):
                velocity.x = 0

        player.x += velocity.x * delta_time

        screen.fill("black")
        pg.draw.rect(screen, "white", player)

        score_text = font.render(f"Score: {scene_state['score']}", True, "white")
        screen.blit(score_text, (10, 10))

    return _scene


def run(initial_scene):
    pg.init()
    screen = pg.display.set_mode((800, 600))
    clock = pg.time.Clock()
    scene = initial_scene
    shared_state = {"high_score": 0}

    while True:
        delta_time = clock.tick(60) / 1000
        events = pg.event.get()

        if any(event.type == pg.QUIT for event in events):
            break

        next_scene = scene(screen, events, delta_time, shared_state)

        if next_scene:
            scene = next_scene

        pg.display.flip()


run(title_screen())
```

Now the player's score will be tracked during the game, and when they return to
the title screen, the high score will be updated if they beat it. This pattern
is very flexible: the `shared_state` dictionary can hold any data you want to
persist across your entire game, while each scene can still have its own
internal state (like the `scene_state` in `play_game`) for temporary data that
should reset every time the scene is entered.

### A Note on Design Patterns

If you're familiar with software design patterns, you may have noticed that this
approach is a functional implementation of the **State Pattern** (or its close
cousin, the **Strategy Pattern**). Our main `run` function acts as the
"Context", and each scene function is a concrete "State". The context delegates
all its work to the current state object, and the states themselves are
responsible for transitioning to other states.

This is of course not limited to a functional style. For those who prefer
object-oriented programming (OOP), the same pattern can be implemented with
classes. Here is a complete, runnable example of how our program would look
using this style:

```python
import pygame as pg


class TitleScene:
    def __init__(self):
        self.font = pg.Font(None, 36)
        self.title_text = self.font.render("Press any key to start", True, "white")
        self.title_rect = self.title_text.get_rect()

    def run(self, screen, events, delta_time, shared_state):
        if any(event.type == pg.KEYDOWN for event in events):
            return PlayScene()

        screen.fill("blue")
        self.title_rect.center = screen.get_rect().center
        screen.blit(self.title_text, self.title_rect)

        score_text = self.font.render(f"High Score: {shared_state['high_score']}", True, "white")
        score_rect = score_text.get_rect(centerx=self.title_rect.centerx, top=self.title_rect.bottom + 50)
        screen.blit(score_text, score_rect)

        # return self to stay in this scene
        return self


class PlayScene:
    def __init__(self):
        self.player = pg.Rect(400, 300, 50, 50)
        self.velocity = pg.Vector2(0, 0)
        self.font = pg.Font(None, 30)
        self.score = 0

    def run(self, screen, events, delta_time, shared_state):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.score += 10
                if event.key == pg.K_ESCAPE:
                    shared_state["high_score"] = max(shared_state["high_score"], self.score)
                    return TitleScene()
                if event.key == pg.K_LEFT:
                    self.velocity.x = -200
                if event.key == pg.K_RIGHT:
                    self.velocity.x = 200
            if event.type == pg.KEYUP and event.key in (pg.K_LEFT, pg.K_RIGHT):
                self.velocity.x = 0

        self.player.x += self.velocity.x * delta_time

        screen.fill("black")
        pg.draw.rect(screen, "white", self.player)

        score_text = self.font.render(f"Score: {self.score}", True, "white")
        screen.blit(score_text, (10, 10))

        # return self to stay in this scene
        return self


def run(initial_scene):
    pg.init()
    screen = pg.display.set_mode((800, 600))
    clock = pg.time.Clock()
    scene = initial_scene
    shared_state = {"high_score": 0}

    while scene is not None:
        delta_time = clock.tick(60) / 1000
        events = pg.event.get()

        if any(event.type == pg.QUIT for event in events):
            break

        scene = scene.run(screen, events, delta_time, shared_state)

        pg.display.flip()


run(TitleScene())

```

#### Which is Better?

For this particular case, I think that closures are the better fit. As
[Jack Diederich pointed out way back at PyCon 2012](https://www.youtube.com/watch?v=o9pEzgHorH0),
if your class has two methods and one of them is `__init__`, you probably don't
need a class. The classes here just add extra boilerplate without providing much
benefit.

However, if you are more comfortable with Object Oriented Programming, as many
people are, the class-based approach works just as well.

### Conclusion

And that's my take on a simple scene manager. It's a pattern I've found useful
for keeping game logic organized without a lot of ceremony. If you find your
game getting more complex, you might want to look into things like a scene stack
for pausing, but for many games, this is all you need. I hope you find it useful
too!

