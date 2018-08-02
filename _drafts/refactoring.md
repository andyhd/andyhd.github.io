---
layout: post
title: "What Is Good Code?"
date: "2017-09-19 16:10:27 +0100"
comments: false
---

I have opinions.<!--more-->

This is the first post in a series about rewriting existing code to make it
better. I'll be writing about good coding practice, refactoring, testing and how
to review other people's code - stuff that I've learned over the last 20 years
of writing software professionally.

How to decide whether code is good or not can be a controversial subject, as
developers can be very touchy about their code. Writing code is a creative act
and every program, class and function is an expression of the coder's
personality, opinions and experiences. And when someone criticizes your
creations, however reasonably and constructively, it's easy to feel that they
are criticizing you. *Suck it up*.  We have a job to do, and it is our
responsibility to write code that not only works, but that the rest of our team,
current and future, can easily understand and maintain.


### Good Code - a Definition

The top few search results for "what does good code look like?" are roughly in
agreement: good code is simple, organised, easy to read and understand, and
testable (and tested!). All fairly self-evident, perhaps? And yet, whether in
huge tech companies, cutting-edge startups or government departments, very
rarely have I worked with code that could be described by all (or often any) of
those terms.

#### Simple

Keeping code simple is a surprisingly difficult task. Especially because I think
it's safe to say most developers consider themselves rather clever and enjoy
demonstrating their slickest coding tricks every now and then. I often have to
fight the urge to write a clever hack to satisfy my vanity.

In truth, it depends on what constraints exist, like the code has to run as
quickly or efficiently as possible, which prevent us from optimising for what I
think we should all agree is the default priority: **maintainability**.

You know that feeling when you're looking at old code and wondering who could
have produced such impenetrable gibberish - and then `git blame` turns up your
own name? Well, it has happened to me **a lot**. It's amazing sometimes how even
a week or two away from a codebase can render it incomprehensible when you
return to it.

```python
def foo():
    pass
```

* joining an existing project
* complexity, KISS
* cleverness, doing too much at once, kill your darlings
* over-engineering, premature optimisation, yagni

#### Organised


#### Readable

* code standards
* documentation - out of date
* revealing intent
* naming

#### Testable

* tests

### Summary

