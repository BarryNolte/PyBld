import os
from enum import Enum
from pybld.utility import Indenter, PrintColor
from pybld.config import theme, crossMark, checkBox


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
