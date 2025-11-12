Date: 2025-11-17 20:34
Title: Wiping Out
Summary: Why didn't I manage to finish this month's game?
Friendly_Date: on a chilly autumn evening
Series: 1gam
Tags: gamedev, python, pygame, 1gam


Game #3 of my [one game a month challenge][1] was going to be an endless runner,
but I tripped at the first hurdle.

Here's how it went down:

## Week 1: Pride Before a Fall

My first idea was [Flappy Bird][6], but it felt too simple after [Loco Lift
Rush][2]. I wanted it to be more impressive, and that's where I strayed from
the true goal of the challenge: practice finishing, not impressing.

Next I tried an endless [Frogger][7] concept. Jumping into prototyping the
procedural generation of an endless stream of roads and rivers was a fun
distraction from the niggling feeling of dissatisfaction with [an unoriginal
idea][8].

After falling down various procgen rabbit holes, I forced myself to reset
and come up with a plan and a schedule - the lessons I was supposed to have
learned from participating in Pyweek.

## Week 2: Scope Creep

While writing up the [GDD][4], I decided that Frogger was too staccato. Usually
in an endless runner the player is constantly moving forwards, but Frogger
forces the player to stop and wait for a gap in the traffic or for a log to
float by. Sometimes they might even have to go backwards.

This is how I landed on [Eterniski][10]. The player can only go downhill, and
the only reason to stop is crashing into a tree. Going through consecutive
slalom gates builds score multipliers. I liked this idea and it brought back
fond memories of [Horace Goes Skiing][9] (which coincidentally starts with a
Frogger level).

But then I wanted the controls to feel right. I wanted the satisfaction of long
carving turns and quick slaloms. And suddenly I was in unfamiliar territory.

I realised [the limitation of my control system][5], which only handled digital
input (on/off) and not analog input (like joystick tilt). I spent some time
refactoring my control system to handle this, but by this point I was eating
into the time I had scheduled for composing the soundtrack.

## Week 3: Procrastination

Music is daunting for me. With no background in theory, I've only ever dabbled.
I procrastinated on the last game's soundtrack, and it suffered.  I had made it
a priority this time, but here I was again, doing anything but composing.  I put
a few notes together in [Bosca Coeil][11], in the delusion that messing about
would lead to a soundtrack. But it didn't. I started looking at tutorials on
[Strudel][3], thinking that I might have more luck "coding" music, but that was
just more procrastination.

By the end of week 3 I was behind schedule and demoralised. I had a stub of a
game that I didn't feel excited about, and didn't have enough time to make it
better and learn how to make a soundtrack too, so I started avoiding working on
it at all.  I wrote a post on the control system instead, and even ended up
working on my day-job in my spare time, which I try very hard not to do as a
rule.


## Week 4: Admitting Defeat

So here we are, on the last day of the month, and I have to admit defeat.

I've published the incomplete game on [Github][12] and you can play it here:

[Play Eterniski][13]{.btn}

## Lessons Learned

1. **I need to finish, not impress.**
   My ego was still buzzing from Pyweek, and I wanted to make something that
   stood out. I dismissed Flappy Bird as too simple, but that simplicity would
   have let me spend more time on finishing the game.

2. **Don't let prototyping become procrastination.**
   Jumping into code feels like progress. It's a developer's comfort-zone. But
   it is a trap. Messing about with procedural generation was fun, but it didn't
   get me any closer to a finished game.

3. **Just enough process.** I hate to admit it, but I need a plan to stay on
   track. A schedule and a GDD are the guardrails that keep me from driving off
   the cliff. So I'm making templates that I can fill in first thing each month.

4. **I need to practice music.** I have decades of coding experience, I've been
   drawing pictures since I was a child. Music composition experience? A few
   hours. I have to start being deliberate about learning.

**Pride comes before a fall.** This time I wiped out, but I've picked myself up
and I'll be back next month with a finished game.

[1]: /1gam
[2]: /pyweek-40-part-2-submission
[3]: https://strudel.cc/
[4]: https://en.wikipedia.org/wiki/Game_design_document
[5]: /choking-on-my-own-dog-food
[6]: https://en.wikipedia.org/wiki/Flappy_Bird
[7]: https://en.wikipedia.org/wiki/Frogger
[8]: https://crossyroad.com/
[9]: https://torinak.com/qaop/play/horaceskiing
[10]: /1gam/03_endless_runner
[11]: https://humnom.net/apps/boscaceoil/
[12]: https://github.com/andyhd/eterniski
[13]: https://andydriver.net/eterniski
