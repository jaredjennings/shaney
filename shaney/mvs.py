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
import sys
import logging

from textpush import (splitmerge, pipe, prime, identity, log,
                      drop_tagged, take_tagged, null)
from textpush.input import push_lines_from_files
from textpush.output import lines_to_file
from shaney.generators.comments import sort_comments, invert_comments
from shaney.generators.autoindex import autoindex
from shaney.generators.labels import (
    buffer_labels_till_first_latex_line,
    labels_for_files, labels_for_modules)
from shaney.generators.requirement import (
    find_implements, find_doneby, find_bydefault,
    find_ia_control_tags)
from shaney.generators.latex import (
    lines_to_toplevel, LatexEmitter, neutralize_verb_tag)
from shaney.generators.exec_summary import executive_summary
from shaney.generators.paragraphs import paragraphs
from shaney.generators.per_iac import (
    puppet_labels_for_per_iac, latex_labels_for_per_iac,
    tag_iac_paragraphs)
from shaney.generators.per_iac_output import latex_to_files_in
from shaney.per_iac_pre import (
    write_empty_sections, write_special_sections)

from shaney import ia_controls


class MarkVShaney(object):
    def __init__(self, nToStrip, latex_files, puppet_files, checklists,
            per_iac_special_dir, per_iac_empty_template, policy_output,
            exec_summary_output, per_iac_output_dir):
        self.nToStrip = nToStrip
        self.latex_files = latex_files
        self.puppet_files = puppet_files
        self.checklists = checklists
        self.per_iac_special_dir = per_iac_special_dir
        self.per_iac_empty_template = per_iac_empty_template
        self.policy_output = policy_output
        self.exec_summary_output = exec_summary_output
        self.per_iac_output_dir = per_iac_output_dir
        self.log = logging.getLogger('MarkVShaney')

    def prepare(self):
        self.log.debug('There are %d LaTeX files', len(self.latex_files))
        self.log.debug('There are %d Puppet files', len(self.puppet_files))
        self.write_the_iac_files = prime(latex_to_files_in(self.per_iac_output_dir,
                    ia_controls.names)(None))
        # since the latex_to_files_in doesn't emit messages, it doesn't matter
        # what comes after it in the pipe; but pipe expects to call something
        # with one argument
        self.write_iac_files_pipe_entry = lambda t: self.write_the_iac_files
        self.write_exec_summary = prime(pipe(
                executive_summary(ia_controls.names),
                LatexEmitter('exec_summary'),
                lines_to_file(self.exec_summary_output),
                None))
        self.write_exec_summary_splitmerge_entry = \
                lambda t: self.write_exec_summary
        find_each_indirect_iacs = [find_ia_control_tags(name, meaning,
                ia_controls.for_system_profile[meaning.profile_id])
            for (name, meaning) in self.checklists.items()]
        self.add_all_indirect_iacs = splitmerge(*(
            find_each_indirect_iacs + [identity]))

    def prepare_per_iac(self):
        write_empty_sections(self.per_iac_empty_template,
                self.per_iac_output_dir)
        # when we have an exec_summary, we need to poke the values in
        # take_credit_for into it before we start the pipeline going
        if self.per_iac_special_dir is not None:
            take_credit_for = write_special_sections(self.per_iac_special_dir,
                    self.write_the_iac_files)
            self.write_exec_summary.send(('implements', 'iacontrol', 
                tuple(take_credit_for), False))

    def do_latex_files(self):
        go = push_lines_from_files(self.latex_files)
        master = pipe(
                splitmerge(identity, lines_to_toplevel),
                splitmerge(latex_labels_for_per_iac, identity),
                splitmerge(
                    lambda t: pipe(neutralize_verb_tag, 
                        splitmerge(
                            find_implements,
                            find_doneby),
                        t),
                    identity),
                self.add_all_indirect_iacs,
                splitmerge(identity, paragraphs),
                tag_iac_paragraphs,
                self.write_the_iac_files)
        go(prime(master))


    def do_puppet_files(self):
        go = push_lines_from_files(self.puppet_files)
        input_stage = splitmerge(
                identity,
                lambda t: pipe(sort_comments, invert_comments, t))
        label_stage = lambda t: pipe(
                splitmerge(
                    identity,
                    labels_for_files(self.nToStrip),
                    labels_for_modules(self.nToStrip)),
                buffer_labels_till_first_latex_line,
                autoindex,
                t)
        add_written_reqs = splitmerge(
                find_implements,
                find_doneby,
                find_bydefault,
                identity)
        do_policy_output = lambda t: pipe(
                drop_tagged('line'),
                LatexEmitter('policy'),
                lines_to_file(self.policy_output),
                t)
        per_iac_output = lambda t: pipe(
                # grab both implements (from upstream) and paragraphs
                splitmerge(identity, paragraphs),
                splitmerge(puppet_labels_for_per_iac(self.nToStrip), identity),
                tag_iac_paragraphs,
                self.write_iac_files_pipe_entry,
                t)
        master = pipe(
                splitmerge(identity, lambda t: pipe(
                        take_tagged('new_file'),
                        log('reading', logging.DEBUG),
                        null,
                        t)),
                input_stage,
                label_stage,
                add_written_reqs,
                self.add_all_indirect_iacs,
                splitmerge(
                    self.write_exec_summary_splitmerge_entry,
                    per_iac_output,
                    do_policy_output),
                lambda t: null(t))
        go(prime(master))

    def now_go(self):
        self.prepare()
        self.prepare_per_iac()
        self.do_latex_files()
        self.do_puppet_files()
        self.write_the_iac_files.close()
        self.write_exec_summary.close()
