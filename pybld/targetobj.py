"""TargetObject definition."""
import os
from enum import Enum

from pybld.configutil import checkBox, config, crossMark, F, B, A
from pybld.utility import Indenter


class TargetStatus(Enum):
    """Status Values."""

    NOTRUN = 1
    RUNSUCCESS = 2
    RUNFAIL = 3


class TargetObject():
    """Defines a target, and what it depends on."""

    def __init__(self, func, args, MakefileObj):
        """Initialize class members."""
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
        """Check the validity of a targets dependencies."""
        indent = Indenter()
        idstr = '-' * indent.GetIndent()
        print(f'{idstr} {F.Magenta}Dependency checking of Target "{self.Name}"{F.Reset}')

        # leaf node, this has no dependencies
        if not self.Dependencies:
            return True

        for _, item in enumerate(self.Dependencies):
            if isinstance(item, list):
                # assumed to be list of file names (paths)
                for subitem in item:
                    if not os.path.isfile(subitem.Source):
                        print(f'{crossMark}  Dependency Error @ Target "{self.Name}": file "{subitem.Source}" does not exsist!')
                        return False
            elif isinstance(item, str):
                if not os.path.isfile(item):
                    print(f'{crossMark}  Dependency Error @ Target "{self.Name}": file "{item}" does not exsist!')
                    return False
            elif isinstance(item, TargetObject):  # another target
                if not item.run():
                    print(f'{crossMark}  Dependency Error @ Target "{self.Name}": Target "{item.Name}" failed')
                    return False

        return True

    def run(self):
        """Run the target function if it doesn't have dependencies of it's own."""
        if self.check_dependencies():
            print()
            print(f'{F.Green}{A.Underscore}Executing Target "{self.Name}"{A.Reset}{F.Reset}')
            try:
                self.Status = TargetStatus.RUNFAIL

                retV, time = self.func(*self.args_var)
                self.Time = time

                if not retV:
                    print(f'{crossMark}  Target "{self.Name}" failed!')
                else:
                    self.Status = TargetStatus.RUNSUCCESS
                    print(f'{checkBox}  Target "{self.Name}" succeded! ({time:.4f} sec)')

                return retV
            except(BaseException):
                print(f'{F.Red}Internal error in the target function "{self.Name}"{F.Reset}')
                raise

        else:
            return False
