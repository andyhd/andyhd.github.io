Date: 2025-10-04 16:39
Title: Cover Your Assets
Summary: A simple asset loader for Pygame
Friendly_Date: in the aftermath of Storm Amy
Tags: gamedev, python, pygame


Pygame provides functions for loading images, fonts, and sounds, which make it
easy to get assets into your game. But it doesn't provide any guidance or a
standard way to manage and organize these assets. This is left up to you, and
something I have often seen is how this can lead to repetitive code or
"boilerplate".

I'm sure if you've used Pygame before, you will recognise this block of asset
loading code at the top of a file:

```python
import pygame as pg

pg.init()
screen = pg.display.set_mode((800, 600))

# Load player image
player_image = pg.image.load("assets/images/player.png").convert_alpha()

# Load enemy images
num_enemy_types = 4
enemy_images = [
    pg.image.load(f"assets/images/enemy{i}.png").convert_alpha()
    for i in range(num_enemy_types)
]

# Load sound effects
pew_pew = pg.mixer.Sound("assets/sounds/pew_pew.wav")

# Load font
clock_font = pg.font.Font("assets/fonts/clock.ttf", 32)

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            pew_pew.play()

    screen.fill("black")

    screen.blit(player_image, (400, 500))

    for i, img in enumerate(enemy_images):
        for x in range(50, 750, 100)
            screen.blit(img, (x, i * 50))

    clock_text = "Time: {0:02}:{1:02}".format(*divmod(pg.time.get_ticks() // 1000, 60))
    screen.blit(clock_font.render(clock_text, True, "white"), (10, 10))

    pg.display.flip()
```

This works of course, but when your project grows it can become difficult to
manage your assets, especially if asset loading is spread throughout your
codebase, and you could end up loading the same asset multiple times, wasting
memory and resources.

Wouldn't it be nice if we could delegate to an "asset manager" that we could
point at a directory of assets and then just ask it for them by name and let
it take care of loading and caching?

Some requirements could be:

- Load assets from a specified directory
- Support different asset types (images, sounds, fonts)
- Only load assets when they are first requested
- Cache assets to avoid redundant loading
- Provide a simple interface for accessing assets by name
- Allow for easy extension to support new asset types

Let's imagine what using such an asset manager could look like in practice:

```python
from pathlib import Path

import pygame as pg

from utils import asset_loader

pg.init()
screen = pg.display.set_mode((800, 600))

images = asset_loader(Path("assets/images"))
sounds = asset_loader(Path("assets/sounds"))
fonts = asset_loader(Path("assets/fonts"))

num_enemy_types = 4

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            sounds("pew-pew").play()

    screen.fill("black")

    screen.blit(images("player"), (400, 500))

    for i in range(num_enemy_types):
        for x in range(50, 750, 100)
            screen.blit(images(f"enemy{i}"), (x, i * 50))

    clock_text = "Time: {0:02}:{1:02}".format(divmod(pg.time.get_ticks() // 1000, 60))
    screen.blit(fonts("clock", 32).render(clock_text, True, "white"), (10, 10))

    pg.display.flip()
```

Now _that_ feels much better. All the loading logic is abstracted away, we just
ask for assets by a simple name, and we don't have to worry about the details
for the most common cases. It's clear and concise, and lets us focus on the fun
parts of making a game.

So, how do we build it? The complete function is surprisingly short. Let's take
a look at the code, and then we'll break down the key concepts that make it
work.

```python
from collections.abc import Callable, Mapping
from functools import lru_cache, partial
from pathlib import Path
from typing import Concatenate

import pygame as pg

Asset = pg.Surface | pg.mixer.Sound | pg.Font
AssetLoader = Callable[Concatenate[str, ...], Asset]
AssetLoaderMap = Mapping[str, AssetLoader]

IMAGE_EXTS = ".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp"  # etc
AUDIO_EXTS = ".ogg", ".wav", ".mp3"
FONT_EXTS = ".ttf", ".otf"

ASSET_LOADERS = (
    {_: lambda path: pg.image.load(path).convert_alpha() for _ in IMAGE_EXTS}
    | {_: pg.mixer.Sound for _ in AUDIO_EXTS}
    | {_: partial(pg.font.Font, path) for _ in FONT_EXTS}
)


def asset_loader(path: Path, loaders: AssetLoaderMap = ASSET_LOADERS) -> AssetLoader:
    if not path.is_dir():
        raise ValueError(f"Not a directory: {path}")

    @lru_cache
    def get_asset(name: str, *args, **kwargs) -> Asset:
        if not (asset := next(path.glob(f"{name}.*"), None)):
            raise LookupError(f"Asset not found: {path / name}")

        if not (load_fn := loaders.get(asset.suffix.lower())):
            raise LookupError(f"No loader for asset type: {asset.suffix}")

        return load_fn(asset, *args, **kwargs)

    return get_asset
```

### Made to Order

This `asset_loader` is a factory function takes a directory path and returns a
`get_asset` function. If you have read my previous post on [how to code a simple
scene manager][1], you will recognise this pattern and probably are starting to
suspect that I like it. It is a powerful pattern that in this case allows us to
create separate loaders for different asset types or directories. It also means
we do not have to pass the directory path every time we want to load an asset.

### Laziness is a Virtue

Another benefit of this approach is that assets are only loaded when they are
first requested. If an asset is never used, it is never loaded, which keeps
memory usage down.

### Cache is King

We're also using the [`functools.lru_cache` _decorator_][2] from Python's standard
library, our secret weapon that gives our `get_asset` function a memory.  The
first time you ask for an asset, it does the work of loading the file into
memory and decompressing and parsing the data, ready to use. Then it remembers
that result and each time you ask for the same asset after that it just returns
the saved copy. Performance win for one line of code? Nice!

### Embrace and Extend

The `ASSET_LOADERS` dictionary maps file extensions to their respective loading
functions. This makes it easy to add support for new asset types by simply
adding new entries to the dictionary. For example, if you wanted to add support
for JSON data files, you could do something like this:

```python
import json

ASSET_LOADERS[".json"] = lambda path: json.loads(path.read_text())
```

And then you could create a data loader:

```python
data = asset_loader(Path("assets/data"))
game_config = data("config")  # loads assets/data/config.json
```

Additionally, we have left room for customization by allowing additional
arguments to be passed to the asset loading functions. This is particularly
useful for fonts, where you also need to specify the font size when loading.

And finally, we can override the default loaders by passing a custom `loaders`
mapping to the `asset_loader` function if we want to change how certain asset
types are loaded. For example, if we wanted to load background music as a
streaming music track instead of a sound effect, we could do something like this:

```python
def load_music(path: Path):
    pg.mixer.music.load(path)
    return pg.mixer.music  # return the music module for playback control

music = asset_loader(
    Path("assets/music"),
    loaders={".ogg": load_music},
)

# Then load music like this:
music("background").play(loops=-1)  # loads assets/music/background.ogg
```

### A Clean Slate

This approach keeps your asset loading code clean and organized, reduces
redundancy, and makes it easy to manage your game's assets as your project
grows. It is intentionally simple, but provides a lot of benefit for small to
medium-sized projects. For larger projects, you might want to consider more
sophisticated asset management solutions, but in my experience, this pattern
covers most use cases without adding unnecessary complexity.


[1]: /a-change-of-scene.html
[2]: https://docs.python.org/3/library/functools.html#functools.lru_cache
