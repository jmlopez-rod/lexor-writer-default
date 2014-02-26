"""LEXOR: PARAGRAPH NodeWriter

Node writer description.

"""

from lexor.core.writer import NodeWriter
from lexor.command.lang import load_rel

NW = load_rel(__file__, 'nw')


class ParagraphNW(NodeWriter):
    """Write a paragraph. """

    def start(self, node):
        self.writer.flush_buffer(False)
        if node.parent.name in ['li'] and node.element_index == 0:
            pass
        else:
            if self.writer.pos[1] != 1:
                self.writer.endl(tot=2)
            elif not self.writer.last().endswith('\n\n'):
                self.writer.endl()
        if node.attlen > 0:
            att = NW.format_attributes(node)
            self.write('%%%%{%s' % node.name)
            if att != '':
                self.write(' %s' % att)
            self.write('}')

    def end(self, node):
        if node.attlen > 0:
            self.write('%%')
        self.writer.flush_buffer(False)
        if self.writer.pos[1] == 1:
            self.writer.endl()
        else:
            self.writer.endl(tot=2)
