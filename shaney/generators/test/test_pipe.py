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
from shaney.generators.test import Sink
from shaney.generators import prime, pipe

def add(y):
    def g(target):
        while True:
            x = (yield)
            target.send(x+y)
    return g

def mul(y):
    def g(target):
        while True:
            x = (yield)
            target.send(x*y)
    return g

class TestPipe(unittest.TestCase):
    def testZeroMemberPipe(self):
        self.assertRaises(ValueError, pipe)

    def testOneMemberPipe(self):
        s = Sink()
        # pipe will call s() to get generator object
        p = prime(pipe(s))
        p.send(3)
        self.assertEqual(s.values, [3])

    def testTwoMemberPipe(self):
        s = Sink()
        sg = prime(s())
        p = prime(pipe(add(1), sg))
        p.send(3)
        self.assertEqual(s.values, [4])

    def testThreeMemberPipe(self):
        s = Sink()
        sg = prime(s())
        p = prime(pipe(add(1), mul(3), sg))
        p.send(4)
        # add(1) happens first -> 5
        # then mul(3) -> 15
        self.assertEqual(s.values, [15])

if __name__ == '__main__':
    unittest.main()
