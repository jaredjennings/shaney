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
import unittest
from shaney.generators.test import CoroutineTest
from shaney.generators.comments import sort_comments, invert_comments

class TestSortComments(CoroutineTest):
    coroutine_under_test = sort_comments
    send = [
            ('new_file', 'foo'),
            ('line', '#!a hashbang'),
            ('line', '# commented line 1'),
            ('line', 'uncommented line 2'),
            ('line', '# commented line 3'),
        ]
    expect = [
            ('comment', ' commented line 1'),
            ('toplevel', 'uncommented line 2'),
            ('comment', ' commented line 3'),
        ]

class TestInvertComments(CoroutineTest):
    coroutine_under_test = invert_comments
    send = [
            ('comment', ' commented line 1'),
            ('toplevel', 'uncommented line 2'),
            ('comment', ' commented line 3'),
        ]
    expect = [
            ('toplevel', ' commented line 1'),
            ('verbatim', 'uncommented line 2'),
            ('toplevel', ' commented line 3'),
        ]

if __name__ == '__main__':
    unittest.main()
