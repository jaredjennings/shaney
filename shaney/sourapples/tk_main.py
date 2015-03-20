#!/usr/bin/python2.6
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
import time
from shaney.sourapples.config import SourApplesConfig
from shaney.sourapples.build import build
from shaney.sourapples.tk_log import run_and_view_log

def main():
    # We depend entirely on the configuration file, not on command line
    # arguments, because we may not be executed from a command line.
    config = SourApplesConfig()

    # set up logging
    loglevel = getattr(logging, config.get('main', 'loglevel'))
    def thestuff():
        # Without this sleep, the Tk GUI under Windows freezes before it
        # shows itself. I have no idea why.
        time.sleep(0.5)
        build(config)
    run_and_view_log(thestuff, loglevel)

if __name__ == '__main__':
    main()
