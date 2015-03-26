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
from setuptools import setup

setup(
        name='shaney',
        description='Deal with literate Puppet code',
        long_description="""\
Turn literate Puppet code inside out, and perform other feats.

Take Puppet code with comments containing LaTeX inputs, and produce
LaTeX inputs with verbatim sections containing the Puppet code. Also
produce automatic summaries of statements of compliance posture.
""",
        version='1.12',
        author='Jared Jennings',
        author_email='jjennings@fastmail.fm',
        license='GPLv3',
        platforms='OS-independent',
        packages=['shaney', 'shaney.generators', 'shaney.sourapples',
                  'shaney.test', 'shaney.generators.test',
                  'shaney.sourapples.test'],
        entry_points = {
            'console_scripts': [
                'shaneyg = shaney.generators.main:main',
                'sourapples = shaney.sourapples.console_main:main',
                'sourapples_tk = shaney.sourapples.tk_main:main',
                'sourapples_clean = shaney.sourapples.clean:main',
            ],
        },
        include_package_data=True,
        )

