---
layout: post
title: "Blogging again"
date: "2017-09-15 18:43:21 +0100"
tags:
  - blog
  - jekyll
  - python
---

Doing a blog using Jekyll.<!--more-->

Here's a familiar code snippet to test things.

```python
def fizzbuzz(i):

    out = ''

    if i % 3 == 0:
        out = 'fizz'

    if i % 5 == 0:
        out = '{}buzz'.format(out)

    return out or str(i)


print('\n'.join(map(fizzbuzz, range(1, 20))))
```
