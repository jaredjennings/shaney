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
import os.path
from textpush import pipe, prime, log
from shaney.generators.latex import LatexEmitter
from textpush.output import lines_to_file

class AbracaDict(dict):
    """Construct items when they don't exist, and remember them.

    This is suspiciously similar to a defaultdict, but the defaultdict
    calls its factory with no arguments, and here we hand the factory
    one argument.
    """
    def __init__(self, factory):
        self.factory = factory
    def __getitem__(self, name):
        if not self.has_key(name):
            self[name] = self.factory(name)
        return super(AbracaDict, self).__getitem__(name)


def latex_to_files_in(directory_name, iac_titles):
    """Write lines to any of several files.

    Input: tuples of the form:
        (filename, anything)
    Output: nothing, to the given target.

    Sends each "anything" to a LatexEmitter pointed at the named file in
    the directory passed as a parameter.

    Closes all files when the input ends.
    """
    def coro(target):
        def summon_file_for_iac(iac):
            f = file(os.path.join(directory_name, iac), 'w')
            print >> f, "\\section{%s: %s}" % (iac, iac_titles[iac])
            print >> f, "\\label{iac-%s}" % iac
            return prime(pipe(
                LatexEmitter(iac),
                prime(lines_to_file(f)(None))))
        outputs = AbracaDict(summon_file_for_iac)
        try:
            while True:
                # this particular generator is constructed, used for one
                # thing, then passed to a pipe call for another purpose,
                # which tries to prime it again. this is a horrible
                # hack:
                thing = (yield)
                if thing is not None:
                    iac, message = thing
                    outputs[iac].send(message)
        except GeneratorExit:
            for g in outputs.values():
                g.close()
    return coro

