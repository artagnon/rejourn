from datetime import datetime
from nose.tools import with_setup
from markdown import markdown
from core import JEntry
import util

class TestMarkdown:
    def __init__(self):
        self.jentry = JEntry('/home/artagnon/dev/rejourn/in/test.txt')

    def setup_jentry(self):
        pass
    
    def teardown_jentry(self):
        pass

    def test_parse_config(self):
        store = self.jentry._JEntry__parse_config()
        assert store.get('basedir', None) == "/home/artagnon/dev/rejourn"

    def test_basic_render(self):
        assert self.jentry._JEntry__render()
    
    def test_basic_write(self):
        assert self.jentry._JEntry__write()

    def test_simple_markdown_output(self):
        assert markdown("*strong* hammer") == "<p><em>strong</em> hammer</p>"

    def test_humanize_timestamp(self):
        assert util.humanize_timestamp(datetime(2009, 1, 1, 1, 1, 1)) == "1 year and 3 months ago"
        assert util.humanize_timestamp(datetime(2010, 1, 1, 1, 1, 1)) == "4 months ago"


