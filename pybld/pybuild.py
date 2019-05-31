import sys
import os
import re
import argparse
from enum import Enum

from pybld.utility import PrintColor, Indenter
from pybld.jobs import Shell

from pybld.makefile_template import gccTemplate
from pybld.config import defaultMakefile
from pybld.config import theme, crossMark, checkBox, config


class TargetStatus(Enum):
    NOTRUN = 1
    RUNSUCCESS = 2
    RUNFAIL = 3


class TargetObject(object):
    '''Defines a target, and what it depends on '''
    def __init__(self, func, args, MakefileObj):
        self.Name = func
        self.func = getattr(MakefileObj, func)
        # Do we need these around??
        args_str = [item.strip() for item in args.split(',')]
        args_var = [getattr(MakefileObj, item)
                    for item in args_str if item != '']
        self.args_str = args_str
        self.args_var = args_var
        ####
        self.MakefileObj = MakefileObj
        self.Dependencies = args_var
        self.Status = TargetStatus.NOTRUN
        self.Time = None

    def check_dependencies(self):
        indent = Indenter()
        idstr = '-' * indent.GetIndent()
        PrintColor(f'{idstr} Dependency checking of Target "{self.Name}"', theme['info'].Foreground(), theme['info'].Background())

        # leaf node, this has no dependencies
        if len(self.Dependencies) == 0:
            return True

        for i, item in enumerate(self.Dependencies):
            if type(item) is list:
                # assumed to be list of file names (paths)
                for subitem in item:
                    if not os.path.isfile(subitem):
                        PrintColor(f'{crossMark}Dependency Error @ Target "{self.Name}": file "{subitem}" does not exsist!', theme['error'].Foreground(), theme['error'].Background())
                        return False
            elif type(item) is str:
                if not os.path.isfile(item):
                    PrintColor(f'{crossMark}Dependency Error @ Target "{self.Name}": file "{item}" does not exsist!', theme['error'].Foreground(), theme['error'].Background())
                    return False
            elif type(item) is TargetObject:  # another target
                if not item.run():
                    PrintColor(f'{crossMark}Dependency Error @ Target "{self.Name}": Target "{item.Name}" failed', theme['error'].Foreground(), theme['error'].Background())
                    return False

        return True

    def run(self):
        if self.check_dependencies():
            print()
            PrintColor(f'Executing Target "{self.Name}"', theme['target'].Foreground(), theme['target'].Background())
            try:
                self.Status = TargetStatus.RUNFAIL

                retV, time = self.func(*self.args_var)
                self.Time = time

                if not retV:
                    PrintColor(f'{crossMark}Target "{self.Name}" failed!', theme['error'].Foreground(), theme['error'].Background())
                else:
                    self.Status = TargetStatus.RUNSUCCESS
                    PrintColor(f'{checkBox}Target "{self.Name}" succeded! ({time:.4f} sec)', theme['success'].Foreground(), theme['success'].Background())

                return retV
            except:
                PrintColor(f'Internal error in the target function "{self.Name}"', theme['error'].Foreground(), theme['error'].Background())
                raise

        else:
            return False


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
    PrintColor('Avalible Targets', theme['target'].Foreground(), theme['target'].Background())
    for target in targets:
        t = targets[target]
        PrintColor(f'  {t.Name}', theme['plain'].Foreground(), theme['plain'].Background())
    sys.exit()


def DoMain():

    # Parse Command Line
    parser = argparse.ArgumentParser(description='PyBld is a simple make system implemented in python.', allow_abbrev=True)
    parser.add_argument('-l', help=f'List available targets in make file.', action='store_true')
    parser.add_argument('-f', metavar='Makefile', help=f'Explicit path to makefile, default = "{defaultMakefile}".', default=defaultMakefile)
    parser.add_argument('-j', metavar='Jobs', type=int, help='Number of jobs used in the make process.')
    parser.add_argument('target', metavar='Target', nargs='*', help='Make target in the makefile.', default=['all'])

    args = parser.parse_args()

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
    # Tests
    DoMain()
