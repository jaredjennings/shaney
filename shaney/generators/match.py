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
import re

def tagged_match(tag, regex):
    """Do something when a tag and a regex both match; passthrough.

    Constructs generators that take as input any of the following
    tuples:
        (tag, line)
        (any other string, anything)
    Output:
        (depends on the function tagged_match is decorating)
        (any other string, anything)
    Passes messages through.

    Example::
        @tagged_match('toplevel', r"^bla")
        def bla_at_beginning(match, value, target):
            target.send( ('i_saw_a_bla',) )
            # pass value through
            target.send(value)

        coro = bla_at_beginning(my_target)
    After this, coro is a coroutine which expects to be sent tuples
    (tag, value), like coro.send((tag, value)). It will send things on
    to my_target in like manner. If the tag is 'toplevel', and the regex
    matches, the body of bla_at_beginning will be called with the match.
    If either condition is not true, the value will be sent through to
    the target unmodified. (This behavior is not written in the body of
    bla_at_beginning; it's part of tagged_match.)
    
    Consequently if you have a pipeline A B C D E of such coroutines,
    where B is A's target, C is B's target and so on, the output at E's
    target will be at least what was input, and maybe more, if some of
    the regexes matched.
    """
    log = logging.getLogger('tagged_match')
    def gets_block(fn):
        def matcher(target):
            while True:
                value = (yield)
                if value[0] == tag:
                    text = value[1].strip()
                    m = re.findall(regex, text)
                    if m:
                        fn(m, value, target)
                    else:
                        target.send(value)
                else:
                    target.send(value)
        return matcher
    return gets_block

def tagged_match_or_drop(tag, regex):
    """Do something when a tag and a regex both match; no passthrough.

    Constructs generators that take as input any of the following
    tuples:
        (tag, line)
        (any other string, anything)
    Output:
        (depends on the function tagged_match is decorating)
    Does not pass messages through.

    Example::
        @tagged_match_or_drop('toplevel', r"^bla")
        def bla_at_beginning(match, value, target):
            target.send( ('i_saw_a_bla',) )

        coro = bla_at_beginning(my_target)
    After this, coro is a coroutine which expects to be sent tuples
    (tag, value), like coro.send((tag, value)). It will send only
    ('i_saw_a_bla',) tuples on to my_target.
    
    Consequently if you have a pipeline A B C D E of such coroutines,
    where B is A's target, C is B's target and so on, the output at E's
    target will be solely what E decided to say about what D said.
    """
    log = logging.getLogger('tagged_match_or_drop')
    def gets_block(fn):
        def matcher(target):
            while True:
                value = (yield)
                if value[0] == tag:
                    text = value[1].strip()
                    m = re.findall(regex, text)
                    if m:
                        fn(m, value, target)
        return matcher
    return gets_block

@tagged_match('toplevel', r'\\verb(.)([^\1]*)\1')
def neutralize_verb_tag(m, value, target):
    logging.getLogger('neutralize_verb_tag').debug('found a verb tag; m is %r', m)
    neutralized = value[1]
    # just in case there's more than one \verb
    for a_match in m:
        neutralized = neutralized.replace(r'\verb%s%s%s' % (
            a_match[0], a_match[1], a_match[0]), r'\verb!...!')
    target.send( (value[0], neutralized) )
