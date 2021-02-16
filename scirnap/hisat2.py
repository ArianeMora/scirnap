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
from datetime import datetime
from scirnap import BasePipeline

import os


""" 
Documentation: https://ccb.jhu.edu/software/hisat2/manual.shtml 
             : http://www.htslib.org/doc/samtools-view.html 
"""


class Hisat2(BasePipeline):

    def __init__(self, data_dir: str, program_location: str, param_str: str, output_dir: str, annotation_idx_dir: str,
                 s_or_p: str, file_ending='.fq.gz', name='HISAT2', dryrun=False, nthreads=None):
        super().__init__(data_dir, program_location, file_ending=file_ending, name=name, dryrun=dryrun,
                         nthreads=nthreads)
        if s_or_p not in ['s' or 'p']:
            self.u.err_p([f'Error: passed an invalid parameter for s_or_p: {s_or_p}.\n'
                          f'Please use "s" or "p" (s=single ended reads, p=paired ended reads in separate files.)'])
            return
        self.s_or_p = s_or_p
        self.param_str = param_str
        self.output_dir = output_dir
        self.annotation_idx_dir = annotation_idx_dir
        self.params = {'Param str': self.param_str, 'Single or paired': s_or_p, 'Output dir': output_dir,
                       'Annotation index': annotation_idx_dir}
        self.add_params_to_logfile()

    def generate_se_cmd(self, filepath):
        file_out = self._gen_fname_str(filepath)
        # Run hisat2 > pipe results to SAMTOOLS to compress to bam > sort the bam
        return f'{self.program_location} {self.param_str} --summary-file {file_out}_summary.txt ' \
               f'-x {self.annotation_idx_dir} -U {filepath} | ' \
               f'samtools view -bS | ' \
               f'samtools sort -o ' \
               f'{file_out}.sorted.bam'

    def generate_pe_cmd(self, filepath):
        """ """
        self.u.err_p([f'Error: paired end implementation not yet implemented.'])
        return

    def generate_cmd(self, filepath):
        """ """
        if self.s_or_p == 's':
            return self.generate_se_cmd(filepath)

    def summarise_results(self, output_filename: str):
        """ """
        files = os.listdir(self.output_dir)
        with open(output_filename, 'a+') as fout:
            for filename in files:
                if 'summary' in filename:
                    # Read in the file
                    with open(os.path.join(self.output_dir, filename), 'r+') as summary:
                        line_cnt = 0
                        end = 5
                        for line in summary:
                            if line_cnt == end:
                                try:
                                    line_str = filename + "\t" + line.split(' ')[0][:-1]
                                    if self.verbose:
                                        print(line_str)
                                    fout.write(line_str)
                                except:
                                    end = 14
                            line_cnt += 1