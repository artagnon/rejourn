from __future__ import with_statement
import os
from ConfigParser import ConfigParser
from mako.template import Template
from mako.lookup import TemplateLookup
from markdown import markdown
from datetime import datetime
import util

class JBase:
    def __init__(self):
        self.config = self.__parse_config()
        self.jentries = [JEntry(os.path.join(in_basedir, infile))
                         for infile in os.listdir(in_basedir)
                         if infile.endswith('.txt')]

    def write(jentries):
        for jentry in jentries:
            jentry.write()

class JEntry:
    def __init__(self, file_path):
        """Read the infile and populate the object"""

        self.context = {}
        self.in_filepath = file_path
        self.config = self.__parse_config()
        with open(file_path) as infile:
            raw_header, self.content = infile.read().split('\n---\n')
        self.context = self.__parse_header(raw_header)
        self.context = self.__update_context(self.context)
        self.outfile =  self.context['permalink'] + '.html'
        tfile = util.view_mapper.get(self.context.get('view', 'default'))
        tlookup = TemplateLookup(directories = ['.'],
                                 output_encoding='utf-8',
                                 encoding_errors='replace')
        self.template = Template(filename = os.path.join('design', tfile),
                                 lookup = tlookup)

    def __parse_config(self):
        """Uses ConfigParser to parse core.cfg configuration file"""
        
        config = {}
        parser = ConfigParser()
        parser.read('core.cfg')
        for (k, v) in parser.items('Main'):
            config[k] = v
        return config

    def __build_permalink(self, context = None):
        """Either returns permalink or builds it based on the
        title. If no title is present, title defaults to No Title"""
        
        if context is None:
            context = self.context
        if context.get('permalink', None):
            permalink = context['permalink']
        else:
            permalink = util.slugify(context.get('title', 'No Title'))
        return permalink
    
    def __build_timestamp_h(self, context = None):
        """Builds timestamp to be displayed in rendered page"""
        
        if context is None:
            context = self.context
        if context.get('pubdate', None):
            t = datetime.strptime(context['pubdate'], util.time_isofmt)
            return t.strftime(util.time_hfmt)
        else:
            return '[Unpublished]'

    def __render(self, template = None, context = None):
        """Renders a page given template and context"""
        
        if template is None:
            template = self.template
        if context is None:
            context = self.context
        extensions = ['codehilite', 'html_tidy']
        self.context['html_content'] = markdown(self.content, extensions)
        return template.render(**context)

    def __parse_header(self, raw_header):
        """Parses raw header string into context"""
        
        context = {}
        parser = ConfigParser()
        for line in raw_header.split('\n'):
            (key, value) = line.split(': ')
            context[key] = value
        return context

    def __update_header(self, context = None):
        """Updates file header with given context. Function has
        side-effects and returns exit status"""
        
        if context is None:
            context = self.context
        with open(self.in_filepath, 'w') as infile_handle:
            for key in util.header_table:
                if context.get(key, None):
                    infile_handle.write(key + ': '
                                        + context[key].__str__() + '\n')
            infile_handle.write('---\n')
            infile_handle.write(self.content)
        return True

    def __update_context(self, context = None):
        """Post processing: Given certain values in context,
        calculates others"""
        
        if context is None:
            context = self.context
        context['permalink'] = self.__build_permalink(context)
        context['pubdate_h'] = self.__build_timestamp_h(context)
        return context

    def __write(self):
        """Render page and write it to a file"""
        
        outpath = os.path.join(self.config['basedir'], 'out', self.outfile)
        with open(outpath, 'w') as outfile:
            outfile.write(self.__render())
        return True

    def publish(self, context = None):
        """Sets published and pubdate, updates header and context
        appropriately, and renders the page"""
        
        if context is None:
            context = self.context
        context['published'] = True
        context['pubdate'] = datetime.now().strftime(util.time_isofmt)
        self.__update_header(context)
        context = self.__update_context(context)
        self.__write()

    def trash(self, context = None):
        if context is None:
            context = self.context
        pass

jentry = JEntry('/home/artagnon/dev/rejourn/in/test.txt')
print jentry.context
