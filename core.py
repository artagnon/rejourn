from __future__ import with_statement
import os
from mako.template import Template
from mako.lookup import TemplateLookup
from xml.sax import saxutils
from datetime import datetime
import util
import sys
import hashlib

sys = reload(sys)
sys.setdefaultencoding("utf-8")

class JEntry:
    def __init__(self, inpath):
        """Read the infile and populate the object"""

        # First patse the config and extract data from infile
        self.inpath = inpath
        self.config = util.parse_config()
        with open(inpath) as infh:
            raw_header, self.content = infh.read().split('\n' + self.config.get('separator', '---') + '\n', 1)

        # Parse the header and populate the context with this
        # information
        self.context = self.__update_context(util.parse_header(raw_header))

        # Get a template ready to write
        tfile = util.view_mapper.get(self.context.get('view', 'single'))
        tlookup = TemplateLookup(directories = ['.'],
                                 output_encoding='utf-8',
                                 encoding_errors='replace')
        self.template = Template(filename = os.path.join(self.config.get('designdir', 'design'), tfile),
                                 lookup = tlookup)

    def __render(self, template = None, context = None):
        """Renders a page given template and context"""

        if template is None:
            template = self.template
        if context is None:
            context = self.context

        context['html_content'] = util.htransform(self.content,
                                                  self.config.get('htransform', None))
        try:
            return template.render(**context)
        except UnicodeDecodeError, msg:
            digest = hashlib.sha1(self.content).hexdigest()
            print "Rendering failed: %s" % msg
            print "Renter input is at '%s'." % os.path.join('cache', digest)
            sys.exit(1)

    def __update_header(self, context = None):
        """Updates file header with given context. Function has
        side-effects and returns exit status"""

        if context is None:
            context = self.context
        buf = []
            
        # Write context information in header_table
        nowriteback = self.config.get('nowriteback', '').split(', ')
        for key in util.header_table:
            if (not key in nowriteback) and context.get(key, None):
                buf.append(key + ': '
                                    + context[key].__str__() + '\n')

        # Finish header. Write back original content
        buf.append(self.config.get('separator', '---') + '\n' + self.content)
        with open(self.inpath, 'r') as infh:
            if infh.read() == ''.join(buf):
                return True
        with open(self.inpath, 'w') as infh:
            infh.write(''.join(buf))
            return True
        return False

    def __update_context(self, context = None):
        """Post processing: Given certain values in context,
        calculates others"""

        if context is None:
            context = self.context
            
        # permalink might already be in header, in which case we don't
        # want to change it
        title = context.get('title', 'No Title')
        context['permalink'] = context.get('permalink',
                                           util.build_slug(self.config, title, self.inpath))
        context['draft'] = context.get('draft', None);
        
        # If pubdate is None, util.build_tiemstamp_h will return the
        # string "[Unpublished]"
        pubdate = context.get('pubdate', None)
        context['pubdate_h'] = util.build_timestamp_h(pubdate)
        return context

    def __write_out(self, outpath):
        """Render page and write it to a file"""

        with open(outpath, 'w') as outfh:
            outfh.write(self.__render())
        return True

    def publish(self, context = None):
        """Sets published and pubdate, updates header and context
        appropriately, and renders the page"""

        if context is None:
            context = self.context

        if not context.get('pubdate', None):
            context['pubdate'] = datetime.now().strftime(util.time_isofmt)
        if not context.get('tags', None):
            context['tags'] = ""
        context = self.__update_context(context)
        self.__update_header(context)
        self.__write_out(util.build_path(self.config['outdir'],
                                         self.context['permalink']))
        return True

class JIndex:
    def __init__(self, name, target_list, rss = False):
        """Index builder"""

        self.config = util.parse_config()
        self.name = name
        self.rss = rss
        self.tagprefix = 'tags'
        self.context = self.__update_context(target_list)
        if not rss:
            tfile = util.view_mapper.get('index')
        else:
            tfile = util.view_mapper.get('rss')
        tlookup = TemplateLookup(directories = ['.'],
                                 output_encoding='utf-8',
                                 encoding_errors='replace')
        self.template = Template(filename = os.path.join(self.config.get('designdir', 'design'), tfile),
                                 lookup = tlookup)

    def __render(self, template = None, context = None):
        """Renders a page given template and context"""

        if template is None:
            template = self.template
        if context is None:
            context = self.context
        return template.render(**context)

    def __update_context(self, target_list = None):
        """Builds context from target_list"""

        entries = []
        context = {}
        for target in target_list:
            with open(target + '.txt', 'r') as infh:
                raw_header, content = infh.read().split('\n' + self.config.get('separator', '---') + '\n', 1)
                header = util.parse_header(raw_header)
                title = header.get('title', 'No Title')
                extensions = ['codehilite', 'html_tidy']
                snip = header.get('snip', '')
                if not len(snip) and (not 'snips' in self.config or self.config['snips'] == True):
                    snip = util.htransform(content, self.config.get('htransform', None))[:50] + ' ...'
                if not self.rss:
                    html_content = util.htransform(content, self.config.get('htransform', None))
                else:
                    rss_content = saxutils.escape(util.htransform(content, self.config.get('htransform', None)))
                pubdate = header.get('pubdate', None)
                pubdate_h = util.build_timestamp_h(pubdate, rss=self.rss)

                # Has a date it was published, isn't a draft and isn't a static page
                if pubdate and not (header.get('draft', None) or header.get('static', None)):
                    entries.append({'title': title,
                                    'permalink': header.get('permalink', util.build_slug(self.config, title, infh.name)),
                                    'snip': snip,
                                    'pubdate': pubdate,
                                    'pubdate_h': pubdate_h})
                    if not self.rss:
                        entries[-1]['html_content'] = html_content
                    else:
                        entries[-1]['rss_content'] = rss_content
        entries.sort(cmp = (lambda x, y: -1 if x['pubdate'] > y['pubdate'] else 1))
        indexlen = int(self.config.get('indexlen', 10))
        rsslen = int(self.config.get('rsslen', 10))
        taglen = int(self.config.get('taglen', 0))
        if self.name == 'index' and indexlen > 0:
            context['entries'] = entries[:indexlen]
        elif self.name.endswith('.rss') and rsslen > 0:
            context['entries'] = entries[:rsslen]
        elif (not (self.name.endswith('.rss') or self.name == 'archive')) and taglen > 0:
            context['entries'] = entries[:taglen]
        else:
            context['entries'] = entries
        context['permalink'] = self.name
        if self.name.startswith('index') or self.name.startswith('archive'):
            context['title'] = self.config['title']
            self.tagprefix = ''
        else:
            if self.name.endswith('.rss'):
                context['title'] = saxutils.escape(self.config['title'] + ' - Tags: ' + self.name.replace('.rss', ''))
                self.tagprefix = ''
            else:
                context['title'] = self.config['title'] + ' - Tags: ' + self.name
        context['baseurl'] = self.config['baseurl']
        return context

    def __write_out(self, outpath):
        """Render page and write it to a file"""

        with open(outpath, 'w') as outfh:
            outfh.write(self.__render())
        return True

    def publish(self, context = None):
        """Writes out index file after building appropriate context"""

        if context is None:
            context = self.context

        tagsdir = os.path.join(self.config['outdir'], self.tagprefix)
        if not os.path.exists(tagsdir):
            os.makedirs(tagsdir)
        self.__write_out(util.build_path(self.config['outdir'],
                                         os.path.join(self.tagprefix, self.context['permalink'])))
        return True
# vim:set shiftwidth=4 softtabstop=4 expandtab:
