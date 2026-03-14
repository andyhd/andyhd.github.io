AUTHOR = 'Andy Driver'
SITENAME = 'Andy Driver'
SITEURL = 'https://andydriver.net'

EXTRA_PATH_METADATA = {
    "misc/robots.txt": {"path": "robots.txt"},
    "misc/sitemap.xml": {"path": "sitemap.xml"},
}

PATH = 'content'
ARTICLE_PATHS = ["posts"]
STATIC_PATHS = [
    'images',
    'misc/robots.txt',
    'misc/sitemap.xml',
    'posts/1gam',
]

ARTICLE_URL = '{category}/{slug}/'
ARTICLE_SAVE_AS = '{category}/{slug}/index.html'
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'
INDEX_SAVE_AS = 'posts/index.html'

DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = False

PLUGIN_PATHS = ['plugins']
PLUGINS = ['pelican.plugins.series', 'comments']

TIMEZONE = 'Europe/London'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ATOM = "feeds/atom.xml"
# FEED_ALL_ATOM = None
# CATEGORY_FEED_ATOM = None
# TRANSLATION_FEED_ATOM = None
# AUTHOR_FEED_ATOM = None
# AUTHOR_FEED_RSS = None

# # Blogroll
# LINKS = (('Pelican', 'https://getpelican.com/'),
#          ('Python.org', 'https://www.python.org/'),
#          ('Jinja2', 'https://palletsprojects.com/p/jinja/'),
#          ('You can modify those links in your config file', '#'),)

# Social widget
# SOCIAL = (('You can add links in your config file', '#'),
#           ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

THEME = "themes/godobject"

MARKDOWN = {
    "extension_configs": {
        "wikilinks": {"base_url": "/pages/"},
        "markdown.extensions.codehilite": {"css_class": "highlight"},
        "markdown.extensions.extra": {},
        "markdown.extensions.meta": {},
        "markdown.extensions.toc": {"toc_depth": "2-3"},
    },
    "output_format": "html5",
}