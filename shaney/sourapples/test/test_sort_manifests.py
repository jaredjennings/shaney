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
from upd_builder.sort_manifests import puppet_key

class TestPuppetSort(unittest.TestCase):
    def test_same_dir_normal(self):
        "Files are normally sorted alphabetically"
        ab = ['/foo/bar/blart.pp', '/foo/bar/baz.pp']
        ab = sorted(ab, key=puppet_key)
        self.assertEqual(ab, ['/foo/bar/baz.pp', '/foo/bar/blart.pp'])

    def test_same_dir_init(self):
        "init.pp comes first in a directory"
        ab = ['/foo/bar/blart.pp', '/foo/bar/init.pp']
        ab = sorted(ab, key=puppet_key)
        self.assertEqual(ab, ['/foo/bar/init.pp', '/foo/bar/blart.pp'])

    def test_same_dir_site_init(self):
        "site.pp comes first, but after init.pp"
        ab = ['/foo/bar/blart.pp', '/foo/bar/site.pp', '/foo/bar/init.pp']
        ab = sorted(ab, key=puppet_key)
        self.assertEqual(ab, ['/foo/bar/init.pp', '/foo/bar/site.pp',
                              '/foo/bar/blart.pp'])

    def test_analogous_dir(self):
        "sub-sub-module files go right after the sub-module"
        ab = [
                '/foo/bar/aardvark.pp',
                '/foo/bar/balloon.pp',
                '/foo/bar/init.pp',
                '/foo/bar/plane.pp',
                '/foo/bar/balloon/zeppelin.pp',
                '/foo/bar/balloon/blimp.pp',
            ]
        ab = sorted(ab, key=puppet_key)
        self.assertEqual(ab, [
            '/foo/bar/init.pp',
            '/foo/bar/aardvark.pp',
            '/foo/bar/balloon.pp',
            '/foo/bar/balloon/blimp.pp',
            '/foo/bar/balloon/zeppelin.pp',
            '/foo/bar/plane.pp',
        ])

    def test_multiple_inits(self):
        ab = [
                '/foo/bar/zart/init.pp',
                '/foo/bar/zart/other.pp',
                '/foo/bar/bletch/init.pp',
                '/foo/bar/bletch/other2.pp',
            ]
        ab = sorted(ab, key=puppet_key)
        self.assertEqual(ab, [
            '/foo/bar/bletch/init.pp',
            '/foo/bar/bletch/other2.pp',
            '/foo/bar/zart/init.pp',
            '/foo/bar/zart/other.pp',
        ])

    def test_different_modules_dirs(self):
        "all modules-* files are sorted together"
        ab = [
                '/foo/modules-foo/mod2/manifests/init.pp',
                '/foo/modules-ubb/mod1/manifests/init.pp',
            ]
        ab = sorted(ab, key=puppet_key)
        self.assertEqual(ab, [
            '/foo/modules-ubb/mod1/manifests/init.pp',
            '/foo/modules-foo/mod2/manifests/init.pp',
        ])

if __name__ == '__main__':
    unittest.main()
