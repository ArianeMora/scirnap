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

import argparse
import sys

from sciutil import SciUtil

from scirnap import __version__
from scirnap import Hisat2, FeatureCounts, FastQC, StringTie, Pool, Sort, Cutadapt


def print_help():
    lines = ['-h Print help information.']
    print('\n'.join(lines))


def run(args):
    if args.t == 'cutadapt':
        t = Cutadapt(args.d, args.c, args.p, args.mp, args.o, args.sp, args.f, args.n, args.dr, args.nt)
        files = t.get_files_in_dir()
        t.run_per_file(files)
    elif args.t == 'fastqc':
        t = FastQC(args.d, args.c, args.o, args.f, args.n, args.dr, args.nt)
        files = t.get_files_in_dir()
        t.run_per_file(files)
    elif args.t == 'featurecounts':
        t = FeatureCounts(args.d, args.c, args.p, args.o, args.gtf, args.f, args.n, args.dr, args.nt)
        files = t.get_files_in_dir()
        t.run_on_files(files)
    elif args.t == 'stringtie':
        t = StringTie(args.d, args.c, args.p, args.o, args.gtf, args.f, args.n, args.dr, args.nt)
        files = t.get_files_in_dir()
        t.run_per_file(files)
    elif args.t == 'hisat2':
        t = Hisat2(args.d, args.c, args.p, args.o, args.adir, args.sp, args.f, args.n, args.dr, args.nt)
        files = t.get_files_in_dir()
        t.run_per_file(files)
    elif args.t == 'pool':
        t = Pool(args.d, args.c, args.o, args.f, args.n, args.fm, args.dr, args.nt)
        files = t.get_files_in_dir()
        t.run_per_file(files)
    elif args.t == 'sort':
        t = Sort(args.d, args.c, args.o, args.f, args.n, args.dr, args.nt)
        files = t.get_files_in_dir()
        t.run_per_file(files)
    else:
        print("Command not yet implemented. Please contact us if you wish for that to be implemented.")


def gen_parser():
    parser = argparse.ArgumentParser(description='scie2g')
    tools = ['cutadapt', 'fastqc', 'featurecounts', 'stringtie', 'hisat2', 'sort', 'pool']
    parser.add_argument('--t', type=str, help=f'Tool name (one of: {", ".join(tools)})')

    parser.add_argument('--d', type=str, help='Directory with data.')
    parser.add_argument('--o', type=str, help='Output directory.')
    parser.add_argument('--mp', type=str, help='Cutadapt: Path to multiqc file.')
    parser.add_argument('--p', type=str, default="", help='Parameter string (specific to each program)')

    parser.add_argument('--c', type=str, help='Program command or location.')
    parser.add_argument('--f', type=str, default=None, help='File ending (e.g. .fq.gz) Optional.')
    parser.add_argument('--dr', type=bool, default=False, help='Dry run, defaults to false.')
    parser.add_argument('--nt', type=int, default=1, help='Number of threads (default is 1)')
    parser.add_argument('--n', type=str, default="", help='Name to append to files.')

    # Cutadapt specific
    parser.add_argument('--mp', type=str, help='Cutadapt: Path to multiqc file.')
    parser.add_argument('--sp', type=str, help='Cutadapt and Hisat2: s or p (single or paired).')

    # FeatureCounts specific
    parser.add_argument('--gtf', type=str, help='FeatureCounts and Stringtie: path to the GTF (genome annotation) file.')

    # Stringtie specific
    parser.add_argument('--ctab', type=str, help='Stringtie: Path to place the CTAB files.')

    # hisat2 specific
    parser.add_argument('--adir', type=str, help='Hisat2: Path to directory with the indexs for Hisat2.')

    # Pooling specific
    # parser.add_argument('--fm', type=str, help='Pool: Dictionary with pooled filenames (in json format).')

    return parser


def main(args=None):
    parser = gen_parser()
    u = SciUtil()
    if args:
        sys.argv = args
    if len(sys.argv) == 1:
        print_help()
        sys.exit(0)
    elif sys.argv[1] in {'-v', '--v', '-version', '--version'}:
        print(f'scirnap v{__version__}')
        sys.exit(0)
    else:
        print(f'scirnap v{__version__}')
        args = parser.parse_args(args)
        # Validate the input arguments.
        tools = ['cutadapt', 'fastqc', 'featurecounts', 'stringtie', 'hisat2', 'sort', 'pool']
        if not args.t in tools:
            u.err_p([f'The command you attempted to run is not in our list, you sent: {args.t},'
                     f'\nPlease choose from one of: {", ".join(tools)}'])
            sys.exit(1)
        # Otherwise we have need successful so we can run the program
        u.dp(['Running sci-rnap with tool: ', args.t])
        # RUN!
        run(args)
    # Done - no errors.
    sys.exit(0)


if __name__ == "__main__":
    main()
    # ----------- Example below -----------------------
    # root_dir = '../'
    # main(["--dmr", root_dir + "tests/data/methylSig_prom.csv", "--dmc", root_dir + "tests/data/methylKit_DMC.csv"])