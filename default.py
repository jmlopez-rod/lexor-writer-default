"""LEXOR: DEFAULT Writer Style

The goal of this style is to take any file, treat it as HTML and
write it in the lexor format. The lexor format is still being
developed. It will essentially be derived from Markdown, Kramdown,
pandoc and other preprocessors out there.

"""

from lexor import init, load_aux

INFO = init(
    version=(0, 0, 1, 'rc', 0),
    lang='lexor',
    type='writer',
    description='Writes files in the lexor format.',
    url='http://jmlopez-rod.github.io/lexor-lang/lexor-writer-default',
    author='Manuel Lopez',
    author_email='jmlopez.rod@gmail.com',
    license='BSD License',
    path=__file__
)
DEFAULTS = {
    'width': '70',
    'add_block': '',
    'del_block': '',
    'header': 'setext'
}
MOD = load_aux(INFO)['nw']
MAPPING = {
    'li': MOD.ListItemNW,
    'h1': MOD.HeaderNW,
    'hr': MOD.HRuleNW,
    'a': MOD.AnchorNW,
    'i': MOD.EmNW,
    'em': MOD.EmNW,
    'strong': MOD.StrongNW,
    'p': MOD.ParagraphNW,
    '#document': MOD.DocumentNW,
    '#text': MOD.TextNW,
    '#entity': MOD.EntityNW,
    '#comment': MOD.CommentNW,
    '#doctype': MOD.DoctypeNW,
    '#cdata-section': MOD.CDataNW,
    '__default__': MOD.DefaultNW,
}
for item in ['h2', 'h3', 'h4', 'h5', 'h6']:
    MAPPING[item] = 'h1'

def pre_process(writer, _):
    """Sets the default width for the writer. """
    writer.header = writer.defaults['header']
    writer.width = int(writer.defaults['width'])
    writer.pre_node = 0
    for name in writer.defaults['add_block'].split(','):
        if name and name not in MOD.BLOCK:
            MOD.BLOCK.append(name)
    for name in writer.defaults['del_block'].split(','):
        try:
            MOD.BLOCK.remove(name)
        except ValueError:
            pass
