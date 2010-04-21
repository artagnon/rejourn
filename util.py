import re
from datetime import datetime

# Standard timestamp format for serlialization
time_hfmt = '%A, %d %B %Y'
time_isofmt = '%Y-%m-%dT%H:%M:%SZ'

# List of valid headers
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

def slugify(text):
    slug = re.sub(r'\W+', '-', text.lower())
    return re.sub(r'-+', '-', slug).strip('-')[:30]
