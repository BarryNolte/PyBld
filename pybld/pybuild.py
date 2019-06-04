import sys
import os
import re
import argparse

from pybld.utility import PrintColor, Fore
from pybld.jobs import Shell

from pybld.makefile_template import gccTemplate
from pybld.config import defaultMakefile
from pybld.config import theme, config

from pybld.targetobj import TargetObject, TargetStatus
from tabulate import tabulate


def ParseMakefile(makefile_path, makefileObj):
    '''Parse the makefile to find the targets'''
    def ParseTargetArgs(args):
        '''Parse out the arguments to the target if there are any'''
        arglist = l.replace('@target', '').replace('(', '') \
            .replace(')', '').replace(',', ';').replace('; ', ';') \
            .replace("'", '').replace('"', '')

        argdict = {}
        if arglist:
            argdict = dict(item.split("=") for item in arglist.split(";"))

        desc = argdict.get('desc', '')
        pre = argdict.get('preFunc', None)
        post = argdict.get('postFunc', None)

        return desc, pre, post

    Targets = {}  # type: dict[str, TargetObject]
    if os.path.isfile(makefile_path):
        with open(makefile_path, 'r') as f:
            makefile_str = f.read()

        makefile_lines = makefile_str.splitlines()
        for i, l in enumerate(makefile_lines):
            if l.startswith('@target'):
                target_func = re.findall(r'def\s+(\w+)\s*\(', makefile_lines[i + 1])
                target_func = target_func[0]
                target_args = re.findall(r'def\s+\w+\s*\((.*)\)', makefile_lines[i + 1])
                target_args = target_args[0]

                # desc, pre, post = ParseTargetArgs(l)

                Targets[target_func] = TargetObject(target_func, target_args, makefileObj)

        # Detect Dependencies
        for key in Targets.keys():
            tarItem = Targets[key]
            for i, item in enumerate(tarItem.Dependencies):
                if callable(item):
                    depTarget_str = tarItem.args_str[i]
                    depTarget = Targets[depTarget_str]
                    tarItem.Dependencies[i] = depTarget

    return Targets


def CreateMakefile(filename):
    retV = input(f'Makefile does not exist, do you want to create "{filename}"? (y/n): ')
    if retV.lower() == 'y':
        tempText = str(gccTemplate)
        with open(filename, 'w') as f:
            f.write(tempText)
    sys.exit()


def PrintTargets(targets):
    table = []
    for target in targets:
        row = []
        dep = ''
        for depTarget in targets[target].Dependencies:
            if type(depTarget) is TargetObject:
                dep += ' -> ' + depTarget.Name
            elif type(depTarget) is list:
                for fn in depTarget:
                    dep += fn + ' '
        row.append(target)
        row.append(dep)
        table.append(row)

    Y = Fore.YELLOW
    N = Fore.RESET
    print(tabulate(table, headers=[f'{Y}Avalible Targets{N}', f'{Y}Depends On{N}'], tablefmt="psql"))
    sys.exit()


class CapitalisedHelpFormatter(argparse.HelpFormatter):
    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = f'{Fore.YELLOW}usage: {Fore.RESET}'
        return super(CapitalisedHelpFormatter, self).add_usage(usage, actions, groups, prefix)


def DoMain():

    # Parse Command Line
    parser = argparse.ArgumentParser(description=f'{Fore.CYAN}PyBld is a simple make system implemented in python.{Fore.RESET}', formatter_class=CapitalisedHelpFormatter)
    parser._positionals.title = f'{Fore.YELLOW}positional arguments:{Fore.RESET}'
    parser._optionals.title = f'{Fore.YELLOW}optional arguments:{Fore.RESET}'
    parser.add_argument('-l', help=f'List available targets in make file and exit.', action='store_true')
    parser.add_argument('-f', metavar='Makefile', help=f'Explicit path to makefile, default = "{defaultMakefile}".', default=defaultMakefile)
    # parser.add_argument('-j', metavar='Jobs', type=int, help='Number of jobs used in the make process.')
    parser.add_argument('-D', metavar='Define', action='append', help='Define variables for use in the makefile. format="-Dvar=value"')
    parser.add_argument('target', metavar='Target', nargs='*', help='Make target(s) in the makefile.', default=['all'])

    args = parser.parse_args()

    if args.D:
        try:
            for define in args.D:
                ds = define.split('=')
                config['defines'][ds[0]] = ds[1]
        except:
            print('Error in -D arguments.')
            exit(1)

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

    # Call this function before any make actions take place,
    # must be called after the make file is loaded
    if config['PreMakeFunction'] is not None:
        config['PreMakeFunction']()

    # =======================================================================
    # If we have targets, execute them

    for targ in args.target:
        selected_Target = Targets.get(targ)  # type: TargetObject

        if selected_Target and selected_Target.Status == TargetStatus.NOTRUN:
            selected_Target.run()
        else:
            PrintColor(f'Error: target function "{selected_Target.Name}" does not exist!', theme['error'].Foreground(), theme['error'].Background())
            sys.exit(1)

    # =======================================================================

    if config['PostMakeFunction'] is not None:
        config['PostMakeFunction']()

    return 0


if __name__ == '__main__':
    DoMain()
