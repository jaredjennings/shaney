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
"""Information about DoDI 8500.2 IA controls.

names is a dictionary containing the names of all IA controls, for every
system profile (combination of mission assurance category and
sensitivity). ::

    >>> ia_controls.names['EBBD-3']
    'Boundary Defense'

for_system_profile is a dictionary whose keys are system profile names,
as written in the STIGs received from DISA in XCCDF format (e.g.
'MAC-3_Sensitive'). For each such key, the value is a tuple of all
identifiers for IA controls which apply to that system profile (one such
identifier may be 'COAS-1').

    >>> len(len(ia_controls.names)
    157
    >>> len(ia_controls.for_system_profile['MAC-3_Sensitive'])
    100
    >>> ia_controls.for_system_profile['MAC-3_Sensitive'][0]
    'COAS-1'

"""

try:
    from pkg_resources import resource_string, resource_listdir
    _files = lambda: resource_listdir('shaney', 'ia_controls_info')
    # resource_string uses only /, not os.path.sep
    _contents = lambda fn: resource_string('shaney',
                'ia_controls_info/' + fn)
except ImportError:
    # Don't have setuptools or other similar. Use __file__
    import os
    _iac_info_dir = os.path.join(
            os.path.dirname(__file__),
            'ia_controls_info')
    _files = lambda: os.listdir(_iac_info_dir)
    _contents = lambda fn: file(os.path.join(_iac_info_dir, fn)).read()

_all_colon_separated = _contents('names.txt')
# [:-1]: discard last item, which will be an empty string
_lines = _all_colon_separated.split('\n')[:-1]
# each line has exactly one colon, separating the IA control identifier
# and the IA control name
names = dict(x.strip().split(':') for x in _lines)

del _lines
del _all_colon_separated

for_system_profile = {}

for _fn in _files():
    if _fn.startswith('profile_') and _fn.endswith('.txt'):
        _profilename = _fn[len('profile_'):-len('.txt')]
        # [:-1]: discard empty string after last '\n'
        _iacs = tuple(_contents(_fn).split('\n')[:-1])
        for_system_profile[_profilename] = _iacs

del _fn
del _profilename
del _iacs
try:
    del _iac_info_dir
except NameError:
    pass
del _files
del _contents
