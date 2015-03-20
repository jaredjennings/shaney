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

def prime(g):
    """Prime a generator.

    For a generator x, you can't x.send(a_value) until you first
    call x.next() once. To save a line of code per generator, this
    function does that for you.

    Example::
        gen1 = fun_generator()
        gen1.next()
        # use gen1

        # -- or --
        gen1 = prime(fun_generator())
        # use gen1
    """
    g.next()
    return g

def pipe(*corofuncs):
    """Pipe generator coroutines together.
    
    For example, suppose you have three coroutines, a, b and c, each of
    which consumes values and sends something to its target; s, a
    source, which sends things; and t, which consumes values but doesn't
    send anything. Normally you would have to say something like this::

        t = prime(sink())
        c = prime(mul4(t))
        b = prime(add2(c))
        a = prime(negate(b))
        s = prime(source([2,3,4], a))

    With the pipe function, you can say this::

        p = prime(pipe(negate, add2, mul4, prime(sink())))
        s = prime(source([2,3,4], p))

    (Your editor does have parenthesis match highlighting, doesn't it?...)

    Each coroutine except the last must take one argument, the target.
    """
    if len(corofuncs) == 0:
        raise ValueError('a pipe must have more than 0 generators')
    # don't prime target
    thepipe = corofuncs[-1]
    if len(corofuncs) > 1:
        # >>> a = [0,1,2,3]
        # >>> a[-2:0:-1]
        # [2, 1]
        for previous in corofuncs[-2:0:-1]:
            thepipe = prime(previous(thepipe))
    # don't prime the last generator we stack on; that way the pipe will
    # be unprimed, as expected
    thepipe = corofuncs[0](thepipe)
    return thepipe

def identity(target):
    while True:
        x = (yield)
        target.send(x)

def null(target):
    while True:
        x = (yield)

def split(*targets):
    """Send output to multiple coroutines.

    You may find this difficult to use, because if more than one of the
    target coroutines has a common target, that target must already be
    bound to a variable, so that you can give its name. That means you
    have to construct latter parts of a pipeline before former ones.
    """
    while True:
        x = (yield)
        for t in targets:
            t.send(x)

def splitmerge(*corofuncs):
    """Send output to multiple coroutines, and gather it back again.
    """
    def coro(target):
        # hook up each coroutine to the same target, the given target;
        # this is the merge
        hooked_up = [prime(c(target)) for c in corofuncs]
        # now we split our input into each hooked_up coroutine
        return split(*hooked_up)
    return coro

def annotate_after(corofunc):
    return splitmerge(identity, corofunc)

def annotate_before(corofunc):
    return splitmerge(corofunc, identity)

def log(logger_name, log_level):
    l = logging.getLogger(logger_name)
    def coro(target):
        while True:
            x = (yield)
            l.log(log_level, '%r', x)
            target.send(x)
    return coro

def drop_tagged(tag):
    def coro(target):
        while True:
            value = (yield)
            if value[0] != tag:
                target.send(value)
    return coro

def take_tagged(tag):
    """Could have called this one grep."""
    def coro(target):
        while True:
            value = (yield)
            if value[0] == tag:
                target.send(value)
    return coro
