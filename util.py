import re, os
import time
import hashlib
from datetime import datetime
from ConfigParser import ConfigParser
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
    input_buf = StringIO.StringIO(content)
    output_buf = StringIO.StringIO()
    asciidoc.execute(input_buf, output_buf)
    return output_buf.getvalue()

# hTransform mapper
htransform_mapper = {
    'markdown'  : markdown,
    'asciidoc'  : asciidoc,
    }

def htransform(content, transform):
    # Attempt to fetch it from cache
    digest = hashlib.sha1(content).hexdigest()
    if os.path.exists(os.path.join('cache', digest)):
        with open(os.path.join('cache', digest), 'r') as infh:
            return infh.read()

    # Choose a htransform function 
    render_function = htransform_mapper.get(transform, markdown)
    output_buf = render_function(content)

    # Write to cache before returning
    with open(os.path.join('cache', digest), 'w') as outfh:
        outfh.write(output_buf)
        return output_buf
# vim:set shiftwidth=4 softtabstop=4 expandtab:
