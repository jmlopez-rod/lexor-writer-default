"""LEXOR: DEFAULT Writer Style

The goal of this style is to take any file, treat it as HTML and
write it in the lexor format. The lexor format is still being
developed. It will essentially be derived from Markdown, Kramdown,
pandoc and other preprocessors out there.

"""

from lexor import init, load_aux

INFO = init(
    version=(0, 0, 1, 'rc', 1),
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
    'header': 'setext',
    'hashheader': 'closed',
}
MOD = load_aux(INFO)
MAPPING = {
    'ul': MOD['list'].ListNW,
    'ol': 'ul',
    'li': MOD['list'].ListItemNW,
    'a': MOD['nw'].AnchorNW,
    'em': MOD['inline'].EmNW,
    'i': 'em',
    'strong': MOD['inline'].StrongNW,
    'hr': MOD['nw'].HRuleNW,
    'h1': MOD['header'].HeaderNW,
    'p': MOD['paragraph'].ParagraphNW,
    '#document': MOD['nw'].DocumentNW,
    '#text': MOD['nw'].TextNW,
    '#entity': MOD['nw'].EntityNW,
    '#comment': MOD['nw'].CommentNW,
    '#doctype': MOD['nw'].DoctypeNW,
    '#cdata-section': MOD['nw'].CDataNW,
    '__default__': MOD['nw'].DefaultNW,
}
for item in ['h2', 'h3', 'h4', 'h5', 'h6']:
    MAPPING[item] = 'h1'

def pre_process(writer, _):
    """Sets the default width for the writer. """
    writer.disable_raw()
    writer.enable_wrap()
    writer.header = writer.defaults['header']
    writer.width = int(writer.defaults['width'])
    writer.pre_node = 0
    writer.list_level = 0
    for name in writer.defaults['add_block'].split(','):
        if name and name not in MOD['nw'].BLOCK:
            MOD['nw'].BLOCK.append(name)
    for name in writer.defaults['del_block'].split(','):
        try:
            MOD['nw'].BLOCK.remove(name)
        except ValueError:
            pass
