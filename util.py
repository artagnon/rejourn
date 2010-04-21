import re, os
from datetime import datetime
from ConfigParser import ConfigParser

# Standard timestamp format for serlialization
time_hfmt = '%A, %d %B %Y'
time_isofmt = '%Y-%m-%dT%H:%M:%SZ'

# List of valid headers to extract from context
header_table = [
    'view',
    'permalink',
    'published',
    'pubdate',
    'title',
    'author',
    ]

# Dictionary of views
view_mapper = {
    'default'  : 'default.html',
    'single'   : 'single.html',
    'multiple' : 'multiple.html',
    }

def build_slug(text):
    slug = re.sub(r'\W+', '-', text.lower())
    return re.sub(r'-+', '-', slug).strip('-')[:30]

def parse_config(filename):
    """Uses ConfigParser to parse core.cfg configuration file"""

    config = {}
    parser = ConfigParser()
    parser.read(filename)
    for (k, v) in parser.items('Main'):
        config[k] = v
    return config

def parse_header(raw_header):
    """Parses raw header string into context"""
        
    context = {}
    for line in raw_header.split('\n'):
        (key, value) = line.split(': ')
        context[key] = value
    return context

def build_timestamp_h(self, pubdate = None):
    """Builds timestamp to be displayed in rendered page"""
    
    if pubdate is not None:
        t = datetime.strptime(pubdate, util.time_isofmt)
        return t.strftime(util.time_hfmt)
    return '[Unpublished]'

def build_outpath(basedir, permalink):
    """Given a basedir and permalink, use os.join to build the path of
    the final file to write"""
    
    return os.path.join(basedir, 'out', permalink + '.html')
