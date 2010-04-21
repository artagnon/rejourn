from __future__ import with_statement
from datetime import datetime
from nose.tools import with_setup
from markdown import markdown
from core import JEntry
import util

testfile = '/home/artagnon/dev/rejourn/in/hackers-dream-journal.txt'

class TestAll:
    def __init__(self):
        self.jentry = JEntry(testfile)

    def test_init(self):
        title = """The hacker's dream journal engine"""
        assert self.jentry.context['title'] == title
        assert self.jentry.context['permalink'] == util.build_slug(title)

    def test_parse_header(self):
        raw_header = "view: single\npermalink: the-hacker-s-dream-journal-eng\npublished: True\npubdate: 2010-04-21T12:04:36Z\ntitle: The hacker's dream journal engine\nauthor: Ramkumar Ramachandra"
        header = util.parse_header(raw_header)
        assert header['pubdate'] == '2010-04-21T12:04:36Z'

    def test_parse_config(self):
        config = util.parse_config('core.cfg')
        assert config.get('basedir', None) == "/home/artagnon/dev/rejourn"

    def test_publish(self):
        self.jentry.publish()
        with open(testfile) as infile:
            assert infile.read().find("published: True") != -1

    def test_mtime_check(self):
        assert self.jentry.publish() == -1

    def test_markdown_lib(self):
        assert markdown("*strong* hammer") == "<p><em>strong</em> hammer</p>"

