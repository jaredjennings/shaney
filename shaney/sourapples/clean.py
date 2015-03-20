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
import os
import shutil
from glob import glob

from shaney.sourapples.config import SourApplesConfig

def rm_rf(*args):
    for a in args:
        for ga in glob(a):
            shutil.rmtree(ga, True)

def rm_f(*args):
    for a in args:
        for ga in glob(a):
            try:
                os.unlink(ga)
            except OSError:
                pass

def main():
    c = SourApplesConfig()
    rm_f('main.pdf')
    for sec in ('policy', 'attendant_files', 'per_iac', 'exec_summary'):
        rm_f(c.get(sec, 'output_file'))
    rm_f('*.aux', '*.log', '*.toc', '*.out')
    rm_f('*.idx', '*.ind', '*.ilg')
    rm_f('*.bbl', '*.blg')
    rm_rf(c.get('per_iac', 'output_dir'))


if __name__ == '__main__':
    main()
