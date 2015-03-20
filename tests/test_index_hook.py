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
import shaney.faxlore
from cStringIO import StringIO

# This mock class is crappy and incomplete, and there is a Python mock
# module. But heaven forbid we should use software that exists; that
# would be insecure.
class Mock(object):
    def __init__(self):
        self.calls = []
        self.getattrs = []

    def __getattr__(self, name):
        self.getattrs.append(name)
        def recordkeeper(*args, **kwargs):
            self.calls.append((name, args, kwargs))
        return recordkeeper

class TestIndexHook(unittest.TestCase):
    def testIncludeParameter(self):
        """The index hook rejects false class includes [4594]."""
        m = Mock()
        shaney.faxlore.index_hook('    include => "foo",', m)
        if len(m.calls) > 0:
            self.fail('index_hook wrongly indexed an unfortunately-' \
                    'named class parameter')

    def testIncludeColonColon(self):
        """The index hook accepts nested class includes [4595]."""
        m = Mock()
        shaney.faxlore.index_hook('    include a::b', m)
        self.assertEqual(m.calls, [
            ('index_entry', ('class', 'a::b'), {}),])

    def testIncludeDashInName(self):
        """The index hook accepts includes with dashes in the class name
        [4597]."""
        m = Mock()
        shaney.faxlore.index_hook('    include a-b', m)
        self.assertEqual(m.calls, [
            ('index_entry', ('class', 'a-b'), {}),])

if __name__ == '__main__':
    unittest.main()
