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
import shaney.requirement
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

class MockWith(Mock):
    def __init__(self, *methodnames):
        super(MockWith, self).__init__()
        for m in methodnames:
            # make each method be in dir(aninstance)
            setattr(self, m, getattr(self, m))

class TestRequirement(unittest.TestCase):
    def testImplements1(self):
        m = MockWith('on_implements')
        f = shaney.requirement.FindRequirementTags()
        f.add_listener(m)
        f.on_line('# \implements{unixsrg}{GEN000300}')
        self.assertEqual(m.calls, [
            ('on_implements', ('unixsrg', ['GEN000300'], False), {})])

    def testImplementsMultiple(self):
        m = MockWith('on_implements')
        f = shaney.requirement.FindRequirementTags()
        f.add_listener(m)
        f.on_line('# \implements{unixsrg}{GEN000300,GEN000400}')
        self.assertEqual(m.calls, [
            ('on_implements', ('unixsrg', [
                'GEN000300', 'GEN000400'], False), {})])

    def testDoneby1(self):
        m = MockWith('on_doneby')
        f = shaney.requirement.FindRequirementTags()
        f.add_listener(m)
        f.on_line('# \doneby{admins}{unixsrg}{GEN000300}')
        self.assertEqual(m.calls, [
            ('on_doneby', ('admins', 'unixsrg', ['GEN000300'], False), {})])


if __name__ == '__main__':
    unittest.main()
