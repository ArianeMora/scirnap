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
import os
import subprocess
import ntpath
from multiprocessing.dummy import Pool as ThreadPool

from sciutil import SciUtil, SciException


class PipelineException(SciException):
    def __init__(self, message=''):
        Exception.__init__(self, message)


class BasePipeline:

    def __init__(self, data_dir: str, program_location: str, output_dir=None, logfile=None, verbose=True,
                 file_ending=None, name=None, dryrun=False, nthreads=None):
        self.data_dir = data_dir
        self.output_dir = data_dir if output_dir is None else output_dir
        self.logfile_location = logfile or f'{name}_logfile-{datetime.now().strftime("%d%m%Y-%H%M%S")}.txt'
        self.logfile = open(self.logfile_location, 'a+')
        self.u = SciUtil()
        self.verbose = verbose
        self.dryrun, self.nthreads = dryrun, nthreads
        self.program_location = program_location
        # Check it is a location
        if not os.path.exists(self.data_dir):
            self.u.err_p([f'Error: checked for data location & directory does not exist.\n Please check '
                          f'{data_dir} and re-run.\nProgram terminating.'])
        # Write the version of the program to the logfile
        self.program_version = subprocess.Popen(f'{program_location} --version', shell=True,
                                                stdout=subprocess.PIPE).stdout.read()  # Call subprocess
        if not self.program_version:
            self.u.warn_p([f'Warning: the version of your program could not be determined i.e.'
                           f' --version did not return. Continuing to run.'])
        else:
            self.logfile.write(f'# program version: {self.program_version}')
        self.file_ending, self.name = file_ending, name
        self.params = {}

    def print_params(self):
        for p, v in self.params.items():
            self.u.dp([f'Param: {p}\nValue: {v}'])

    def print_logfile_dir(self):
        self.u.dp([f'FYI: your logfile is located here:\n{self.logfile_location}'])

    def print_program_version(self):
        if not self.program_version:
            self.u.warn_p([f'Warning: the version of your program could not be determined i.e.'
                           f' --version did not return.'])
        else:
            self.u.dp([f'Program version:\n {self.program_version}'])

    def add_params_to_logfile(self):
        for p, v in self.params.items():
            self.logfile.write(f'# {p}: {v}\n')

    def exec_cmd(self, cmd):
        if self.logfile:
            self.logfile.write(f'{cmd}\t {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\n')
        if not self.dryrun:
            pid = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
            if self.verbose:
                print(pid)
        else:
            self.u.dp([f'Normally would be executing cmd:\n{cmd}'])

    def generate_cmd(self, filepath):
        return 'echo YouNeedToSelectAnOverridingClass'

    def get_files_in_dir(self) -> list:
        files = os.listdir(self.data_dir)
        file_paths = []
        for filename in files:
            if self.file_ending in filename:
                filepath = os.path.join(self.data_dir, filename)
                file_paths.append(filepath)

        return file_paths

    def run_on_files(self, file_paths):
        """ Since we run all files at once, we overwrite this method. """
        cmd = self.generate_cmd(file_paths)

        if self.verbose:
            self.u.dp([f'Running {self.name} on files in: {self.data_dir}'])

        self.exec_cmd(cmd)

        # Close the logfile
        self.logfile.close()

    def run_on_file(self, file_path):
        cmd = self.generate_cmd(file_path)

        if self.verbose:
            self.u.dp([f'Running {self.name} on files in: {self.data_dir}'])

        self.exec_cmd(cmd)
        # Close the logfile
        self.logfile.close()

    def _gen_and_exec_cmd(self, file_path):
        cmd = self.generate_cmd(file_path)
        if self.verbose:
            self.u.dp([f'Running {self.name} on file: {file_path}'])

        self.exec_cmd(cmd)

    def run_per_file(self, file_paths):
        if self.nthreads:
            # https://stackoverflow.com/questions/2846653/how-can-i-use-threading-in-python
            if self.verbose:
                self.u.dp(['Running multithreaded, number of threads: ', self.nthreads])
            # Make sure the number of threads doesn't exceed number of files (that would be dumb) but hey you never
            # know the inputs people choose...
            self.nthreads = self.nthreads if self.nthreads < len(file_paths) else len(file_paths)
            pool = ThreadPool(self.nthreads)
            results = pool.map(self._gen_and_exec_cmd, file_paths)
            if self.verbose:
                self.u.dp(["Outputs from executing cmds: ", results])
        else:
            for f in file_paths:
                cmd = self.generate_cmd(f)
                if self.verbose:
                    self.u.dp([f'Running {self.name} on file: {f}'])

                self.exec_cmd(cmd)

        # Close the logfile
        self.logfile.close()

    @staticmethod
    def _get_filename(file_path):
        head, tail = ntpath.split(file_path)
        return tail or ntpath.basename(head)

    def _gen_fname_str(self, file_path):
        return f'{os.path.join(self.output_dir, self.name)}-' \
               f'{datetime.now().strftime("%d%m%Y")}_{self._get_filename(file_path)}'