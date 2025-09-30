Date: 2025-09-21 20:17
Title: PyWeek 40
Summary: In which I attempt to actually submit a gamejam entry for once.
Friendly_Date: on an unusually warm autumn evening
Series: 1gam
Tags: gamedev, python, pygame

It is the 20th Anniversary Edition of [PyWeek ](https://pyweek.org/40), the
Python game jam. Although I have tried to participate in several game jams in
the past, the last (and only) actual submission I made was for [Ludum Dare 42 in
2018](/ludum-dare-results.html). I've abandoned several attempts since then, but
as I am challenging myself to publish [one game per month](/1gam) at the moment,
I can kill two birds with one stone by actually submitting something this time!

The theme voting was last week, and the winning theme is **Skyscraper City**
- which I voted for, so I am pleased with the result. I had a few ideas for
games immediately spring to mind, and the one I have already started
prototyping is a game where you control a lift in a busy skyscraper, picking up
and dropping off passengers on different floors. The working title is **Loco Lift
Rush**.

![Screenshot of Loco Lift Rush
prototype]({static}loco-lift-rush-2025-09-21.png){width=400px, style="float: left"}

The core gameplay is super simple, just moving the lift up and down and
letting people in and out. The challenge comes from the continuous stream of
passengers, each with their own destination floor, and the fact that they will
get impatient and leave if you take too long. The goal is to deliver as many
passengers as possible within a time limit.

I've already got a basic prototype going, but before I get too far ahead of
myself, I should set out a plan and schedule to make sure I can actually finish
in the one week time limit - unlike previous attempts!

To that end, I will sketch out a simple
[GDD](https://en.wikipedia.org/wiki/Game_design_document) to define the scope of
the game, and then break it down into chunks that I can tackle day by day.

### Elevator Pitch

You are a lift operator in an ever-growing skyscraper. Your job is to move the
lift up and down to pick up and drop off a stream of users at random floors.
The users will get impatient if you take too long, so be quick!

### The "Must-Have"s
  - Game screen is a side-on cut-away interior view of a skyscraper with
    multiple floors
  - Player uses simple keyboard or mouse controls to move a central lift up and
    down between floors
  - Passengers continuously arrive from the sides of the screen to call the lift
    at random intervals, on random floors, and with random destination floors
    (destination is shown in a sign over their heads)
  - Users wait to board the lift when it arrives at their floor and disembark
    when the lift stops at their destination floor
  - Users leave and complain if they have to wait too long
  - Score based on number of users served and number of complaints
  - Level "complete" after a certain amount of time
  - Vertical scrolling camera for taller buildings

### The "Nice-to-Have"s
  - Different passenger types with varying patience levels and behaviours
  - Sound effects for lift moving, passengers complaining, and background music
  - Gradually increasing difficulty (more floors, faster rate of user arrival)
  - Power-ups (like a speed boost, extra time, or increased capacity)
  - Survival mode - no time limit, just see how long you can last

The "Must-Have" list is intentionally small. I'm trying hard to avoid my
tendency to over-scoping and perfectionism, which has scuppered previous
attempts.

This should be comfortably achievable within the one week time limit, even with
my limited free time. The core mechanics are simple, and I can always add more
features if I have time left over.

### Schedule

With the scope of the game defined, I can now outline a schedule:

1. **MVP** (Days 1-2): Tackle everything on the "Must-Have" list
2. **Look and Feel** (Days 3-4): Focus on graphics and sound
3. **Polish & Ship** (Days 5-7): Add stretch goals, fix bugs, and submit

### <span lang="ja" title="Ganbatte! (Do your best!)" style="font-family: mobo-bold; -webkit-text-stroke-width: 0.05em"> がんばって</span> !

As I write this, it's already the evening of Day 1, and I've already got the
basic game loop started, with a simple lift moving up and down and passengers
appearing on random floors, so I'm on track. Wish me luck!
