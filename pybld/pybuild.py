import traceback
import sys
import os
import re
import argparse
import argcomplete

from pybld.utility import print_color
from pybld.make import shell

from pybld.makefile_template import gccTemplate
from pybld.config import defaultMakefile
from pybld.config import theme, crossMark

HighlightErrors = False
HighlightWarnings = False
Debug = True


class Target_t(object):
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
        if len(self.Dependencies) == 0:
            return True

        print_color(f'Dependency checking of Target "{self.Name}"', theme['info'].Foreground(), theme['info'].Background())
        for i, item in enumerate(self.Dependencies):
            if type(item) is list:
                # assumed to be list of file names (paths)
                for subitem in item:
                    if not os.path.isfile(subitem):
                        print_color(f'Dependency Error @ Target "{self.Name}": {subitem} does not exsist!', theme['error'].Foreground(), theme['error'].Background())
                        return False
            elif type(item) is str:
                if not os.path.isfile(item):
                    print_color(f'Dependency Error @ Target "{self.Name}": {item} does not exsist!', theme['error'].Foreground(), theme['error'].Background())
                    return False
            elif type(item) is Target_t:  # another target
                if not item.run():
                    print_color(f'Dependency Error @ Target "{self.Name}": Target "{item.Name}" failed', theme['error'].Foreground(), theme['error'].Background())
                    return False

        return True

    def run(self):
        if self.check_dependencies():
            print_color(f'Executing Target "{self.Name}"', theme['target'].Foreground(), theme['target'].Background())
            try:
                if len(self.args_var) == 0:
                    retV = self.func()
                else:
                    retV = self.func(*self.args_var)

                if not retV:
                    print_color(f'{crossMark}Target "{self.Name}" failed', theme['error'].Foreground(), theme['error'].Background())
                return retV
            except:
                print_color(f'Internal error in the target function "{self.Name}"', theme['error'].Foreground(), theme['error'].Background())
                if Debug:
                    traceback.print_exc()

        else:
            return False


def Parse_Makefile(makefile_path, makefileObj):
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
                TargetV = Target_t(target_func, target_args, makefileObj)
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
        makefile_path = defaultMakefile
    if os.path.isfile(makefile_path):
        with open(makefile_path, 'r') as f:
            makefile_str = f.read()

        makefile_lines = makefile_str.splitlines()
        for i, l in enumerate(makefile_lines):
            if l.startswith('@target'):
                resV = re.findall(r'def\s+(\w+)\s*\(', makefile_lines[i + 1])
                Targets.append(resV[0])
    return Targets


def complete_targets(prefix, parsed_args, **kwargs):
    Targets = []
    # argcomplete.warn(parsed_args)
    # argcomplete.warn(parsed_args.f)
    if parsed_args.f:
        Targets = getTargets_forBash_autocomplete(parsed_args.f)
    elif os.path.isfile(defaultMakefile):
        Targets = getTargets_forBash_autocomplete(defaultMakefile)
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
    parser.add_argument('-t', metavar='    Target', type=str, help='Make target in the makefile', default='all')  # .completer = complete_targets
    parser.add_argument('-f', metavar='    Makefile', help=f'Explicit path to makefile, default = {defaultMakefile}', default=defaultMakefile)
    parser.add_argument('-j', metavar='    Jobs', type=int, help='Number of jobs used in the make process')
    parser.add_argument('-v', metavar="    Verbose", type=bool, help='Verbose output', default=False)
    parser.add_argument('-debug', metavar="Debug", type=bool, help='Create output suitable to debug a makefile', default=False)

    argcomplete.autocomplete(parser)

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
    shell('rm -f *.pyc')

    # TODO: Make this into a configuration class??
    Debug = getattr(makefileObj, 'Debug', False)
    HighlightErrors = getattr(makefileObj, 'HighlightErrors', False)
    HighlightWarnings = getattr(makefileObj, 'HighlightWarnings', False)

    # Get list of possible targets
    Targets = Parse_Makefile(args.f, makefileObj)

    # If we have a target, execute it
    if args.t:
        try:
            selected_Target = Targets[args.t.strip()]  # type: Target_t
        except:
            print_color(f'Error: target function "{args.t}" does not exist!', theme['error'].Foreground(), theme['error'].Background())
            if Debug:
                traceback.print_exc()
            sys.exit()

        retV = selected_Target.run()
        return retV

    else:
        print_color(f'No target to build, exiting...', theme['warning'].Foreground(), theme['warning'].Background())
        sys.exit()


if __name__ == '__main__':
    # Tests
    do_main()
