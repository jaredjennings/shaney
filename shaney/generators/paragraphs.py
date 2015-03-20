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

def paragraphs(target):
    """Groups markup lines into paragraphs.

    Input: tuples of these forms:
        ('toplevel', line)
        ('verbatim', line)
    Output: tuples of these forms:
        ('paragraph', list of lines)
    Does not pass messages through.
    """
    at_toplevel = False
    accumulated = []
    log = logging.getLogger('paragraphs')
    def burp(message):
        if len(accumulated) > 0:
            # avoid sending empty paragraphs
            target.send( ('paragraph', tuple(accumulated)) )
            del accumulated[:]
    try:
        while True:
            value = (yield)
            if value[0] == 'end_of_file':
                # paragraph has ended
                burp('end of file')
            if value[0] == 'toplevel':
                line = value[1]
                blank_line = re.match(r'^\s*$', line)
                if at_toplevel:
                    if blank_line:
                        # blank line ends paragraph.
                        burp('blank line')
                    else:
                        # paragraph is continued by this line
                        accumulated.append(line)
                else:
                    accumulated.append(value[1])
                at_toplevel = True
            elif value[0] == 'verbatim':
                if at_toplevel:
                    # verbatim line ends paragraph.
                    burp('toplevel line after verbatim')
                else:
                    # we continue in the verbatim
                    pass
                at_toplevel = False
            else:
                pass
    except GeneratorExit:
        # whatever we have accumulated is the last paragraph.
        burp('end of input')
