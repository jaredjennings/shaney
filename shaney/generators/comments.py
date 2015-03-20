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
def sort_comments(target):
    """Tease apart comments and non-comments; ignore hashbangs.
    
    Input: tuples of these forms:
        ('new_file', filename)
        ('line', line)
        (any other string, anything)
    Output: tuples of these forms:
        ('comment', line minus comment mark)
        ('toplevel', line)
    Does not pass messages through.
    """
    first_line = True
    while True:
        value = (yield)
        if value[0] == 'new_file':
            first_line = True
        elif value[0] == 'line':
            line = value[1]
            if first_line:
                if line.startswith('#!'):
                    # ignore
                    continue
            if line.startswith('#'):
                target.send( ('comment', line[1:]) )
            else:
                target.send( ('toplevel', line) )
        else:
            pass

def invert_comments(target):
    """Turn comments into toplevel, and toplevel into verbatim.

    Things written at the top level of a Puppet source file are Puppet
    code; things written in the comments are marked-up text meant for a
    formatter (we assume that formatter is LaTeX).

    But by the time we get to emitting the input that the formatter is
    intended to see, things written at the top level are marked-up text,
    and things written in verbatim blocks are Puppet code.

    This coroutine translates the sense of usual text from that of
    Puppet code to that of the document to be formatted.

    Input: tuples of these forms:
        ('comment', line)
        ('toplevel', line)
        (any other string, anything)
    Output: tuples of these forms:
        ('toplevel', line)
        ('verbatim', line)
        (any other string, anything)
    Passes messages through.
    
    """
    while True:
        value = (yield)
        if value[0] == 'comment':
            target.send( ('toplevel',) + value[1:] )
        elif value[0] == 'toplevel':
            target.send( ('verbatim',) + value[1:] )
        else:
            target.send(value)


