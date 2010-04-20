import re
from datetime import datetime

# Standard timestamp format for serlialization
timestamp_fmt = '%b %d %Y %I:%M %p'

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

def humanize_timestamp(timestamp):
    time_delta = datetime.now() - timestamp
    years = time_delta.days / 365
    months = time_delta.days % 365 / 30
    weeks = time_delta.days % 365 % 30 / 7
    days = time_delta.days
    hours = time_delta.seconds / 3600
    minutes = time_delta.seconds % 3600 / 60
    seconds = time_delta.seconds % 3600 % 60

    if years > 0:
        if years == 1 and months < 3:
            return "A year ago"
        elif years == 1:
            return "%s year and %s months ago" % (years, months)
        elif months == 1:
            return "%s years ago" % years
        elif months > 9:
            return "%s years ago" % years + 1
        else:
            return "%s years and %s months ago" % (years, months)
    
    elif months > 0:
        if months > 9:
            return "A year ago"
        elif months == 1 and days < 15:
            return "A month ago"
        elif days > 15:
            return "%s months ago" % (months + 1)
        else:
            return "%s months ago" % months

    elif days > 0:
        if days > 15:
            return "A month ago"
        elif days == 1:
            return "A day ago"
        elif days > 10:
            return "%s days ago" % ((days / 10) * 10)
        elif days < 3:
            return "A few days ago"
        else:
            return "%s days ago" % days
        
    elif hours > 0:
        if hours > 22:
            return "A day ago"
        elif hours == 1:
            return "An hour ago"
        elif hours < 3:
            return "A few hours ago"
        else:
            return "%s hours ago" % hours
    
    elif minutes > 0:
        if minutes > 50:
            return "An hour ago"
        elif minutes == 1:
            return "A minute ago"
        elif minutes > 10:
            return "%s minutes ago" % ((minutes / 10) * 10)
        elif hours < 3:
            return "A few minutes ago"
        else:
            return "%s minutes ago" % minutes

    else:
        return "Just now"
