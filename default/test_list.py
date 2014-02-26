"""LEXOR: DEFAULT writer LIST test

Testing suite to write LEXOR in the DEFAULT style.

"""

import lexor
from lexor.command.test import compare_with

DOCUMENT = """
<ol>
    <li>level 1: first
        <ol>
            <li>Level 2
                <ul>
                    <li>Level 3
                        <ol><li>Level 4</li>
                        </ol>
                    </li>
                </ul>
            </li>
        </ol>
        <p>This is a paragraph in level 1</p>
    </li>
    <li>level 1: second
        <ul>
            <li>Level 2: first
                <ul>
                    <li>Level 3: first</li>
                    <li>Level 3: second
                        <ul>
                            <li>Level 4: first
                            </li>
                        </ul>
                    </li>
                    <li>Level 3: third
                    </li>
                </ul>
            </li>
            <li><p>Level 2: second</p>
                <ol>
                    <li>Level 3: first</li>
                    <li>Level 3: second</li>
                    <li>Level 3: third</li>
                    <li>Level 3: fourth</li>
                </ol>
                <p>Level 2 other content</p>
            </li>
            <li>Level 2: third</li>
            <li>Level 2: fourth</li>
            <li><p>Level 2: cinco. This is a lengthy item.</p>
                <p>Which reminds me, there are a few things
                    that I wish put into a list:
                </p>
                <ul>
                    <li>Level 3: uno</li>
                    <li>Level 3: dos</li>
                    <li>Level 3: tres</li>
                    <li>Level 3: cuatro</li>
                    <li>Level 3: cinto</li>
                    <li>Level 3: seis</li>
                </ul>
                <p>That is all.</p>
                <p>Nope, not really</p>
                <ol>
                    <li>car</li>
                    <li>bike</li>
                </ol>
                <p>Now I'm done.</p>
            </li>
        </ul>
    </li>
    <li><p>Level 1: item tres</p></li>
</ol>
"""
EXPECTED = """%%{list}
+ level 1: first
++ Level 2
*** Level 3
++++ Level 4
^++

  This is a paragraph in level 1

+ level 1: second
** Level 2: first
*** Level 3: first
*** Level 3: second
**** Level 4: first
*** Level 3: third
** Level 2: second

+++ Level 3: first
+++ Level 3: second
+++ Level 3: third
+++ Level 3: fourth
^+++

   Level 2 other content

** Level 2: third
** Level 2: fourth
** Level 2: cinco. This is a lengthy item.

   Which reminds me, there are a few things that I wish put into a
   list:

*** Level 3: uno
*** Level 3: dos
*** Level 3: tres
*** Level 3: cuatro
*** Level 3: cinto
*** Level 3: seis
^***

   That is all.

   Nope, not really

+++ car
+++ bike
^+++

   Now I'm done.

+ Level 1: item tres

%%

"""


def test_default():
    """lexor.writer.default.list """
    doc, _ = lexor.parse(DOCUMENT, 'html')
    doc.lang = 'lexor'
    doc.style = 'default'
    compare_with(str(doc), EXPECTED)
