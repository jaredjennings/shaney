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
def lines_to_file(file_handle):
    """Write lines to a file.

    Input: strings. (No Unicode handling.)
    Output: nothing.
    Side effects: writes to file_handle.

    Closes the file_handle given when the input ends.
    """
    def coro(target):
        try:
            while True:
                x = (yield)
                file_handle.write(x)
        except GeneratorExit:
            file_handle.close()
    return coro
