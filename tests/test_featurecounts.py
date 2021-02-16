###############################################################################
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program. If not, see <http://www.gnu.org/licenses/>.     #
#                                                                             #
###############################################################################

import os
import shutil
import tempfile
import unittest

from scirnap import FeatureCounts


class TestFeatureCounts(unittest.TestCase):

    def setUp(self):
        # Flag to set data to be local so we don't have to download them repeatedly. ToDo: Remove when publishing.
        self.local = True

        if self.local:
            THIS_DIR = os.path.dirname(os.path.abspath(__file__))
            self.tmp_dir = os.path.join(THIS_DIR, 'data/tmp/')
            if os.path.exists(self.tmp_dir):
                shutil.rmtree(self.tmp_dir)
            os.mkdir(self.tmp_dir)
        else:
            self.tmp_dir = tempfile.mkdtemp(prefix='EXAMPLE_PROJECT_tmp_')

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def test_featurecounts(self):
        # data_dir: str, program_location: str,  param_str: str, output_dir: str, gtf_filepath: str,
        #                  file_ending='.bam', name='FEATURECOUNTS'
        cu = FeatureCounts('data/bams/',
                      'software/subread-2.0.1-MacOS-x86_64/bin/./featureCounts',
                      '-F GTF -t exon -T 10 -g gene_id ',
                      'data/featurecounts/',
                      'software/ensembl/Homo_sapiens.GRCh38.100.gtf',
                      dryrun=False)
        files = cu.get_files_in_dir()
        # Run dryrun
        cu.run_on_files(files)
