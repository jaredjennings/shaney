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
import re
import logging
import os.path
from collections import defaultdict
from shaney.generators.labels import sanitize_label

#from shaney.generators.requirement import requirement_tags_to_interpret
# don't tag paragraphs with \bydefault in them
requirement_tags_to_interpret = ('implements', 'doneby')

def puppet_labels_for_per_iac(dirs_to_strip):
    def coro(target):
        log = logging.getLogger('puppet_labels_for_per_iac')
        while True:
            value = (yield)
            if value[0] == 'new_file':
                filename = value[1]
                pieces = filename.split(os.path.sep)[dirs_to_strip:]
                filename = os.path.sep.join(pieces)
                label = sanitize_label(filename)
                target.send( ('label_for_paragraph', label) )
    return coro

def latex_labels_for_per_iac(target):
    while True:
        x = (yield)
        if x[0] == 'toplevel':
            line = x[1].strip()
            m = re.findall('\\label{([^}]+)}', line)
            if m:
                target.send( ('label_for_paragraph', m[0]) )


def tag_iac_paragraphs(target):
    """Transcribe paragraphs notated as implementing IA controls.
    
    Input: tuples of the forms:
        ('new_file', filename)
        ('implements', 'iacontrol', 
                tuple of IA control identifiers, True or False)
        ('implements', any other string, anything)
        ('doneby', any string, 'iacontrol', 
                tuple of IA control identifiers, True or False)
        ('doneby', any string, any other string, anything)
        ('paragraph', tuple of strings)
        (any other string, anything)
    Output: tuples of the form:
        (IA control identifier, tuple of strings)
    Does not pass messages through.

    A given paragraph may pertain to more than one IA control; if so it
    will result in more than one output tuple.
    """
    log = logging.getLogger('per_iac_output')
    iacs_applying_to_next_paragraph = set()
    last_label = None
    last_cited = defaultdict(lambda: None)
    while True:
        value = (yield)
        if value[0] == 'label_for_paragraph':
            last_label = value[1]
        elif value[0] in requirement_tags_to_interpret:
            document, controls, derived = value[-3:]
            if document == 'iacontrol':
                iacs_applying_to_next_paragraph |= set(controls)
        elif value[0] == 'paragraph':
            lines = value[1]
            for iac in iacs_applying_to_next_paragraph:
                if last_label != last_cited[iac]:
                    target.send( (iac, ('excerpt_from', last_label)) )
                    last_cited[iac] = last_label
                for line in lines:
                    target.send( (iac, ('toplevel', line)) )
                # send blank line not included at end of para
                target.send( (iac, ('toplevel', '\n')) )
            iacs_applying_to_next_paragraph.clear()
