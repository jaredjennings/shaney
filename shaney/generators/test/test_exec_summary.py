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
from shaney.generators.exec_summary import executive_summary

class TestToplevelParagraphs(CoroutineTest):
    coroutine_under_test = executive_summary({
        'IAC-1': 'Time Waste Efficiency',
        'IAC-2': 'Prohibited Features Used Properly'})
    send = [
            ('implements', 'unixstig', ('BLABLA',), False),
            ('implements', 'iacontrol', ('IAC-1',), True),
            ('toplevel', '\implements{unixstig}{BLABLA} Do stuff.\n'),
            ('toplevel', 'And some other stuff.\n'),
            ('toplevel', '\n'),
            ('verbatim', 'bla\n'),
            ('implements', 'iacontrol', ('IAC-2',), False),
            ('toplevel', 'A second paragraph.\n'),
            ('toplevel', '\n'),
        ]
    expect = [
            ('begin_execsummary',),
            ('execsummary_iacontrol', 'IAC-1', 'Time Waste Efficiency'),
            ('execsummary_iacontrol', 'IAC-2',
                'Prohibited Features Used Properly'),
            ('end_execsummary',),
        ]

if __name__ == '__main__':
    unittest.main()
