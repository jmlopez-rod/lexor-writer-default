"""LEXOR: DEFAULT writer INLINE test

Testing suite to write LEXOR in the DEFAULT style.

"""

import lexor
from lexor.command.test import compare_with

DOCUMENT = """
"""

EXPECTED = """
"""


def test_default():
    """lexor.writer.default.inline """
    doc, _ = lexor.parse(DOCUMENT, 'html')
    doc.style = 'default'
    #compare_with(str(doc), EXPECTED)
