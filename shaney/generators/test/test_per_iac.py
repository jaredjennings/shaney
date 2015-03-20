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
from shaney.generators import pipe, log, splitmerge, identity
from shaney.generators.test import CoroutineTest
from shaney.generators.paragraphs import paragraphs
from shaney.generators.per_iac import per_iac_output

class TestSingleParagraph(CoroutineTest):
    coroutine_under_test = per_iac_output
    send = [
            ('implements', 'unixstig', ('BLABLA',), False),
            ('implements', 'iacontrol', ('IAC-1',), True),
            ('paragraph', (
                '\implements{unixstig}{BLABLA} Do stuff.\n',
                'And some other stuff.\n',
                 )),
            ('paragraph', (
                'A second paragraph.\n',
                )),
        ]
    expect = [
            ('IAC-1', (
                '\implements{unixstig}{BLABLA} Do stuff.\n',
                'And some other stuff.\n',
                )),
        ]



if __name__ == '__main__':
    unittest.main()
