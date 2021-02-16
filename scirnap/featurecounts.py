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

from scirnap import BasePipeline

""" Documentation at: https://pubmed.ncbi.nlm.nih.gov/24227677/ """

class FeatureCounts(BasePipeline):

    def __init__(self, data_dir: str, program_location: str, param_str: str, output_dir: str, gtf_filepath: str,
                 file_ending='.bam', name='FEATURECOUNTS',  dryrun=False, nthreads=None):
        super().__init__(data_dir, program_location, file_ending=file_ending, name=name, dryrun=dryrun,
                         nthreads=nthreads)
        self.gtf_filepath = gtf_filepath
        self.output_dir = output_dir
        self.param_str = param_str  # e.g. '-F GTF -t exon -T 10 -s 2 -g gene_id --primary -a '
        self.params = {'GTF path': self.gtf_filepath, 'Param str': self.param_str}
        self.add_params_to_logfile()

    def generate_cmd(self, file_paths):
        return f'{self.program_location} {self.param_str} -a {self.gtf_filepath} -o {self._gen_fname_str(file_paths[0])}.txt' \
               f' {" ".join(file_paths)}'
