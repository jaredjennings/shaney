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
from __future__ import with_statement
"""Prepare the per-IAC output directories.

This means writing empty per-IAC sections, and copying written (special)
per-IAC sections into place.
"""

import os.path
from glob import glob
from shaney import ia_controls

def write_empty_sections(per_iac_empty_template, iac_output_dir):
    """Write an empty section for each possible IA control.

    This is so the section numbers in the per-IAC chapter will never change,
    even if the policy expands and fulfills more IA controls in the future.
    (This could happen as more areas of the host's configuration come under
    policy control, or as the policy begins to control hosts in other mission
    assurance categories or with other sensitivities.)
    """
    lines = file(per_iac_empty_template, 'rt').readlines()
    lines = [l for l in lines if not l.startswith('##')]
    template = ''.join(lines)
    for id, title in ia_controls.names.items():
        with file(os.path.join(iac_output_dir, id), 'w') as f:
            to_write = template.replace('${id}', id).replace('${title}', title)
            f.write(unicode(to_write).encode('UTF-8'))


def write_special_sections(per_iac_special_dir, write_the_iac_files):
    """Copy special per-IAC text to the per-IAC output directory.

    "Special" means that the IA control in question is easy to write a
    fixed section of prose about, and it's hard to programmatically
    derive prose about it. For these we copy files from the
    per_iac_special_dir to the per-IAC output directory.

    If something pertaining to an IA control is programmatically found
    after the special section is copied into place, the programmatic
    text will overwrite the special text.
    """
    take_credit_for = []
    for special in glob(os.path.join(per_iac_special_dir, '*')):
        basename = os.path.basename(special)
        if basename != 'README':
            for line in file(special):
                # basename is the name of a file named after an IA control
                write_the_iac_files.send((basename, ('toplevel', line)))
            take_credit_for.append(basename)
    return take_credit_for
