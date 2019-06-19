"""Mail PyBld code file."""
import argparse
import os
import re
import sys
from textwrap import fill, wrap

from pybld.configutil import A, F, B, config, crossMark, defaultMakefile
from pybld.jobs import Shell
from pybld.makefile_template import makeFileTemplate
from pybld.targetobj import TargetObject, TargetStatus
from pybld.decorators import descriptions
from tabulate import tabulate

# TODO: Need to 'classify' these to hide functions


def ParseMakefile(makefile_path, makefileObj):
    """Parse the makefile to find the targets."""
    Targets = {}  # type: dict[str, TargetObject]
    if os.path.isfile(makefile_path):
        with open(makefile_path, 'r') as f:
            makefile_str = f.read()

        makefile_lines = makefile_str.splitlines()
        for i, l in enumerate(makefile_lines):
            if l.startswith('@buildTarget'):
                target_func = re.findall(r'def\s+(\w+)\s*\(', makefile_lines[i + 1])
                target_func = target_func[0]
                target_args = re.findall(r'def\s+\w+\s*\((.*)\)', makefile_lines[i + 1])
                target_args = target_args[0]

                # desc, pre, post = ParseTargetArgs(l)

                Targets[target_func] = TargetObject(target_func, target_args, makefileObj)

        # Detect Dependencies
        for _unused, value in Targets.items():
            for i, item in enumerate(value.Dependencies):
                if callable(item):
                    depTarget_str = value.args_str[i]
                    depTarget = Targets[depTarget_str]
                    value.Dependencies[i] = depTarget

    return Targets


def CreateMakefile(filename):
    """Create a makefile from a template."""
    retV = input(f'Makefile does not exist, do you want to create "{filename}"? (y/n): ')
    if retV.lower() == 'y':
        tempText = str(makeFileTemplate)
        with open(filename, 'w') as f:
            f.write(tempText)
    sys.exit()


def PrintTargets(targets):
    """Print out all targets and their dependencies."""
    table = []
    for target in targets:
        row = []
        dep = ''
        for depTarget in targets[target].Dependencies:
            if isinstance(depTarget, TargetObject):
                dep += ' -> ' + depTarget.Name
            elif isinstance(depTarget, list):
                for fn in depTarget:
                    dep += fn.Source + ' '
        desc = descriptions.get(target, '')
        desc = '' if desc is None else desc
        
        row.append(target)
        row.append(fill(dep, 36))
        row.append(fill(desc, 36))
        
        table.append(row)

    Y = F.Yellow
    N = A.Reset + F.Reset + B.Reset
    print(tabulate(table, headers=[f'{Y}Targets{N}', f'{Y}Depends On{N}', f'{Y}Description{N}'], tablefmt="psql"))
    sys.exit()


class CapitalisedHelpFormatter(argparse.HelpFormatter):
    """Help formatter class."""

    def add_usage(self, usage, actions, groups, prefix=None):
        """Is called when help needs to print usage."""
        if prefix is None:
            prefix = f'{F.Yellow}usage: {F.Reset}'
        return super(CapitalisedHelpFormatter, self).add_usage(usage, actions, groups, prefix)


def DoMain():
    """Program Entry, this is where it all starts."""
    # Parse Command Line
    parser = argparse.ArgumentParser(description=f'{F.Cyan}PyBld is a simple make system implemented in python.{A.Reset}', formatter_class=CapitalisedHelpFormatter)
    parser._positionals.title = f'{F.Yellow}positional arguments{F.Reset}'
    parser._optionals.title = f'{F.Yellow}optional arguments{F.Reset}'
    parser.add_argument('-l', help=f'List available targets in make file and exit.', action='store_true')
    parser.add_argument('-f', metavar='Makefile', help=f'Explicit path to makefile, default = "{defaultMakefile}".', default=defaultMakefile)
    parser.add_argument('-j', metavar='Jobs', type=int, help='Number of jobs used in the make process.', default=4)
    parser.add_argument('-D', metavar='Define', action='append', help='Define variables for use in the makefile. format="-Dvar=value"')
    parser.add_argument('target', metavar='Target', nargs='*', help='Make target(s) in the makefile.')   

    args = parser.parse_args()

    # Parse out any defined 'defines'
    if args.D:
        try:
            for define in args.D:
                ds = define.split('=')
                config['defines'][ds[0]] = ds[1]
        except(BaseException):
            print('Error in -D arguments.')
            exit(1)

    # How many concurrent jobs should we run
    config['jobs'] = args.j

    # Does the makefile exist?
    if not os.path.isfile(args.f):
        CreateMakefile(args.f)

    # import the makefile so we can use it
    import imp
    makefileObj = imp.load_source('makefileObj', args.f)
    Shell('rm -f *.pyc')

    # Get list of possible targets
    Targets = ParseMakefile(args.f, makefileObj)

    # Print targets if requested, then exit
    if args.l:
        PrintTargets(Targets)
        exit()

    # Call this function before any make actions take place,
    # must be called after the make file is loaded
    if config['PreMakeFunction'] is not None:
        config['PreMakeFunction']()

    # =======================================================================
    # If we have targets, execute them
    toRunTargets = None
    if not args.target:
        toRunTargets = config['defaultTargets']
    else:
        toRunTargets = args.target

    for targ in toRunTargets:
        selected_Target = Targets.get(targ)  # type: TargetObject

        if selected_Target and selected_Target.Status == TargetStatus.NOTRUN:
            selected_Target.run()
        else:
            print(f'{crossMark}  {F.Red}Error{F.Reset}: Target function {A.Bright}"{targ}"{A.Reset} does not exist!')
            sys.exit(1)

    # =======================================================================

    if config['PostMakeFunction'] is not None:
        config['PostMakeFunction']()
        
    return 0


if __name__ == '__main__':
    DoMain()
