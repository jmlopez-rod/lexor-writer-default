"""LEXOR: LIST NodeWriter

When an `ol` or `ul` tag is encountered lexor enters its `list` mode.
The list mode is a tag with no attributes. It is nothing but a marker
that lets you know that you can create lists. An item must begin with:

%%{list}
* `*` for unordered lists.
* `+` for ordered lists.
%%

To tell lexor that you want a sublist simply repeat the starting
character. For instance, writing `***` will tell lexor that we are
starting a list in level 3.

If your list have some attributes you may specify them by using an
attribute list right after the item declaration:

    ***{#ul-id}{#li-id}

If two attribute lists are declared then the first one belongs to the
`ul` or `ol` tag, the second one belongs to the `li` tag. If only one
attribute list is specified then it belongs to the `li` tag.

"""

from lexor.core.writer import NodeWriter
from lexor.command.lang import load_rel

NW = load_rel(__file__, 'nw')


class ListNW(NodeWriter):
    """Manage lists. """
    current = []
    display = []

    def start(self, node):
        self.current.append(node.name)
        self.display.append(NW.format_attributes(node))
        if self.writer.list_level == 0:
            self.writer.endl(False)
            self.write('%%{list}')
        self.writer.list_level += 1
        self.writer.indent = ' '*(self.writer.list_level+1)

    def end(self, node):
        self.writer.list_level -= 1
        if self.writer.list_level > 0:
            level = self.writer.list_level
            if node.next_element is not None:
                self.writer.indent = ''
                if self.current[-1] == 'ul':
                    self.write('^%s\n' % ('*'*(level+1)))
                else:
                    self.write('^%s\n' % ('+'*(level+1)))
            self.writer.indent = ' '*(level+1)
        else:
            self.writer.indent = ''
            self.write('%%')
            self.writer.endl(tot=2)
        self.display.pop()
        self.current.pop()


class ListItemNW(NodeWriter):
    """List elements display. """

    def start(self, node):
        list_nw = self.writer.get_node_writer('ul')
        if len(list_nw.current) == 0:
            self.write('- ')
            self.writer.flush_buffer()
            return
        indent = self.writer.indent
        self.writer.indent = ''

        self.writer.endl(False)
        if list_nw.current[-1] == 'ul':
            self.write('*'*self.writer.list_level)
        else:
            self.write('+'*self.writer.list_level)
        if list_nw.display[-1]:
            self.write('{%s}' % list_nw.display[-1])
            list_nw.display[-1] = ''
        att = NW.format_attributes(node)
        if att != '':
            self.write('{%s} ' % att)
        else:
            self.write(' ')
        self.writer.flush_buffer()
        self.writer.indent = indent

    def end(self, _):
        self.writer.endl(False, tail=False)


class LexorListItemNW(NodeWriter):
    """Display Lexor list items. """

    def start(self, node):
        self.writer.endl(False, tail=False)
        char = '*'
        if node['type'] == 'ol':
            char = '+'
        self.writer.indent = ''
        indent_level = node['level'] + 1
        if 'flag' in node and node['flag'] == 'close':
            self.write('^')
            indent_level -= 1
        self.write(char*node['level']+' ')
        self.writer.flush_buffer(tail=True)
        self.writer.indent = ' '*indent_level

    def end(self, node):
        if node.next is None:
            self.writer.indent = ''
