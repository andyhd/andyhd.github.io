#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = "Andy"
SITENAME = "God Object"
SITEURL = ""

PATH = "content"
PAGE_PATHS = ["."]
STATIC_PATHS = ["css", "images"]

TIMEZONE = "Europe/London"

DEFAULT_LANG = "en"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = ()

# Social widget
SOCIAL = ()

DEFAULT_PAGINATION = True

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

THEME = "themes/godobject"

import pymdownx.emoji

MARKDOWN = {
    "extension_configs": {
        "pymdownx.superfences": {},
        "pymdownx.smartsymbols": {},
        "pymdownx.emoji": {
            "emoji_index": pymdownx.emoji.gemoji,
            "emoji_generator": pymdownx.emoji.to_png,
            "alt": "short",
            "options": {
                "attributes": {"align": "absmiddle", "height": "20px", "width": "20px"},
            },
        },
        "smarty": {},
        "wikilinks": {},
        "markdown.extensions.codehilite": {
            "css_class": "highlight",
        },
        "markdown.extensions.extra": {},
        "markdown.extensions.meta": {},
    },
    "output_format": "html5",
}