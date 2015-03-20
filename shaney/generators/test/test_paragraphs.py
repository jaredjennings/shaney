# shaney - prepare Puppet code with LaTeX comments for multiple audiences.
# Based on <https://github.com/afseo/cmits>.
# Copyright (C) 2015 Jared Jennings, jjennings@fastmail.fm.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import logging
import unittest
from shaney.generators.test import CoroutineTest
from shaney.generators.paragraphs import paragraphs

class TestToplevelParagraphs(CoroutineTest):
    coroutine_under_test = paragraphs
    send = [
            ('implements', 'unixstig', ('BLABLA',), False),
            ('implements', 'iacontrol', ('IAC-1',), True),
            ('toplevel', '\implements{unixstig}{BLABLA} Do stuff.\n'),
            ('toplevel', 'And some other stuff.\n'),
            ('toplevel', '\n'),
            ('toplevel', 'A second paragraph.\n'),
            ('toplevel', '\n'),
        ]
    expect = [
            ('paragraph', (
                '\implements{unixstig}{BLABLA} Do stuff.\n',
                'And some other stuff.\n',
                )),
            ('paragraph', (
                'A second paragraph.\n',
                )),
        ]

class TestToplevelLastParagraph(CoroutineTest):
    coroutine_under_test = paragraphs
    send = [
            ('toplevel', 'No blank line, but at end of input.\n'),
        ]
    expect = [
            ('paragraph', ('No blank line, but at end of input.\n',)),
        ]

class TestToplevelAndVerbatim(CoroutineTest):
    coroutine_under_test = paragraphs
    send = [
            ('toplevel', 'A toplevel line.\n'),
            ('verbatim', 'A verbatim line.\n'),
            ('toplevel', 'End of input.\n'),
        ]
    expect = [
            ('paragraph', ('A toplevel line.\n',)),
            ('paragraph', ('End of input.\n',)),
        ]



if __name__ == '__main__':
    unittest.main()
