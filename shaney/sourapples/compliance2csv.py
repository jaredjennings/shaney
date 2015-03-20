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

import sys
import os.path
import logging

def parse_compliance(compliance_aux):
    compliance = {}
    for l in compliance_aux:
        document, requirement, status = l.strip().split(':')
        compliance.setdefault(document, {})
        compliance[document][requirement] = status
    return compliance

def parse_explanations(explanations_aux):
    explanations = {}
    state = 0
    lastd = None
    lastr = None
    for l in explanations_aux:
        if state == 0:
            document, requirement, throwaway = l.strip().split(':')
            explanations.setdefault(document, {})
            explanations[document][requirement] = ''
            lastd = document
            lastr = requirement
            state = 1
        elif state == 1:
            if l.strip() == ':':
                state = 0
            else:
                explanations[lastd][lastr] += l
    return explanations

def table_rows(docname, meaning, compliance_for_document,
        explanations_for_document):
    yield (
        'STIG',
        'STIG ID',
        'IA Controls',
        'Title',
        'Rule ID',
        'Severity',
        'Compliant?',
        'Explanation/Mitigation',
        )
    for rg in meaning.selected_rule_groups():
        for r in rg.rules():
            try:
                compliant = compliance_for_document[r.version]
            except KeyError:
                compliant = '(nothing written)'
            try:
                explanation = explanations_for_document[r.version]
            except KeyError:
                explanation = ''
            yield (
                    docname,
                    r.version,
                    ', '.join(rg.ia_controls),
                    r.title,
                    r.id,
                    r.severity,
                    compliant,
                    explanation,
                    )

def values_to_csv(iterable_of_tuples):
    for row in iterable_of_tuples:
        # HACK: replace double quotes in values with single quotes, so that
        # when we use double quotes to delimit values, quotes inside the
        # values won't screw up the file format
        yield u','.join(u'"%s"' % (x.replace('"', "'")) for x in row)


def compliance2csv(checklists, compliance_aux, explanations_aux):
    """Read aux files created by LaTeX and yield CSV table of compliance.

    meaning is an XCCDFMeaning object.

    compliance_aux and explanations_aux are iterables of lines from a
    the respective files (e.g., open file objects).
    """
    log = logging.getLogger('compliance2csv')
    compliance = parse_compliance(compliance_aux)
    explanations = parse_explanations(explanations_aux)
    for docname, meaning in checklists.items():
        if docname in compliance:
            this_compliance = compliance[docname]
        else:
            log.warning('no notations of compliance found for %s',
                    docname)
            this_compliance = {}
        if docname in explanations:
            this_explanations = explanations[docname]
        else:
            log.info('no explanations of non-compliance '
                    'found for %s. (Maybe there is no '
                    'non-compliance to explain!)',
                    docname)
            this_explanations = {}
        rows = table_rows(docname, meaning, this_compliance, this_explanations)
        for x in values_to_csv(rows):
            yield x
