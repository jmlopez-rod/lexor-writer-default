"""LEXOR: DEFAULT writer NW test

Testing suite to write LEXOR in the DEFAULT style.

"""

import lexor
from lexor.command.test import compare_with

DOCUMENT = """
"""

EXPECTED = """
"""

def test_default():
    """lexor.writer.default.nw """
    #doc, _ = lexor.parse(DOCUMENT, 'lexor')
    #doc.style = 'default'
    #compare_with(str(doc), EXPECTED)
    pass
