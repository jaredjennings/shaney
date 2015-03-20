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
from shaney.generators.requirement import find_implements

class TestFindImplementsMatch(CoroutineTest):
    """find_implements can find an \\implements tag:"""
    coroutine_under_test = find_implements
    send = [
            ('toplevel', '\\implements{unixstig}{BLABLA} Do stuff.\n'),
        ]
    expect = [
            ('implements', 'unixstig', ('BLABLA',), False),
        ]

class TestFindMultipleOnSameLine(CoroutineTest):
    """find_implements deals with multiple \\implements tags on same line:
        
    In all likelihood, an actual human author would not write it like
    this, but like::

        \implements{unixstig}{BLABLA}
        \implements{apachestig}{BLUBLU}
        Do stuff.
    """
    coroutine_under_test = find_implements
    send = [
            ('toplevel', '\\implements{unixstig}{BLABLA} ' \
                '\\implements{apachestig}{BLUBLU} Do stuff.\n'),
        ]
    expect = [
            ('implements', 'unixstig', ('BLABLA',), False),
            ('implements', 'apachestig', ('BLUBLU',), False),
        ]

class TestMultipleRequirementsMet(CoroutineTest):
    """find_implements deals with multiple requirements in one statement:
    """
    coroutine_under_test = find_implements
    send = [
            ('toplevel', '\\implements{unixstig}{BLABLA,BLUBLU} Do stuff.'),
        ]
    expect = [
            ('implements', 'unixstig', ('BLABLA','BLUBLU'), False),
        ]


if __name__ == '__main__':
    unittest.main()
