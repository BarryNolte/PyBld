import traceback
import sys
import os
import re
import argparse

from pybld.utility import PrintColor, Indenter
from pybld.make import Shell

from pybld.makefile_template import gccTemplate
from pybld.config import defaultMakefile
from pybld.config import theme, crossMark, checkBox

# TODO: Should be in a class
Debug = True


class TargetObject(object):
    def __init__(self, func, args, MakefileObj):
        self.Name = func
        self.func = getattr(MakefileObj, func)
        args_str = [item.strip() for item in args.split(',')]
        args_var = [getattr(MakefileObj, item)
                    for item in args_str if item != '']
        self.args_str = args_str
        self.args_var = args_var
        self.MakefileObj = MakefileObj
        self.Dependencies = args_var

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
                if len(self.args_var) == 0:
                    retV = self.func()
                else:
                    retV = self.func(*self.args_var)

                if not retV:
                    PrintColor(f'{crossMark}Target "{self.Name}" failed!', theme['error'].Foreground(), theme['error'].Background())
                else:
                    PrintColor(f'{checkBox}Target "{self.Name}" succeded!', theme['success'].Foreground(), theme['success'].Background())

                return retV
            except:
                PrintColor(f'Internal error in the target function "{self.Name}"', theme['error'].Foreground(), theme['error'].Background())
                if Debug:
                    traceback.print_exc()

        else:
            return False


def Parse_Makefile(makefile_path, makefileObj):
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
                TargetV = TargetObject(target_func, target_args, makefileObj)
                Targets[target_func] = TargetV

        # Detect Dependencies
        for key in Targets.keys():
            tarItem = Targets[key]
            for i, item in enumerate(tarItem.Dependencies):
                if callable(item):
                    depTarget_str = tarItem.args_str[i]
                    depTarget = Targets[depTarget_str]
                    tarItem.Dependencies[i] = depTarget

    return Targets


def do_main():
    global Debug

    # Parse Command Line
    parser = argparse.ArgumentParser(description='PyBld is a simple make system implemented in python')
    parser.add_argument('-t', metavar='    Target', help='Make target in the makefile', default='all')
    parser.add_argument('-f', metavar='    Makefile', help=f'Explicit path to makefile, default = {defaultMakefile}', default=defaultMakefile)
    parser.add_argument('-j', metavar='    Jobs', type=int, help='Number of jobs used in the make process')
    parser.add_argument('-v', metavar="    Verbose", type=bool, help='Verbose output', default=False)
    parser.add_argument('-debug', metavar="Debug", type=bool, help='Create output suitable to debug a makefile', default=False)

    args = parser.parse_args()

    # Does the make file exist?
    if not os.path.isfile(args.f):
        retV = input(f'No makefile exists!, do you want to create "{args.f}"? (y/n): ')
        if retV.lower() == 'y':
            tempText = str(gccTemplate)
            with open(args.f, 'w') as f:
                f.write(tempText)
        sys.exit()

    # TODO: ???
    # pkgdir = os.path.normpath(os.path.dirname(__file__) + '/../')
    # sys.path.insert(0, pkgdir)
    # if os.path.exists('/opt/PyBld'):
    #    sys.path.insert(0, '/opt/')

    import imp
    makefileObj = imp.load_source('makefileObj', args.f)
    Shell('rm -f *.pyc')

    # TODO: Make this into a configuration class??
    Debug = getattr(makefileObj, 'Debug', False)

    # Get list of possible targets
    Targets = Parse_Makefile(args.f, makefileObj)

    # If we have a target, execute it
    if args.t:
        try:
            selected_Target = Targets[args.t.strip()]  # type: TargetObject
        except:
            PrintColor(f'Error: target function "{args.t}" does not exist!', theme['error'].Foreground(), theme['error'].Background())
            if Debug:
                traceback.print_exc()
            sys.exit()

        retV = selected_Target.run()
        return retV

    else:
        PrintColor(f'No target to build, exiting...', theme['warning'].Foreground(), theme['warning'].Background())
        sys.exit()


if __name__ == '__main__':
    # Tests
    do_main()
