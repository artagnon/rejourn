from __future__ import with_statement
from datetime import datetime
from nose.tools import with_setup
from core import JEntry
import util

inf = 't/test.txt'
outf = 't/test.html'

class TestAll:
    def __init__(self):
        self.jentry = JEntry(inf)

    def test_init(self):
        title = """The hacker's dream journal engine"""
        assert self.jentry.context['title'] == title
        assert self.jentry.context['permalink'] == util.build_slug(title)
        assert self.jentry.context['tags'] == 'foo, bar'

    def test_parse_header(self):
        raw_header = "view: single\npermalink: the-hacker-s-dream-journal-eng\npublished: True\npubdate: 2010-04-21T12:04:36Z\ntitle: The hacker's dream journal engine\nauthor: Ramkumar Ramachandra"
        header = util.parse_header(raw_header)
        assert header['pubdate'] == '2010-04-21T12:04:36Z'

    def test_parse_config(self):
        config = util.parse_config()
        assert config.get('indir', None)
        assert config.get('outdir', None)

    def test_publish(self):
        assert self.jentry.publish()

    def test_markdown_lib(self):
        assert util.htransform("*strong* hammer", 'markdown') == "<p><em>strong</em> hammer</p>"

    def test_asciidoc_lib(self):
        assert util.htransform("`strong` `{hammer}`", 'asciidoc') == """<div class="paragraph"><p><tt>strong</tt> <tt>{hammer}</tt></p></div>\r\n"""
# vim:set shiftwidth=4 softtabstop=4 expandtab:
