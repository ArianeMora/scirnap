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

from scirnap import BasePipeline

""" Pool bam files: http://www.htslib.org/doc/samtools-merge.html """


class Pool(BasePipeline):

    def __init__(self, data_dir: str, program_location: str, output_dir: str, file_ending='.bam', name='BAMPOOL',
                 filename_map=None, dryrun=False, nthreads=None):
        super().__init__(data_dir, program_location, output_dir=output_dir, file_ending=file_ending, name=name, dryrun=dryrun,
                         nthreads=nthreads)
        # A map from the first filename to the new filename
        self.filename_map = filename_map

    def generate_cmd(self, files_to_merge):
        """ Files to merge is a list of files to merge into bams. """
        filename = self.filename_map[files_to_merge[0]] if self.filename_map else self._get_filename(files_to_merge[0])
        return f'{self.program_location} merge {os.path.join(self.output_dir, filename)}.merged.bam {" ".join(files_to_merge)}'

