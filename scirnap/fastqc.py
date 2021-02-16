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

""" https://dnacore.missouri.edu/PDF/FastQC_Manual.pdf """


class FastQC(BasePipeline):

    def __init__(self, data_dir: str, program_location: str, output_dir: str, file_ending='fq', name='FASTQC',
                 dryrun=False, nthreads=None):
        super().__init__(data_dir, program_location, output_dir=output_dir, file_ending=file_ending, name=name,
                         dryrun=dryrun, nthreads=nthreads)

    def generate_cmd(self, filepath):
        return f'{self.program_location} -o {self.output_dir} {filepath}'
