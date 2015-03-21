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
from __future__ import with_statement
"""Build the unified policy document.

All configuration of this process is accomplished with a configuration
file, written in this directory, named make_config.ini. If there is no
such file, defaults are used; see shaney/sourapples/defaults.ini.
"""

import os
import codecs
from glob import glob
import logging

from shaney.sourapples.attendant import prepare_for_tex_output
from shaney.sourapples.compliance2csv import compliance2csv
from shaney.sourapples.clean import main as clean_main

def build(config):
    log = logging.getLogger('build')
    # set up environment vars for LaTeX and BibTeX
    doc_dirs = config.get('latex_documentation', 'locations').split('\n')
    # The empty entry appears to cause LaTeX to look in all of its usual
    # system-wide places.
    os.environ['TEXINPUTS'] = os.path.pathsep.join(['.'] + doc_dirs + [''])
    os.environ['BIBINPUTS'] = os.path.pathsep.join(doc_dirs)

    log.info('cleaning first')
    clean_main()
    
    afg = config.attendant_file_gatherer
    atg = config.attendant_template_gatherer
    mvs = config.markvshaney
    pdflatex = config.make_latex_function('pdflatex')
    bibtex = config.make_latex_function('bibtex')
    makeindex = config.make_latex_function('makeindex')

    # make the attendant files TeX file
    afofn = config.get('attendant_files', 'output_file')
    with file(afofn, 'w') as output:
        tex_output = prepare_for_tex_output(output)
        for line in afg.operate_on_g(config.attendant_files):
            print >> tex_output, line

    # make the attendant templates TeX file
    aftfn = config.get('attendant_templates', 'output_file')
    with file(aftfn, 'w') as output:
        tex_output = prepare_for_tex_output(output)
        for line in atg.operate_on_g(config.attendant_templates):
            print >> tex_output, line

    # build the policy, executive summary, and per-IAC stuff
    mvs.now_go()

    # concatenate per-IAC snippets into one LaTeX file
    with file(config.get('per_iac', 'output_file'), 'w') as o:
        for fn in sorted(glob(os.path.join(
                config.get('per_iac', 'output_dir'), '*'))):
            o.write(file(fn).read())

    pdflatex('main.tex')
    for name, source_ext, dest_ext in config.indices:
        source = 'main.' + source_ext
        dest = 'main.' + dest_ext
        makeindex('-o', dest, source)
    # BIBINPUTS setting above modifies behavior of bibtex here
    bibtex('main')
    pdflatex('main.tex')
    pdflatex('main.tex')

    # make compliance.csv
    with file('compliance.csv', 'w') as ccsv:
        utf8ccsv = codecs.getwriter('UTF-8')(ccsv)
        for line in compliance2csv(config.meanings,
                file('cyber_compliance.aux'),
                file('cyber_explanations.aux')):
            print >> utf8ccsv, line

    log.info('')
    log.info('******************************')
    log.info('End of make run.')
    log.info('Principal outputs:  %s', '  '.join([
        'main.pdf',
        'compliance.csv',
    ]))
    log.info('******************************')


