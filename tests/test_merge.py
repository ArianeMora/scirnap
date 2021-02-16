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
import pandas as pd

from scirnap import Pool


class TestMerge(unittest.TestCase):

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

    def test_merge_bams(self):
        # -g is the reverse strand
        # data_dir: str, program_location: str, file_ending='.bam', name='BAMPOOL', should_sort=True,
        #                  dryrun=False, nthreads=None
        fqc = Pool('data/hisat2/',
                   'data/merged_bams/',
                   'software/samtools/./samtools', dryrun=False, nthreads=None)
        files = fqc.get_files_in_dir()
        fqc.run_on_file(files)

    def test_merge_on_barcode(self):
        pairs = []
        found = []
        data_dir = 'data/hisat2/'
        file_name_df = pd.read_csv('data/fastq/filelist.csv')
        file_name_map = {}
        barcodes = file_name_df['Barcode'].values
        b_i = 0
        for sample_name in file_name_df['SampleName'].values:
            file_name_map[barcodes[b_i]] = sample_name
            b_i += 1
        files = os.listdir(data_dir)
        file_to_newname = {}
        for f in files:
            if 'summary' not in f:
                file_id = f.split('.')[1]
                if file_id not in found:
                    for pair in files:
                        if 'summary' not in pair:
                            pair_id = pair.split('.')[1]
                            if pair_id == file_id and f != pair:
                                pairs.append([os.path.join(data_dir, f), os.path.join(data_dir, pair)])
                                found.append(file_id)
                                file_to_newname[os.path.join(data_dir, f)] = file_name_map[file_id]
                                print(f, pair)
                                break
        fqc = Pool('data/hisat2/',
                    'software/samtools/./samtools',
                    'data/merged_bams_nodta/',
                    filename_map=file_to_newname, name='bampool', dryrun=False, nthreads=None)
        fqc.run_per_file(pairs)
