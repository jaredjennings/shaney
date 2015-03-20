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

def executive_summary(iac_names):
    """Make an `executive summary` of IA controls implemented.

    An executive summary, as defined, is a table of which IA controls
    this document covers. To construct one, we listen for all
    IA controls implemented, accumulate a set, and output it at the end
    of all things.

    Input: tuples of these forms:
        ('implements', 'iacontrol', tuple of IA control identifiers)
        ('implements', any other string, anything)
        (any other string, anything)
    Output: tuples of these forms:
        ('begin_execsummary',)
        ('execsummary_iacontrol', 
                IA control identifier,
                IA control title)
        ('end_execsummary',)
    Does not pass messages through.
    """
    log = logging.getLogger('executive_summary')
    def coro(target):
        implements = set()
        try:
            while True:
                value = (yield)
                if value is None:
                    pass
                elif value[0] == 'implements':
                    if value[1] == 'iacontrol':
                        implements |= set(value[2])
        except GeneratorExit:
            target.send( ('begin_execsummary',) )
            for imp in sorted(list(implements)):
                target.send( ('execsummary_iacontrol', imp, iac_names[imp]) )
            target.send( ('end_execsummary',) )
    return coro
