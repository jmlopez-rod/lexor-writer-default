"""LEXOR: INLINE NodeWriter

Here we define inline node writers.

"""

from lexor.core.writer import NodeWriter
from lexor.command.lang import load_rel

NW = load_rel(__file__, 'nw')


class StrongNW(NodeWriter):
    """Strong element display. """

    def start(self, node):
        self.write('**')

    def end(self, node):
        self.write('**')
        if node.attlen > 0:
            self.write('{%s}' % NW.format_attributes(node))


class EmNW(NodeWriter):
    """Strong element display. """

    def start(self, node):
        self.write('*')

    def end(self, node):
        self.write('*')
        if node.attlen > 0:
            self.write('{%s}' % NW.format_attributes(node))