---
layout: post
title: "Ludum Dare Results"
date: "2018-09-12 07:52:03 +0100"
comments: false
image-url: "/assets/images/beaver-pitch-title.png"
---

Here's what I managed to achieve in my first game jam.<!--more-->

![Thieving beavers](/assets/images/thieving-beavers.gif)

It's not quite finished, and it's not as good as I hoped, but I learned a lot.

[Download](https://github.com/andyhd/ld42/releases/latest) and try it out.
Or check out the [source code](https://github.com/andyhd/ld42).

I placed [716th overall](https://ldjam.com/events/ludum-dare/42/beaver-pitch), out of 3069 entries. Not too bad for a first effort.

Here's how it went down:


### The idea

The theme of the jam was "Running out of space". I spent half an hour or so
coming up with some ideas that might be workable:

* **Fitting things in**
  * You are the Maitre'd at a popular restaurant and you have to assign diner
    groups to tables.
  * Your disk drive is getting full. You need to delete some files. But which
    are vital code?
  * There are more and more patients and a limited number of hospital beds.
  * You have to clean up orbital debris to make way for satellites and rocket
    launches.
  * Too many cars, not enough parking spaces.
  * Your family is growing too big for your house. Clear out rooms or save for
    an extension.

* **Running**
  * You are a space smuggler "running" contraband between planets.
  * You are literally running in a spacewalk race.
  * You are running a space delivery company.
  * Alien plants are running tendrils from space and choking your planet.

* **Space**
  * You have to navigate a crowded street/train/etc where people get in your
    personal space - try not to lose your temper!
  * Something in Outer space.
  * Game set in Inner space: Nanobots and viruses inside a body.

* **Shrinking environment**
  * You are defending against opponents that consume the ground you are on. You
    need the ground around you for resources.
  * When you fail, the path you took is closed off.
  * You are growing uncontrollably. You have to escape before you get stuck.

Then I chose the one that I thought would be easiest to build in the 48 hours
available and fleshed out the idea into "Beaver Pitch" (credit for the title
goes to Deborah!)

* You are a beaver. Your dam/home is made of logs. Other beavers are trying to
  steal the logs and you have to protect/replace them.

I shared the rest of my ideas on the [LDJam website](https://ldjam.com), in the
hopes that my ideas might help others struggling to come up with something. At
least one person actually did use one of my ideas, which felt pretty good!


### The implementation

I had set aside the whole weekend to work on my game, and I knew I wanted to
build it in Common Lisp, as I said in the
[previous post](/2018/08/02/ludum-dare). I had my working environment all set up
and ready to go, which was great as I could just start coding right away.

What I should have done at this point is make a rough schedule of work - how I
would divide up the 48 hours into coding, drawing the graphics, composing the
music and sound effects, eating and sleeping.

What I actually did was jump straight into drawing a sprite for the main
character. I've seen a few game jam development diaries and postmortems which
reveal that the developer started with just coloured blocks on the screen and no
images at all until they get the core of the gameplay working. I think I will
try this method next time.

I recorded a time-lapse video of my screen as I worked - here is a slightly
edited version which skips long periods of inactivity(!):

<iframe width="560" height="315" src="https://www.youtube.com/embed/A5lTF7UjUAg?rel=0" frameborder="0" allow="encrypted-media" allowfullscreen></iframe>

What surprised me when watching it back was how much time I spent not working on
the game, and instead browsing the LDJam website. I definitely felt a sense of
being involved in the event and being part of a community while reading through
the posts. But I would have got a lot more finished in my game if I had been
more disciplined. Next time, I will use the
[Pomodoro technique](https://francescocirillo.com/pages/pomodoro-technique) to
keep myself focused.


### The learnings

I learned a lot about writing a game, and specifically how to reduce the scope
of a game jam entry.

Beforehand, I read up on how to prepare and familiarised myself with my tools.
Spending a little time just laying the groundwork for the game meant I could hit
the ground running as soon as the jam started. And practicing with
[Sunvox](http://www.warmplace.ru/soft/sunvox/) meant that, if I hadn't run out
of time, I wouldn't have wasted any during the jam, trying to learn as I went.

I really stretched my Common Lisp skills and feel a lot happier with how I
write Lisp. I decided to avoid CLOS so as not to write Lisp as though it were
Python or another OO language. I practiced iteration without using the LOOP
macro in an attempt to broaden my knowledge of Lisp and keep the code as simple
as possible.

Afterwards, I realized how my lack of a schedule had hurt my ability to use the
time available to the fullest. I also received some great feedback during the
rating phase of the jam, and have a list of bug fixes and enhancements to make
to the game post-jam.


### Conclusion

I really enjoyed participating in Ludum Dare 42. The next one starts on 30th
November, and I may have another go, if I can make the time.

I'm also tempted by [1 Game A Month](http://www.onegameamonth.com/). I
think the learning experience of writing a number of games at a less frantic
pace will be more valuable to me than the competition and intensity of a 48 hour
game jam.

Anyway, this experience has shown me how much I have to learn before I'll be
able to develop a game good enough to place well in Ludum Dare.

I know it will be fun getting there!
