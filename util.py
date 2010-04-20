import re

view_mapper = {
    'default'  : 'default.html',
    'single'   : 'single.html',
    'multiple' : 'multiple.html',
    }

def slugify(text):
    slug = re.sub(r'\W+', '-', text.lower())
    return re.sub(r'-+', '-', slug).strip('-')[:30]
