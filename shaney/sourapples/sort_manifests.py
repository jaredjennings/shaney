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
from os.path import sep

def puppet_key(x):
    """Sort full path names of Puppet manifest files in a way that makes sense.

    Making sense is defined as:
    * init.pp comes first in a directory, then site.pp, then everything else;
    * all foo/*.pp come right after foo.pp;
    * other than that, files and directories are sorted alphabetically within a
      directory.
    """

    # ('a',) < ('a', 'b') < ('b',)
    x = x.split(sep)
    # different modules directories should all be sorted together.
    # In Python 2.5 or later, we would say
    #   ['modules' if a.startswith('modules-') else a for a in x]
    x = [a.startswith('modules-') and 'modules' or a for a in x]
    # it appears that any number is less than a string
    if x[-1].endswith('init.pp'):
        x[-1] = 0
    elif x[-1].endswith('site.pp'):
        x[-1] = 1
    else:
        # where a is a puppet file, we strip off the suffix so it will
        # come before its sub-files
        if x[-1].endswith('.pp'):
            x[-1] = x[-1][:-len('.pp')]
    return x
