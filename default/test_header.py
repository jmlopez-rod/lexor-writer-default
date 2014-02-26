"""LEXOR: DEFAULT writer HEADER test

Testing suite to write LEXOR in the DEFAULT style.

"""

import lexor
from lexor.command.test import compare_with

DOCUMENT = """
<h1>First level header</h1>
<h2 class="blue">Second level header</h2>
<h3 id="h3header">H3 header</h3>
<h4>H4 header</h4>
<h5>H5 header</h5>
<h6>H6 header</h6>
"""

EXPECTED = """
First level header
==================


Second level header {.blue}
---------------------------


### H3 header ### {#h3header}


#### H4 header ####


##### H5 header #####


###### H6 header ######

"""
EXPECTED_OPEN = """
# First level header


## Second level header {.blue}


### H3 header {#h3header}


#### H4 header


##### H5 header


###### H6 header

"""


def test_default():
    """lexor.writer.default.header """
    doc, _ = lexor.parse(DOCUMENT, 'html')
    doc.lang = 'lexor'
    doc.style = 'default'
    compare_with(str(doc), EXPECTED)
    doc.defaults = {
        'header': 'hash',
        'hashheader': 'open',
    }
    compare_with(str(doc), EXPECTED_OPEN)
