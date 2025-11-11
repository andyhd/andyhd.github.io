Date: 2025-11-05 21:23
Title: Choking on My Own Dog Food
Summary: A small example of refactoring some Python code.
Friendly_Date: after the excitement of Fireworks Night
Tags: gamedev, python, pygame


Code is rarely _done_. You find gaps, requirements change, and you adjust.
[Refactoring][8] is part of the job.

I have been [eating my own dog food][6] - specifically, using [my customisable
control system][3] in my latest game for [one game a month challenge][2] - and
realised it is missing an important ingredient.


## Square Meal

This system maps input events (keys, buttons) to action names like “jump” or
“move left.” It’s simple and lets you reconfigure controls without changing game
code.

Here is an example of mapping input events to actions:

```python
get_actions = controls.bind({
    "jump": [pg.Event(pg.KEYDOWN, key=pg.K_SPACE)],
    "move_left": [pg.Event(pg.KEYDOWN, key=pg.K_LEFT)],
    "move_right": [pg.Event(pg.KEYDOWN, key=pg.K_RIGHT)],
})
```

In the game loop, we check for these actions like this:

```python
for action in get_actions(pg.event.get()):
    if action == "jump":
        player.jump()
    if action == "move_left":
        player.move_left()
    if action == "move_right":
        player.move_right()
```

This separates the details of input handling from the game logic, making it easy
to change the controls.


## Taste for More

In my new game, [Eterniski][1], I want steering to feel natural: small tilts for
gentle turns, full tilt for fast carves. That needs analog input, not just on/off.

Pygame generates `JOYAXISMOTION` events whenever the stick moves. These contain
the axis index (e.g. 0 for horizontal, 1 for vertical) and a `value`
representing tilt, which ranges from `-1.0` (full tilt left or up) to `1.0`
(full tilt right or down).[^1]

The current `bind` returns only action strings, so metadata like joystick tilt
(`event.value`) or mouse position (`event.pos`) is lost.


## Refining the Recipe

It was obvious that I needed to refactor the control system to supply the event
metadata alongside the action name.

My first thought was [KISS][7]: stick to built-in types and return a list of
tuples, where each tuple contains the action string and the event object that
triggered it.

But a clearer, more type-safe approach would be to define an `Action` dataclass
which has a name (e.g. "move right") and blends in the event metadata, like
joystick tilt. And we can make it immutable by freezing the dataclass.

A custom class makes intent clear in type hints, e.g.
`map_events_to_actions(events: list[Event]) -> list[Action]`.

Copying the event metadata into the `Action` class integrates seamlessly with
[the `match` statement][4], as it was made for exactly this kind of situation.
[Class patterns][5] let you match on the action name and pull out event metadata
in one go, which makes the code easy to read.

For a small tidy-up, we can also define `__match_args__` on the class to set
`name` as the first positional argument, letting us skip typing `name=` in the
class pattern.

Here is the updated control system module with the new `Action` class:

```python
from collections.abc import Callable
from dataclasses import InitVar, dataclass
from typing import Any

import pygame as pg


@dataclass(frozen=True)
class Action:
    name: str
    event: InitVar[pg.Event]
    __match_args__ = ("name",)

    def __post_init__(self, event: pg.Event):
        for key, value in event.__dict__.items():
            object.__setattr__(self, key, value)


ActionMapper = Callable[[list[pg.Event]], list[Action]]


def bind(mapping: dict[str, list[pg.Event]]) -> ActionMapper:

    def get_action(event: pg.Event) -> str | None:

        def match_attribute(attr_name: str, value: Any) -> bool:
            if callable(value):
                return value(getattr(event, attr_name))
            return getattr(event, attr_name) == value

        for action, template_events in mapping.items():
            if any(
                event.type == template_event.type
                and all(
                    match_attribute(attr_name, value)
                    for attr_name, value in template_event.__dict__.items()
                )
                for template_event in template_events
            ):
                return action
        return None

    def map_events_to_actions(events: list[pg.Event]) -> list[Action]:
        return [
            Action(name=action, event=event)
            for event in events
            if (action := get_action(event))
        ]

    return map_events_to_actions
```

With this change in place, we can define our joystick bindings like this:

```python
get_actions = controls.bind({
    "move_left": [pg.Event(pg.JOYAXISMOTION, axis=0, value=lambda v: v < -0.1)],
    "move_right": [pg.Event(pg.JOYAXISMOTION, axis=0, value=lambda v: v > 0.1)],
    "jump": [pg.Event(pg.JOYBUTTONDOWN, button=0)],
})
```

And we can update the game loop code and use pattern matching to handle the
actions:

```python
for action in get_actions(pg.event.get()):
    match action:
        case Action("move_left", value=value):
            player.turn_left(value)
        case Action("move_right", value=value):
            player.turn_right(value)
        case Action("jump"):
            player.jump()
```

The game can read tilt values directly, so turning is smooth and responsive.
Discrete and analog inputs both work, and the code is clear.

## Chef's Kiss

The first `bind` worked, until using it in a new game exposed its limits.
Carrying event metadata with the action enables both discrete and analog
controls.

**Good code adapts**.


[^1]: I'm omitting the `instance_id` attribute, which specifies which joystick
    the event came from, for simplicity. In a real game, you would want to check
    this to be able to handle multiple joysticks. There is also a `joy`
    attribute which did the same thing before Pygame 2.0.0, but is now
    deprecated.

[1]: https://pyweek.org/everything/eterniski
[2]: /1gam
[3]: /control-yourself
[4]: https://docs.python.org/3/tutorial/controlflow.html#match-statements
[5]: https://peps.python.org/pep-0634/#class-patterns
[6]: https://en.wikipedia.org/wiki/Eating_your_own_dog_food
[7]: https://en.wikipedia.org/wiki/KISS_principle
[8]: https://en.wikipedia.org/wiki/Code_refactoring
