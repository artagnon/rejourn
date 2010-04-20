from __future__ import with_statement
from datetime import datetime
from nose.tools import with_setup
from markdown import markdown
from core import JEntry
import util

class TestAll:
    def __init__(self):
        self.jentry = JEntry('/home/artagnon/dev/rejourn/in/test.txt')

    def test_init(self):
        title = """The hacker's dream journal engine"""
        assert self.jentry.context['title'] == title
        assert self.jentry.context['permalink'] == util.slugify(title)

    def test_parse_config(self):
        store = self.jentry._JEntry__parse_config()
        assert store.get('basedir', None) == "/home/artagnon/dev/rejourn"

    def test_render(self):
        assert self.jentry._JEntry__render()
    
    def test_write(self):
        assert self.jentry._JEntry__write()

    def test_publish(self):
        self.jentry.publish()
        with open('/home/artagnon/dev/rejourn/in/test.txt') as infile:
            assert infile.read().find("published: True") != -1

    def test_markdown_lib(self):
        assert markdown("*strong* hammer") == "<p><em>strong</em> hammer</p>"

    def test_humanize_timestamp(self):
        assert util.humanize_timestamp(datetime(2009, 1, 1, 1, 1, 1)) == "1 year and 3 months ago"
        assert util.humanize_timestamp(datetime(2010, 1, 1, 1, 1, 1)) == "4 months ago"


