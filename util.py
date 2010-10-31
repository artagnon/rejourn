import re, os
from datetime import datetime
from ConfigParser import ConfigParser
import time
from email.Utils import formatdate

# Standard timestamp format for serlialization
time_hfmt = '%A, %d %B %Y'
time_isofmt = '%Y-%m-%dT%H:%M:%SZ'

# List of valid headers to extract from context
header_table = [
    'view',
    'permalink',
    'draft',
    'pubdate',
    'title',
    'author',
    'static',
    'snip',
    'tags',
    ]

# Dictionary of views
view_mapper = {
    'default'  : 'default.html',
    'single'   : 'single.html',
    'index'    : 'index.html',
    'rss'      : 'rss.xml',
    }

def build_slug(text):
    slug = re.sub(r'\W+', '-', text.lower())
    return re.sub(r'-+', '-', slug).strip('-')[:30]

def parse_config():
    """Uses ConfigParser to parse core.cfg configuration file"""

    config = {}
    parser = ConfigParser()
    parser.read('core.cfg')
    for (k, v) in parser.items('Main'):
        config[k] = v
    return config

def parse_header(raw_header):
    """Parses raw header string into context"""

    context = {}
    for line in raw_header.split('\n'):
        (key, value) = line.split(': ', 1)
        context[key] = value
    return context

def build_timestamp_h(pubdate = None, rss = False):
    """Builds timestamp to be displayed in rendered page"""

    if pubdate is not None:
        if not rss:
            t = datetime.strptime(pubdate, time_isofmt)
            return t.strftime(time_hfmt)
        else:
            t = time.mktime(time.strptime(pubdate, time_isofmt))
            return formatdate(t, True)
    return '[Unpublished]'

def build_path(basedir, permalink):
    """Given a basedir and permalink, use os.join to build the path of
    the final file to write"""

    if not permalink.endswith(".rss"):
        return os.path.join(basedir, permalink + '.html')
    else:
        return os.path.join(basedir, permalink)

def markdown(content):
    from markdown import markdown
    extensions = ['codehilite', 'html_tidy']
    return markdown(content, extensions)

def asciidoc(content):
    import asciidocapi
    import StringIO
    asciidoc = asciidocapi.AsciiDocAPI()
    asciidoc.options('--no-header-footer')
    infile = StringIO.StringIO(content)
    outfile = StringIO.StringIO()
    asciidoc.execute(infile, outfile)
    return outfile.getvalue()
# vim:set shiftwidth=4 softtabstop=4 expandtab:
