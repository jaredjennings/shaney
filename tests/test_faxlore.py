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

class TestFaxlore(unittest.TestCase):
    def testLabelForFilename(self):
        """Every time we begin a new input file, faxlore emits a label...
        
        after the first line of the file. If the first line of the file
        is a new \section, and we emit the filename label before that
        new \section, the label will point to the end of the previous
        section, not the beginning of this one. See [4557].
        """
        m = Mock()
        f = shaney.faxlore.Faxlore(emitter=m, dirs_to_strip=2)
        f.on_new_file('../../manifests/foo.pp')
        f.on_line('# just some LaTeX')
        self.assertEqual(m.calls, [
            ('toplevel', (' just some LaTeX',), {}),
            ('label', ('manifests/foo.pp',), {})])

    def testLabelForModule(self):
        """Labels are emitted for each module."""
        m = Mock()
        f = shaney.faxlore.Faxlore(emitter=m, dirs_to_strip=2)
        f.on_new_file('../../modules/foo/manifests/init.pp')
        f.on_line('# just some LaTeX')
        self.assertEqual(m.calls, [
            ('toplevel', (' just some LaTeX',), {}),
            ('label', ('modules/foo/manifests/init.pp',), {}),
            ('label', ('module_foo',), {}),])

    def testNoDuplicateModuleLabels(self):
        """Per-module labels are emitted only once for each module."""
        m = Mock()
        f = shaney.faxlore.Faxlore(emitter=m, dirs_to_strip=2)
        f.on_new_file('../../modules/foo/manifests/bar.pp')
        f.on_line('# just some LaTeX')
        self.assertEqual(m.calls, [
            ('toplevel', (' just some LaTeX',), {}),
            ('label', ('modules/foo/manifests/bar.pp',), {})])


    def testStraightPuppet(self):
        """Puppet code is output in verbatim blocks."""
        m = Mock()
        f = shaney.faxlore.Faxlore(emitter=m, dirs_to_strip=2)
        f.on_new_file('../../manifests/foo.pp')
        f.on_line('puppet code')
        f.on_line('more puppet code')
        f.on_end_of_input()
        self.assertEqual(m.calls, [
            ('label', ('manifests/foo.pp',), {}),
            ('verbatim', ('puppet code',), {}),
            ('verbatim', ('more puppet code',), {}),
            ('end', (), {})])

    def testStraightLatex(self):
        """Commented code is treated as LaTeX input."""
        m = Mock()
        f = shaney.faxlore.Faxlore(emitter=m, dirs_to_strip=2)
        f.on_new_file('../../manifests/foo.pp')
        f.on_line('# some latex code')
        f.on_end_of_input()
        self.assertEqual(m.calls, [
            ('toplevel', (' some latex code',), {}),
            ('label', ('manifests/foo.pp',), {}),
            ('end', (), {})])

if __name__ == '__main__':
    unittest.main()
