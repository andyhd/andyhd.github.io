Date: 2025-10-16 19:35
Title: Control Yourself
Summary: Tackling customisable controls in Pygame.
Friendly_Date: on a brisk autumn evening
Tags: gamedev, python, pygame


Pygame's event queue is a simple and effective way to handle user input.  But
you are on your own when mapping those raw input events to meaningful in-game
actions.

## Nailed to the Mast

The most direct method is to check for specific event types and attributes in
your event loop. Let's use a simple example where you can grow and shrink a box:

```python
import pygame as pg

pg.init()
screen = pg.display.set_mode((600, 600))

box = pg.FRect(0, 0, 50, 50).move_to(center=screen.get_rect().center)

while True:
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                box.scale_by_ip(1.5)  # grow
            if event.key == pg.K_DOWN:
                box.scale_by_ip(0.75)  # shrink
            if event.key == pg.K_ESCAPE:
                exit()

    screen.fill("black")
    pg.draw.rect(screen, "cyan", box)
    pg.display.flip()
```

This is straightforward, but the problem is that it is "hard-coded" - if you
want to change the controls, you have to modify the code itself. A better
approach is to store the map of events to actions in a data structure.

## Follow the Map

The simplest mapping data structure in Python is a dictionary. So we could
define a dictionary that maps action names (like "move_up", "move_down") to the
keys that trigger those actions:

```python
# Define the mapping at the top of the file
control_mapping = {
    "grow": [pg.K_UP, pg.K_w],
    "shrink": [pg.K_DOWN, pg.K_s],
    "quit": [pg.K_ESCAPE],
}

# In the main game loop, we replace the event handling loop with this
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            for action, keys in control_mapping.items():
                if event.key in keys:
                    if action == "grow":
                        box.scale_by_ip(1.5)
                    if action == "shrink":
                        box.scale_by_ip(0.75)
                    if action == "quit":
                        exit()
```

This improves the code by separating the input handling from the key map.  That
connection is now stored in the `control_mapping` dictionary. We could now show
the user a settings screen where they can change the keys associated with each
action, and update the dictionary accordingly.

Another improvement is storing lists of keys for each action, so that we
can support multiple input schemes at the same time, like arrow keys and WASD
for movement.

## Here Be Dragons

But we have to go beyond a simple map of keys to actions if we want to handle
other event types, like mouse clicks or joystick movements (or even `KEYUP`!).
The dictionary of keys is a dead end because it only lets us check the `key`
attribute. To go further, we need a more powerful approach.

To support other event types, we need to store more data about the input
events we want to map to actions. We could create our own custom data structure
to hold this information, but we already have the perfect vessel: Pygame
`Event` objects! We can create our own "template" `Event` objects that have the
attributes we want, and compare incoming events against these templates:

```python
control_mapping = {
    "grow": [
        pg.Event(pg.KEYDOWN, key=pg.K_UP),
        pg.Event(pg.MOUSEBUTTONDOWN, button=1),
    ],
    "shrink": [
        pg.Event(pg.KEYDOWN, key=pg.K_DOWN),
        pg.Event(pg.MOUSEBUTTONDOWN, button=3),
    ],
    "quit": [
        pg.Event(pg.QUIT),
        pg.Event(pg.KEYDOWN, key=pg.K_ESCAPE),
    ],
}
```

To handle this new mapping structure, we need a function that can compare an
incoming event against our template events. This function needs to compare the
`type` and other attributes (eg `key`, `button`, etc) of the events.

But if we're building a new function anyway, we can take it a step further and
instead of checking for an exact value, we can check if a value meets a
condition. If we set an attribute in our template `Event` object to function
(like `value=lambda v: v > 0.5`), we can call[^1] that function with the
corresponding attribute from the incoming event.  If it returns `True`, we have
a match!

This sounds complex, but the final function is suprisingly short. Here's the
code, which we'll put in a separate module file called
`customisable_controls.py`:

```python
from operator import call
from typing import Any

import pygame as pg


def bind(mapping: dict[str, list[pg.Event]]):
    """
    Given a mapping of action names to lists of template Pygame Events,
    return a function that maps incoming events to action names.
    """

    def get_action(event: pg.Event) -> str | None:

        def match_attribute(attr_name: str, value: Any) -> bool:
            if callable(value):
                return call(value, getattr(event, attr_name))
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

    def map_events_to_actions(events: list[pg.Event]) -> list[str]:
        return [action for event in events if (action := get_action(event))]

    return map_events_to_actions
```

I've wrapped `get_action` in a factory function[^2], which takes a control
mapping dictionary as input and returns a function that maps incoming events to
actions.


## El Dorado

Let's rewrite the original example to use our new `customisable_controls`
module, and add joystick support with a [deadzone][1]:
```python

import pygame as pg

import customisable_controls

pg.init()

# Initialize joysticks so that we get joystick events
pg.joystick.init()
joysticks = {
    js.get_instance_id(): js
    for js in map(pg.Joystick, range(pg.joystick.get_count()))
}

control_mapping = {
    "grow": [
        pg.Event(pg.JOYAXISMOTION, axis=1, value=lambda v: v < -0.5),
        pg.Event(pg.KEYDOWN, key=pg.K_UP)
    ],
    "shrink": [
        pg.Event(pg.JOYAXISMOTION, axis=1, value=lambda v: v > 0.5),
        pg.Event(pg.KEYDOWN, key=pg.K_DOWN)
    ],
    "quit": [
        pg.Event(pg.QUIT),
        pg.Event(pg.KEYDOWN, key=pg.K_ESCAPE),
    ],
}
get_actions = customisable_controls.bind(control_mapping)

screen = pg.display.set_mode((600, 600))

box = pg.FRect(0, 0, 50, 50).move_to(center=screen.get_rect().center)

while True:
    for action in get_actions(pg.event.get()):
        if action == "grow":
            box.scale_by_ip(1.5)
        if action == "shrink":
            box.scale_by_ip(0.75)
        if action == "quit":
            exit()

    screen.fill("black")
    pg.draw.rect(screen, "cyan", box)
    pg.display.flip()
```

With this handy new tool in our arsenal, we've amassed a bounty of benefits:

 - we've clarified our input handling code by separating the event-to-action
   mapping from the event loop itself.

 - we've enabled customising the controls - we could build a settings screen to let
   users change the `control_mappings` dictionary at runtime.

 - we can easily add joystick support, mouse buttons, or any other Pygame event type,
   simply by adding more template `Event` objects to the mapping.

With one small, reusable function and a map of actions to template events, we've
gone from a rigid, hard-coded script to a flexible and extensible input system.
It's a little more setup up front, but the benefit to the player and to future
code maintenance is pure gold.

[1]: https://thegamingsetup.com/what-is-controller-deadzone

[^1]: I'm using `operator.call()` here to call the attribute-matching functions. This
    is just because it reads so much more clearly than `value(getattr(event,
    attr_name))`. And [reading is fundamental](https://youtu.be/ZH5wM7tfiiU?si=ZcD3qz9oErgBj-9w)!

[^2]: More nested functions - this time 2 levels deep! Can you tell I'm
    a fan of closures?
