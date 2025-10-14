Date: 2025-02-22 17:50
Title: Tower Defence game, Part 2: Path-finding
Friendly-Date: Evening of the first warm day of the year
Tags: gamedev, python, pygame, tower-defence, tutorial
Status: draft


### Laying Down the Law: Grids and Pathing in Tower Defense Games

In a tower defense game, enemies don’t just wander around aimlessly, bumping into trees and questioning their life choices. No, they march with purpose, from point A (the enemy spawn) to point B (your precious base) along a clearly defined path. Your job is to make sure they don’t get there, preferably by setting up an elaborate gauntlet of towers that make their journey an absolute nightmare.

#### The Grid: A Civilized Approach to Order

Most tower defense games use a grid-based system to keep things neat and predictable. This ensures that towers fit snugly into predefined locations and enemies follow a structured path instead of making bizarre diagonal shortcuts that ruin the game’s balance and your carefully planned defenses.

A basic grid can be represented as a 2D array, where each cell stores information about whether it’s a valid placement spot, a path, or an impassable obstacle. Something like this:

```python
LEVEL_MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
]
```

Here, `1` represents a place where towers can be built, and `0` is a path. This simple representation makes it easy to check if a tile is a valid placement spot or part of the enemy’s route.

#### The Path: A Guided Tour to Their Doom

Once you’ve established the grid, you need to define how enemies navigate it. The most common approach is to use waypoints: predefined points that guide enemies along the path.

A basic waypoint system might look like this:

```python
WAYPOINTS = [
    (0, 1), (1, 1), (2, 1), (3, 1), (3, 2), (3, 3), (3, 4), (4, 4), (5, 4), (6, 4)
]
```

Each tuple represents a grid coordinate that enemies will move toward in sequence. When an enemy reaches a waypoint, they simply head toward the next one. If they reach the last one, well, that’s bad news for you.

#### Implementation: Making Them Move

To make enemies follow the path, we give them a target waypoint and move them in that direction. Here’s a simple movement function:

```python
class Enemy:
    def __init__(self, waypoints):
        self.waypoints = waypoints
        self.current_wp = 0
        self.x, self.y = waypoints[0]  # Start at first waypoint

    def update(self):
        target_x, target_y = self.waypoints[self.current_wp]
        dx, dy = target_x - self.x, target_y - self.y
        dist = (dx**2 + dy**2) ** 0.5

        if dist > 0:
            self.x += dx / dist * 2  # Move at speed 2
            self.y += dy / dist * 2

        if dist < 2:  # Close enough to move to next waypoint
            self.current_wp += 1
            if self.current_wp >= len(self.waypoints):
                self.reach_goal()

    def reach_goal(self):
        print("An enemy has reached your base. You should probably do something about that.")
```

This keeps things simple: the enemy moves toward the next waypoint and switches to the next one when it’s close enough. Once it reaches the final waypoint, the game should punish the player appropriately (or at least make them feel bad about their life choices).

#### Wrapping Up

Pathing and grids form the backbone of a well-structured tower defense game. Keeping enemies on a defined route ensures that gameplay remains fair and predictable while allowing players to strategize effectively. Whether you use a simple waypoint system or a full-fledged pathfinding algorithm like A* (for handling player-placed obstacles), the key is ensuring enemies take a logical, challenge-driven path to their inevitable demise.

And if you get it wrong? Well, expect your enemies to take creative liberties with their navigation, much to the frustration of your future players. But hey, at least they’ll have a story to tell.

