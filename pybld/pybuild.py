import traceback
import sys
import os
import re
import argparse
import argcomplete

from pybld.utility import Fore, Back, print_color
from pybld.make import shell

from pybld.makefile_template import gccTemplate

HighlightErrors = False
HighlightWarnings = False
Debug = True


class EntryPoint:
    def Entry():
        do_main()


class argsT():
    t = 'all'
    f = None
    j = 1


class Target_t(object):
    def __init__(self, func, args, MakefileM):
        self.Name = func
        self.func = getattr(MakefileM, func)
        args_str = [item.strip() for item in args.split(',')]
        args_var = [getattr(MakefileM, item)
                    for item in args_str if item != '']
        self.args_str = args_str
        self.args_var = args_var
        self.MakefileM = MakefileM
        self.Dependencies = args_var

    def check_dependencies(self):
        if len(self.Dependencies) == 0:
            return True

        print_color(f'Dependency checking of Target "{self.Name}"', Fore.WHITE, Back.CYAN)
        for i, item in enumerate(self.Dependencies):
            if type(item) is list:
                # assumed to be list of file names (paths)
                for subitem in item:
                    if not os.path.isfile(subitem):
                        print_color(f'Dependency Error @ Target "{self.Name}": {subitem} does not exsist!', Fore.RED, Back.LIGHTWHITE_EX)
                        return False
            elif type(item) is str:
                if not os.path.isfile(item):
                    print_color(f'Dependency Error @ Target "{self.Name}": {item} does not exsist!', Fore.RED, Back.LIGHTWHITE_EX)
                    return False
            elif type(item) is Target_t:  # another target
                if not item.run():
                    print_color(f'Dependency Error @ Target "{self.Name}": Target "{item.Name}" failed', Fore.RED, Back.LIGHTWHITE_EX)
                    return False

        return True

    def run(self):
        if self.check_dependencies():
            print_color(f'Executing Target "{self.Name}"', Fore.WHITE, Back.CYAN)
            try:
                if len(self.args_var) == 0:
                    retV = self.func()
                else:
                    retV = self.func(*self.args_var)

                if not retV:
                    print_color(f'Target "{self.Name}" failed', Fore.WHITE, Back.RED)
                return retV
            except:
                print_color(f'Internal error in the target function "{self.Name}"', Fore.WHITE, Back.LIGHTRED_EX)
                if Debug:
                    traceback.print_exc()

        else:
            return False


def Parse_Makefile(makefile_path, MakefileM):
    Targets = {}  # type: dict[str, Target_t]
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
                TargetV = Target_t(target_func, target_args, MakefileM)
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


def getTargets_forBash_autocomplete(makefile_path=''):
    Targets = []
    if makefile_path == '':
        makefile_path = './makefile.py'
    if os.path.isfile(makefile_path):
        with open(makefile_path, 'r') as f:
            makefile_str = f.read()

        makefile_lines = makefile_str.splitlines()
        for i, l in enumerate(makefile_lines):
            if l.startswith('@target'):
                resV = re.findall(r'def\s+(\w+)\s*\(', makefile_lines[i + 1])
                Targets.append(resV[0])
    return Targets


def Auto_Target():
    if os.path.isfile('./makefile.py'):
        return True
    else:
        return False


def complete_targets(prefix, parsed_args, **kwargs):
    Targets = []
    # argcomplete.warn(parsed_args)
    # argcomplete.warn(parsed_args.f)
    if parsed_args.f:
        Targets = getTargets_forBash_autocomplete(parsed_args.f)
    elif Auto_Target():
        Targets = getTargets_forBash_autocomplete('./makefile.py')
    else:
        Targets = ["No_MakeFile"]

    return Targets


def print_cmd2():
    argcomplete.warn('print_cmd2:')
    argcomplete.warn('_ARGCOMPLETE: ', os.environ['_ARGCOMPLETE'])
    argcomplete.warn('_ARGCOMPLETE_IFS: ', os.environ['_ARGCOMPLETE_IFS'])
    argcomplete.warn('COMP_LINE: ', os.environ['COMP_LINE'])
    argcomplete.warn('COMP_POINT: ', os.environ['COMP_POINT'])
    argcomplete.warn('_ARGCOMPLETE_COMP_WORDBREAKS: ', os.environ['_ARGCOMPLETE_COMP_WORDBREAKS'])
    argcomplete.warn('COMP_WORDBREAKS: ', os.environ['COMP_WORDBREAKS'])


def do_main():
    global Debug, HighlightErrors, HighlightWarnings

    # Parse Command Line
    parser = argparse.ArgumentParser(description='PyBld is a simple make system implemented in python')
    parser.add_argument('-t', metavar='Target', help='Make target in the makefile', default='all')  # .completer = complete_targets
    parser.add_argument('-f', metavar='MakefilePath', help='Explicit makefile, default = ./makefile.py', default='./makefile.py')
    parser.add_argument('-j', metavar='Jobs', type=int, help='Number of jobs used in the make process')
    parser.add_argument('-v', metavar="Verbose", type=bool, help='Verbose output')
    argcomplete.autocomplete(parser)

    # if len(sys.argv) > 1:
    args = parser.parse_args()
    # else:
    #     args = argsT()

    # if args.f:
    #    makefilePath = args.f
    if not os.path.isfile(args.f):
        retV = input(f'No makefile exists!, do you want to create "{args.f}"? (y/n): ')
        if retV.lower() == 'y':
            tempText = str(gccTemplate)
            with open(args.f, 'w') as f:
                f.write(tempText)
        sys.exit()

    import imp

    # TODO: ???
    # pkgdir = os.path.normpath(os.path.dirname(__file__) + '/../')
    # sys.path.insert(0, pkgdir)
    # if os.path.exists('/opt/PyBld'):
    #    sys.path.insert(0, '/opt/')

    makefileObj = imp.load_source('makefileM', args.f)
    shell('rm -f *.pyc')

    # TODO: Make this into a configuration class??
    Debug = getattr(makefileObj, 'Debug', False)
    HighlightErrors = getattr(makefileObj, 'HighlightErrors', False)
    HighlightWarnings = getattr(makefileObj, 'HighlightWarnings', False)

    Targets = Parse_Makefile(args.f, makefileObj)

    if args.t:
        try:
            selected_Target = Targets[args.t.strip()]  # type: Target_t
        except:
            print_color(f'Error: target function "{args.t}" does not exist!', Fore.RED, Back.LIGHTWHITE_EX)
            if Debug:
                traceback.print_exc()
            sys.exit()

        retV = selected_Target.run()
        return retV

    else:
        print('No target to build, exiting...')
        sys.exit()


if __name__ == '__main__':
    # Tests
    do_main()
