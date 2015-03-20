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
import os

def make_walk_and_prune(prune_dirs_named=[]):
    """Make a function that walks dir, not traversing into some subdirs.
    prune_dirs_named is a list of directory names into which not to
    traverse. Returns a function that works like os.walk.
    """
    log = logging.getLogger('walk_and_prune')
    def walk_and_prune(dir):
        for root, dirs, files in os.walk(dir):
            yield (root, dirs, files)
            for pd in prune_dirs_named:
                if pd in dirs:
                    dirs.remove(pd)
    return walk_and_prune

def puppet_manifests_under(dir, walker=os.walk):
    """Find all the Puppet files under dir.

    We reject SELinux policy packages (which also have the extension
    'pp') which must have the extension *.selinux.pp. The alternative is
    to exclude all files under */files/* directories, but then if anyone
    writes a module or submodule called files, the Puppet manifests
    inside it would mysteriously not be shown.
    """
    for root, dirs, files in walker(dir):
        for f in files:
            if f.endswith('.pp') and not f.endswith('.selinux.pp'):
                yield os.path.join(root, f)

def attendant_files_under(dir, walker=os.walk,
        assumed_path_element='files'):
    strings = {
            'S': os.path.sep,
            'A': assumed_path_element,
    }
    for root, dirs, files in walker(dir):
        # Anywhere under a directory named assumed_path_element, yield
        # all files.
        if root.endswith('%(S)s%(A)s' % strings) \
                or ('%(S)s%(A)s%(S)s' % strings) in root:
            for f in files:
                yield os.path.join(root, f)

def latex_files_under(dir, walker=os.walk):
    for root, dirs, files in walker(dir):
        for f in files:
            if f.endswith('.tex') and not f.startswith('.'):
                yield os.path.join(root, f)
