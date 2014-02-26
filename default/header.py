"""LEXOR: HEADER NodeWriter

Lexor supports Setext and atx style headers. Setext style is enabled
by default. When the atx style is enabled then you may specify if
matching hashes should be placed at the end of the header.

"""

from lexor.core.writer import NodeWriter
from lexor.command.lang import load_rel

NW = load_rel(__file__, 'nw')


class HeaderNW(NodeWriter):
    """Writes a header element. """
    wrap_enabled = None

    def start(self, node):
        self.wrap_enabled = self.writer.wrap_enabled()
        if self.wrap_enabled:
            self.writer.disable_wrap()
        self.writer.endl(False)
        self.writer.endl()
        level = int(node.name[1])
        if self.writer.header == 'setext' and level < 3:
            pass
        else:
            self.write(('#'*level)+' ')

    def end(self, node):
        level = int(node.name[1])
        if self.writer.header == 'setext' and level < 3:
            if node.attlen > 0:
                if not self.writer.last().endswith(' '):
                    self.write(' ')
                self.write('{%s}' % NW.format_attributes(node))
            width = self.writer.pos[1] - 1
            self.writer.endl()
            if level == 1:
                self.write(('='*width))
            else:
                self.write(('-'*width))
        else:
            if self.writer.defaults['hashheader'] == 'closed':
                if not self.writer.last().endswith(' '):
                    self.write(' ')
                self.write(('#'*level))
            if node.attlen > 0:
                if not self.writer.last().endswith(' '):
                    self.write(' ')
                self.write('{%s}' % NW.format_attributes(node))
        self.write('\n\n')
        if self.wrap_enabled:
            self.writer.enable_wrap()
