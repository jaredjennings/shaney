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
import shaney.event

class TestEventer(unittest.TestCase):
    def testFire(self):
        class Receives(object):
            received = False
            def on_fire(self):
                self.received = True
        r = Receives()
        s = shaney.event.Eventer()
        s.add_listener(r)
        s.emit_fire()
        self.assertEqual(r.received, True)

if __name__ == '__main__':
    unittest.main()
