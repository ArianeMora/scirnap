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

from scirnap import Hisat2, Cutadapt


class TestHisat2(unittest.TestCase):

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

    def test_hisat2(self):

        # -g is the reverse strand
        # data_dir: str, program_location: str, param_str: str, output_dir: str, annotation_idx_dir: str,
        #                  s_or_p: str
        hs = Hisat2('data/cutadapt/',
                      'software/hisat2-2.2.1/./hisat2',
                      '-k 5 -p 10 -q --max-seeds 5 ',
                      'data/hisat2/',
                      'software/hisat2_indexs/grch38/genome',
                      's', name='hisat2',
                      dryrun=False, nthreads=None)
        cu = Cutadapt('data/fastq/',
                      'cutadapt',
                      '-g "CCCTT;anywhere" ',
                      'data/fastqc/multiqc_data/multiqc_fastqc.txt',
                      'data/cutdadapt/', 's',
                      dryrun=False, nthreads=5)
        files = cu.get_qc_files('overrepresented_sequences', 'pass')  # files = hs.get_files_in_dir()
        print(files)
        hs.run_per_file(files)

