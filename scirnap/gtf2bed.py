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

# https://gffutils.readthedocs.io/en/latest/index.html
# https://gffutils.readthedocs.io/en/latest/gtf2bed.html?highlight=gtf2bed
# version: GFFUtils-0.11.0


class GTF2Bed(BasePipeline):

    def __init__(self, data_dir: str, program_location: str, output_dir: str,
                 file_ending='.gtf', name='GTF2BED',  dryrun=False, nthreads=None):
        super().__init__(data_dir, program_location, file_ending=file_ending, name=name, dryrun=dryrun,
                         nthreads=nthreads)
        self.output_dir = output_dir
        self.params = {}
        self.add_params_to_logfile()

    def generate_cmd(self, file_path):
        return f'{self.program_location} {file_path} > {self._gen_fname_str(file_path)[:-4]}.bed'
