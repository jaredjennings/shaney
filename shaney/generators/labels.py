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
import os.path
import logging

def sanitize_label(l):
    """You can't write a backslash in a label. Fix.

    We use filenames to construct labels. Under windows, those filenames
    contain backslashes. But backslashes are significant to LaTeX, even
    inside label names. So we neutralize them.
    """
    return l.replace('\\', '/')

def labels_for_files(dirs_to_strip):
    """Emits a label when a new file is detected.

    Input: tuples of these forms:
        ('new_file', filename)
        (any other string, anything)
    Output: tuples of these forms:
        ('label', most of filename)
    Does not pass messages through.
    """
    def coro(target):
        log = logging.getLogger('lff')
        while True:
            value = (yield)
            if value[0] == 'new_file':
                filename = value[1]
                pieces = filename.split(os.path.sep)[dirs_to_strip:]
                name = os.path.sep.join(pieces)
                target.send( ('label', sanitize_label(name)) )
            else:
                pass
    return coro

def labels_for_modules(dirs_to_strip):
    """Emits a label when a new Puppet module is detected.

    Input: tuples of these forms:
        ('new_file', filename)
        (any other string, anything)
    Output: tuples of these forms:
        ('label', module name)
    Does not pass messages through.
    """
    def coro(target):
        log = logging.getLogger('lfm')
        while True:
            value = (yield)
            if value[0] == 'new_file':
                filename = value[1]
                pieces = filename.split(os.path.sep)[dirs_to_strip:]
                if pieces[0] == 'modules' or \
                        pieces[0].startswith('modules-'):
                    if pieces[-2:] == ['manifests', 'init.pp']:
                        target.send( ('label', 'module_' + pieces[1]) )
                    else:
                        # this is a file belonging to a submodule, not a
                        # main module
                        pass
                else:
                    # this Puppet source does not belong to a module (e.g.
                    # it is in the manifests directory)
                    pass
            else:
                # message we don't care about
                pass
    return coro

def buffer_labels_till_first_latex_line(target):
    """
    The first LaTeX syntax line in a file is likely a section
    directive. If we emit the label before that directive, the
    label will point at the previous section, not this section.
    So we delay emitting the label until after.

    Input: tuples of these forms:
        ('new_file', filename)
        ('label', string)
        ('comment', line)
        ('toplevel', line)
        (any other string, anything)
    Output: tuples of any of the first four forms above.

    Passes messages through.
    """
    file_just_began = True
    preserved_labels = []
    log = logging.getLogger('bltfll')
    while True:
        value = (yield)
        if value[0] == 'new_file':
            file_just_began = True
            target.send(value)
        elif value[0] == 'label':
            if file_just_began:
                preserved_labels.append(value)
            else:
                target.send(value)
        elif value[0] == 'toplevel':
            target.send(value)
            line = value[1]
            # now, having sent that...
            if file_just_began:
                if line.strip() != '':
                    file_just_began = False
                    for l in preserved_labels:
                        target.send(l)
                    preserved_labels = []
        elif value[0] == 'verbatim':
            target.send(value)
            if file_just_began:
                # Welp, it looks like there's no LaTeX code at the beginning
                # of this file. No LaTeX, no section head. Go ahead and emit
                # the labels.
                file_just_began = False
                for l in preserved_labels:
                    target.send(l)
                preserved_labels = []
        else:
            target.send(value)


