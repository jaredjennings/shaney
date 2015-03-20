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
import subprocess
import logging

def make_run_and_log_if_error(executable):
    log = logging.getLogger('executing')
    sui = None
    if hasattr(subprocess, 'STARTUPINFO'):
        # We are running under Windows. Tell Windows not to open up
        # a console window for this subprocess.
        # http://code.activestate.com/recipes/409002-launching-a-subprocess-without-a-console-window/
        sui = subprocess.STARTUPINFO()
        sui.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    def execute(*args):
        to_exec = (executable,) + args
        log.info(' '.join(to_exec))
        p = subprocess.Popen((executable,) + args,
                stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, startupinfo=sui)
        out, err = p.communicate(None)
        if p.returncode != 0:
            for line in out.split('\n'):
                log.error('stdout: %s', line)
            for line in err.split('\n'):
                log.error('stderr: %s', line)
            raise subprocess.CalledProcessError(p.returncode,
                    to_exec)
    return execute

