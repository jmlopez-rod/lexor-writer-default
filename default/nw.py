"""LEXOR: DEFAULT NodeWriters

Collection of NodeWriter objects to write an html format as if it
was written in the lexor format.

"""

import re
import textwrap
from lexor.core.writer import NodeWriter
import lexor.core.elements as core
RE = re.compile(r'\s+')
TW = textwrap.TextWrapper()
RAWTEXT = (
    'script', 'style', 'textarea', 'title'
)
BLOCK = [
    'html', 'address', 'article', 'aside', 'blockquote', 'dir',
    'div', 'dl', 'fieldset', 'footer', 'form', 'h1', 'h2', 'h3',
    'h4', 'h5', 'h6', 'header', 'hgroup', 'hr', 'main', 'menu',
    'nav', 'p', 'pre', 'section', 'table', 'ol', 'ul', 'li', 'link',
    '#doctype', 'head', 'body',
]
BLOCK.extend(RAWTEXT)


def format_attributes(node, exclude=None):
    """Format a node's attribute. """
    if exclude is None:
        exclude = []
    att = []
    for key, val in node.items():
        if key in exclude:
            continue
        if key == 'id':
            att.append('#%s' % val)
        elif key == 'class':
            if ':' in val:
                att.append('class="%s"' % val)
            else:
                for item in val.split():
                    att.append('.%s' % item)
        else:
            att.append('%s="%s"' % (key, val))
    return ' '.join(att)


class TextNW(NodeWriter):
    """Writes text nodes with multiple spaces removed. """

    def data(self, node):
        if self.writer.pre_node:
            self.wrap(node.data)
            return
        text = re.sub(RE, ' ', node.data)
        if text != ' ' or (node.index != 0 and
                           node.prev.name not in BLOCK and
                           node.next is not None and
                           node.next.name not in BLOCK):
            self.wrap(text)


class DefaultNW(NodeWriter):
    """Default way of writing HTML elements. """

    def start(self, node):
        if node.name == 'pre':
            self.writer.enable_raw()
            self.writer.pre_node += 1
            if 'pre' in BLOCK:
                self.writer.endl(False)
        if not self.writer.pre_node and node.name in BLOCK:
            self.writer.endl(False)
        if isinstance(node, core.ProcessingInstruction):
            self.wrap('<%s' % node.name, split=True)
            if '\n' in node.data:
                self.wrap('\n')
            else:
                self.wrap(' ')
            return
        att = format_attributes(node)
        if node.name == 'span':
            self.wrap('%%%%{%s' % att, split=True)
        else:
            self.wrap('%%%%{%s' % node.name, split=True)
            if att != '':
                self.wrap(' %s' % att)
        if isinstance(node, core.Void):
            self.wrap('}')
        else:
            self.wrap('}')

    def data(self, node):
        if (node.name in RAWTEXT or
                isinstance(node, core.ProcessingInstruction)):
            self.wrap(node.data, raw=True)
        else:
            text = re.sub(RE, ' ', node.data)
            self.wrap(text)

    def child(self, node):
        if self.writer.pre_node:
            return True
        for child in node.child:
            if child.name not in ['#text', '#entity']:
                return True
        for child in node.child:
            if child.name == '#entity':
                self.writer.get_node_writer('#entity').data(child)
            else:
                self.wrap(re.sub(RE, ' ', child.data))
        self.wrap('%%')
        if node.name in BLOCK:
            self.wrap('\n')

    def end(self, node):
        if node.name == 'pre':
            self.writer.pre_node -= 1
            if self.writer.pre_node == 0:
                self.writer.disable_raw()
        raw = self.writer.pre_node
        if node.child is None:
            if isinstance(node, core.ProcessingInstruction):
                self.wrap('?>')
            elif isinstance(node, core.RawText):
                self.wrap('%%')
            if not raw:
                self.writer.endl()
        else:
            self.wrap('%%')
            if not raw and node.name in BLOCK:
                self.writer.endl(False)


class DoctypeNW(NodeWriter):
    """Writes the doctype node: `<!DOCTYPE ...>`. """

    def start(self, node):
        self.wrap('<!DOCTYPE ')

    def data(self, node):
        self.wrap(re.sub(RE, ' ', node.data).strip())

    def end(self, node):
        self.wrap('>\n', raw=True)


class CDataNW(NodeWriter):
    """Writes the CDATA node. """

    def start(self, node):
        self.wrap('<![CDATA[', split=True)

    def data(self, node):
        data = node.data.split(']]>')
        for index in xrange(len(data)-1):
            self.wrap(data[index] + ']]]]><![CDATA[>', raw=True)
        self.wrap(data[-1], raw=True)

    def end(self, node):
        self.wrap(']]>')


class CommentNW(NodeWriter):
    """Comment can also follow the tree structure. They have to be
    formatted to reflect this. """

    def start(self, node):
        if node.prev is not None:
            if node.prev.name == '#text':
                index = node.prev.data.rfind('\n')
                if index != -1:
                    line = node.prev.data[index+1:]
                    if line.strip() == '':
                        self.writer.endl(False)
        self.wrap('<!--', split=True)

    def data(self, node):
        self.wrap(node.data, raw=True)

    def end(self, node):
        self.wrap('-->')
        if node.next is not None:
            nnext = node.next
            if nnext.name == '#text' and nnext.data.startswith('\n'):
                self.writer.endl()


class DocumentNW(NodeWriter):
    """Finish document with a new line character. """

    def end(self, node):
        self.writer.endl(False)


class ParagraphNW(NodeWriter):
    """Write a paragraph. """

    def start(self, node):
        if self.writer.buffer == '':
            if (node.parent.name != 'li' and
                    node.index != 0 and
                    self.writer.prev_str != '\n\n'):
                self.writer.endl()
        else:
            self.writer.strwrite(self.writer.buffer)
            self.writer.buffer = ''
            if node.parent.name != 'li' and node.index != 0:
                self.wrap('\n\n', raw=True)
        if node.attlen > 0:
            att = format_attributes(node)
            self.wrap('%%%%{%s' % node.name)
            if att != '':
                self.wrap(' %s' % att)
            self.wrap('}')

    def end(self, node):
        if node.attlen > 0:
            self.wrap('%%')
        self.wrap('\n\n', raw=True)


class StrongNW(NodeWriter):
    """Strong element display. """

    def start(self, node):
        self.wrap('**')

    def end(self, node):
        self.wrap('**')
        if node.attlen > 0:
            self.wrap('{%s}' % format_attributes(node))


class EmNW(NodeWriter):
    """Strong element display. """

    def start(self, node):
        self.wrap('*')

    def end(self, node):
        self.wrap('*')
        if node.attlen > 0:
            self.wrap('{%s}' % format_attributes(node))


class AnchorNW(NodeWriter):
    """Anchor element display. """

    def start(self, _):
        self.wrap('[')

    def end(self, node):
        self.wrap(']')
        if 'title' in node:
            title = ' "%s"' % node['title']
            exclude = ['href', 'title']
        else:
            title = ''
            exclude = ['href']
        self.wrap('(%s%s)' % (node['href'], title), split=True)
        if node.attlen - len(exclude) > 0:
            self.wrap('{%s}' % format_attributes(node, exclude))


class HRuleNW(NodeWriter):
    """Display hr element. """

    def start(self, _):
        if self.writer.buffer == '':
            if self.writer.prev_str != '\n\n':
                self.writer.endl()
        else:
            self.writer.strwrite(self.writer.buffer)
            self.writer.buffer = ''
            self.wrap('\n\n', raw=True)
        self.wrap('-'*self.writer.width, raw=True)
        self.wrap('\n\n', raw=True)


class EntityNW(NodeWriter):
    """Display the entity nodes. """

    mapping = {
        '&lt;': '<',
        '&gt;': '>',
        '&amp;': '&',
        '&ndash;': '--',
        '&#8211;': '--',
        '&mdash;': '---',
        '&#8212;': '---',
        '&#8216;': "'",
        '&#8217;': "'",
        '&#8220;': '"',
        '&#8221;': '"',
        '&#8226;': '*',
        '&bull;': '*',
        '&nbsp;': ' ',
        '&quot;': '"',
        '&ldquo;': '"',
        '&rdquo;': '"',
    }

    def __init__(self, writer):
        NodeWriter.__init__(self, writer)
        for i in xrange(32, 127):
            self.mapping['&#%d;' % i] = chr(i)

    def data(self, node):
        if self.writer.pre_node:
            raw = True
        else:
            raw = False
        self.wrap('%s' % self.mapping[node.data], raw=raw)


class HeaderNW(NodeWriter):
    """Header elements display. """

    def start(self, node):
        self.writer.disable_wrap()
        if not self.writer.prev_str.endswith('\n'):
            self.writer.endl()
        self.writer.endl()
        level = int(node.name[1])
        if self.writer.header == 'setext' and level < 3:
            pass
        else:
            self.wrap(('#'*level)+' ')

    def end(self, node):
        level = int(node.name[1])
        if self.writer.header == 'setext' and level < 3:
            if node.attlen > 0:
                if not self.writer.prev_str.endswith(' '):
                    self.wrap(' ')
                self.wrap('{%s}' % format_attributes(node))
            width = self.writer.pos[1] - 1
            if level == 1:
                self.wrap('\n'+('='*width))
            else:
                self.wrap('\n'+('-'*width))
        else:
            if node.attlen > 0:
                self.wrap('{%s}' % format_attributes(node))
        self.wrap('\n\n')
        self.writer.enable_wrap()


class ListItemNW(NodeWriter):
    """List elements display. """

    def start(self, _):
        self.writer.endl(False)
        self.wrap('* ')

    def end(self, _):
        self.writer.endl(False)
