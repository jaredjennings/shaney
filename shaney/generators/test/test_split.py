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
from shaney.generators import prime, splitmerge

def find(needle):
    def coro(target):
        while True:
            x = (yield)
            if needle in x:
                target.send('%s found' % needle)
    return coro

class CommonSend(object):
    send = [
            'the quick brown fox jumped over the lazy dog',
            'she sells seashells by the seashore',
            'dennis, there\'s some lovely filth over here',
            'well, she turned me into a newt',
            'a newt?',
            '...',
            'i got better',
            'fox news',
        ]

class TestSingleFind(CommonSend, CoroutineTest):
    coroutine_under_test = find('fox')
    expect = [
            'fox found',
            'fox found',
        ]


class TestSplitMerge(CommonSend, CoroutineTest):
    coroutine_under_test = splitmerge(find('fox'), find('newt'))
    expect = [
            'fox found',
            'newt found',
            'newt found',
            'fox found',
        ]


if __name__ == '__main__':
    unittest.main()
