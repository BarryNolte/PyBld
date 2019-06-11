"""Public facing interfaces for PyBld."""
import sys

# TODO - Clean up imports so the right things are exported :)
from .configutil import config, checkBox, crossMark, F, B, A
from .decorators import buildTarget
from .environment import GetEnvVariable, SetEnvVariable
from .fileops import (ChangeDirectory, CurrentWorkingDirectory,
                      GetDirectoryFiles, GetModifyTime, RemoveDirectory,
                      RenameFile, Touch)
from .jobs import ProcessControl, Shell
from .targetfilelist import MakeStatus, TargetFile, TargetFileList
from .targetobj import TargetObject, TargetStatus


def global_exception_hook(extype, exvalue, tb):
    """Get better exception information."""
    R = F.Red
    Y = F.Yellow
    C = F.Cyan
    N = A.Reset + F.Reset + B.Reset

    print(f'==========================================')
    print(f'=     {R}PyBld E x c e p t i o n{N}            =')
    print(f'==========================================')
    print('')
    print(f' Type  : {Y}{extype}{N}')
    print(f' Value : {Y}{exvalue}{N}')

    import traceback
    tbList = traceback.extract_tb(tb)

    print(f'{C}')
    print(f'    Function Name    Line   Code                       File Name')
    print(f'  -----------------|------|--------------------------|----------------------------')
    print(f'{N}')

    hightLight = ''
    crash = ' '
    for frame in tbList:
        if frame is tbList[-1]:
            hightLight = R
            crash = crossMark
        print(f' {crash}  {frame.name:15} {Y}{frame.lineno:-5}{N}   {hightLight}{frame.line:25}{N}  {frame.filename}')

    print('')
    sys.exit(1)


sys.excepthook = global_exception_hook
