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
import pandas as pd

""" Documentation: https://cutadapt.readthedocs.io/en/stable/ """


class Cutadapt(BasePipeline):

    def __init__(self, data_dir: str, program_location: str, param_str: str, multiqc_path: str, output_dir: str,
                 s_or_p: str, file_ending='.fq.gz', name='CUTADAPT', dryrun=False, nthreads=None):
        super().__init__(data_dir, program_location, file_ending=file_ending, name=name, dryrun=dryrun,
                         nthreads=nthreads)
        if s_or_p not in ['s' or 'p']:
            self.u.err_p([f'Error: passed an invalid parameter for s_or_p: {s_or_p}.\n'
                          f'Please use "s" or "p" (s=single ended reads, p=paired ended reads in separate files.)'])
            return
        self.s_or_p = s_or_p
        self.multiqc_path = multiqc_path
        self.param_str = param_str
        self.output_dir = output_dir
        self.params = {'MultiQC path': self.multiqc_path, 'Param str': self.param_str, 'Single or paired': s_or_p,
                       'Output dir': output_dir}
        self.add_params_to_logfile()

    def generate_se_cmd(self, filepath):
        return f'{self.program_location} {self.param_str} -o {self._gen_fname_str(filepath)} {filepath}'

    def generate_pe_cmd(self, filepath):
        """ """
        self.u.err_p([f'Error: paired end implementation not yet implemented.'])
        return

    def generate_cmd(self, filepath):
        """ """
        if self.s_or_p == 's':
            return self.generate_se_cmd(filepath)

    def get_qc_files(self, metric: str, flag='fail'):
        """  Reads through the multi qc report and returns a list of failed (fail) or caution (warn) files. """
        multiqc_df = pd.read_csv(self.multiqc_path, sep='\t')
        if metric not in list(multiqc_df.columns):
            self.u.err_p([f'Error: Metric passed to get_qc_files ({metric}) was not in multiqc file columns:\n',
                          list(multiqc_df.columns)])
            return
        if flag not in ['pass', 'warn', 'fail']:
            self.u.err_p([f'Error: flag passed to get_qc_files ({flag}) was not an allowed parameter: \n '
                          f'[pass, warn, fail]\nTerminating, please run again.'])
            return
        files = multiqc_df['Filename'].values[multiqc_df[metric] == flag]
        # add the directory path to the data
        file_paths = [f'{self.data_dir}{f}' for f in files]
        return file_paths
