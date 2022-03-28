from VariantValidator import Validator
from unittest import TestCase


class TestWarnings(TestCase):

    @classmethod
    def setup_class(cls):
        cls.vv = Validator()

    def test_t_in_rna_string(self):
        variant = 'NM_007075.3:r.235_236insGCCCACCCACCTGCCAG'
        results = self.vv.validate(variant, 'GRCh37', 'all').format_as_dict(test=True)
        print(results)
        assert 'The IUPAC RNA alphabet dictates that RNA variants must use the character u in place of t' in \
               results['validation_warning_1']['validation_warnings']

    def test_issue_169(self):
        variant = 'NC_000017.10(NM_007294.3):c.4421-63A>G'
        results = self.vv.validate(variant, 'GRCh37', 'all').format_as_dict(test=True)
        print(results)
        assert 'The entered coordinates do not agree with the intron/exon boundaries for the selected transcript' in \
               results['validation_warning_1']['validation_warnings'][0]

    def test_issue_176(self):
        variant = 'NC_000023.10(NM_004006.2):c.8810A>G'
        results = self.vv.validate(variant, 'GRCh37', 'all').format_as_dict(test=True)
        print(results)
        assert 'NC_000023.10:g.31496350T>C: Variant reference (T) does not agree with reference sequence (C)' in \
               results['validation_warning_1']['validation_warnings'][0]

    def test_issue_180a(self):
        variant = 'NC_000017.10:g.41232400_41236235del383'
        results = self.vv.validate(variant, 'hg19', 'all').format_as_dict(test=True)
        print(results)
        assert 'Length implied by coordinates must equal sequence deletion length' in \
               results['validation_warning_1']['validation_warnings'][0]

    def test_issue_180b(self):
        variant = 'NC_000017.10(NM_007300.3):c.4186-1642_4358-983del10'
        results = self.vv.validate(variant, 'GRCh37', 'all').format_as_dict(test=True)
        print(results)
        assert 'Length implied by coordinates must equal sequence deletion length' in \
               results['validation_warning_1']['validation_warnings'][0]

    def test_issue_180c(self):
        variant = 'NC_000017.10(NM_000088.3):c.589-1del2'
        results = self.vv.validate(variant, 'GRCh37', 'all').format_as_dict(test=True)
        print(results)
        assert 'Length implied by coordinates must equal sequence deletion length' in \
               results['validation_warning_1']['validation_warnings'][0]

    def test_issue_195a(self):
        variant = 'NM_000088.3(COL1A1):c.590delG'
        results = self.vv.validate(variant, 'GRCh37', 'all').format_as_dict(test=True)
        print(results)
        assert 'Removing redundant gene symbol COL1A1 from variant description' in \
               results['NM_000088.3:c.590del']['validation_warnings'][0]
        assert 'Removing redundant reference bases from variant description' in \
               results['NM_000088.3:c.590del']['validation_warnings'][1]

    def test_issue_216a(self):
        variant = 'NM_006941.3:c.850_877dup27'
        results = self.vv.validate(variant, 'hg19', 'all').format_as_dict(test=True)
        print(results)
        assert 'Length implied by coordinates must equal sequence duplication length' in \
               results['validation_warning_1']['validation_warnings'][0]

    def test_issue_216b(self):
        variant = 'NM_006941.3:c.850_877dup28'
        results = self.vv.validate(variant, 'hg19', 'all').format_as_dict(test=True)
        print(results)
        assert 'Trailing digits are not permitted in HGVS variant descriptions' in \
               results['NM_006941.3:c.850_877dup']['validation_warnings'][0]

    def test_issue_239(self):
        variant = 'NM_006941.3:c.1047dupT'
        results = self.vv.validate(variant, 'hg19', 'all').format_as_dict(test=True)
        print(results)
        assert 'Removing redundant reference bases from variant description' in \
               results['NM_006941.3:c.1047dup']['validation_warnings'][0]

    def test_issue_338(self):
        # Also issue 357
        variant = 'NM_000088.3:C.589G>T'
        results = self.vv.validate(variant, 'GRCh37', 'all', liftover_level='primary').format_as_dict(test=True)
        print(results)
        assert 'characters being in the wrong case' in \
               results['NM_000088.3:c.589G>T']['validation_warnings'][0]

        variant = 'NM_000088.3:C.589G>T'
        results = self.vv.validate(variant, 'GRCh37', 'all', liftover_level='primary').format_as_dict(test=True)
        print(results)
        assert 'characters being in the wrong case' in \
               results['NM_000088.3:c.589G>T']['validation_warnings'][0]

        variant = 'nm_000088.3:c.589G>T'
        results = self.vv.validate(variant, 'GRCh37', 'all', liftover_level='primary').format_as_dict(test=True)
        print(results)
        assert 'characters being in the wrong case' in \
               results['NM_000088.3:c.589G>T']['validation_warnings'][0]

        variant = 'lrg_1t1:c.589G>T'
        results = self.vv.validate(variant, 'GRCh37', 'all', liftover_level='primary').format_as_dict(test=True)
        print(results)
        assert 'characters being in the wrong case' in \
               results['NM_000088.3:c.589G>T']['validation_warnings'][0]

        variant = 'lrg_1T1:c.589G>T'
        results = self.vv.validate(variant, 'GRCh37', 'all', liftover_level='primary').format_as_dict(test=True)
        print(results)
        assert 'characters being in the wrong case' in \
               results['NM_000088.3:c.589G>T']['validation_warnings'][0]

        variant = 'LRG_1T1:c.589G>T'
        results = self.vv.validate(variant, 'GRCh37', 'all', liftover_level='primary').format_as_dict(test=True)
        print(results)
        assert 'characters being in the wrong case' in \
               results['NM_000088.3:c.589G>T']['validation_warnings'][0]

        variant = 'chr17:50198002C>A'
        results = self.vv.validate(variant, 'GRCh38', 'all', liftover_level='primary').format_as_dict(test=True)
        print(results)
        assert 'because no reference sequence ID has been provided' in \
               results['NM_000088.3:c.589G>T']['validation_warnings'][0]

        # Issue 359
        variant = 'NM_001371623.1:c.483ins'
        results = self.vv.validate(variant, 'GRCh37', 'all', liftover_level='primary').format_as_dict(test=True)
        print(results)
        assert 'The inserted sequence must be provided for insertions or deletion-insertions' in \
               results['validation_warning_1']['validation_warnings'][0]
        assert 'An insertion must be provided with the two positions between which the insertion has taken place' in \
               results['validation_warning_1']['validation_warnings'][1]

        variant = 'NM_001371623.1:c.483ins(10)'
        results = self.vv.validate(variant, 'GRCh37', 'all', liftover_level='primary').format_as_dict(test=True)
        print(results)
        assert 'The length of the variant is not formatted following the HGVS guidelines. Please rewrite (10) ' \
               'to N[10]' in \
               results['validation_warning_1']['validation_warnings'][0]
        assert 'An insertion must be provided with the two positions between which the insertion has taken place' in \
               results['validation_warning_1']['validation_warnings'][1]

        variant = 'NM_001371623.1:c.483ins10'
        results = self.vv.validate(variant, 'GRCh37', 'all', liftover_level='primary').format_as_dict(test=True)
        print(results)
        assert 'The length of the variant is not formatted following the HGVS guidelines. Please rewrite 10 ' \
               'to N[10]' in \
               results['validation_warning_1']['validation_warnings'][0]
        assert 'An insertion must be provided with the two positions between which the insertion has taken place' in \
               results['validation_warning_1']['validation_warnings'][1]

        variant = 'NM_001371623.1:c.483insA[10]'
        results = self.vv.validate(variant, 'GRCh37', 'all', liftover_level='primary').format_as_dict(test=True)
        print(results)
        assert 'NM_001371623.1:c.483insA[10] is better written as NM_001371623.1:c.483insAAAAAAAAAA' in \
               results['validation_warning_1']['validation_warnings'][0]
        assert 'An insertion must be provided with the two positions between which the insertion has taken place' in \
               results['validation_warning_1']['validation_warnings'][1]
        assert 'insertion length must be 1' in \
               results['validation_warning_1']['validation_warnings'][2]

        variant = 'NM_001371623.1:c.483_484insA[10]'
        results = self.vv.validate(variant, 'GRCh37', 'all', liftover_level='primary').format_as_dict(test=True)
        print(results)
        assert 'NM_001371623.1:c.483_484insA[10] is better written as NM_001371623.1:c.483_484insAAAAAAAAAA' in \
               results['NM_001371623.1:c.483_484insAAAAAAAAAA']['validation_warnings'][0]

        variant = 'NM_001371623.1:c.483_484ins[A[10];T]'
        results = self.vv.validate(variant, 'GRCh37', 'all', liftover_level='primary').format_as_dict(test=True)
        print(results)
        assert 'NM_001371623.1:c.483_484ins[A[10];T] is better written as NM_001371623.1:c.483_484insAAAAAAAAAAT' in \
               results['NM_001371623.1:c.483_484insAAAAAAAAAAT']['validation_warnings'][0]


# <LICENSE>
# Copyright (C) 2016-2022 VariantValidator Contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# </LICENSE>
