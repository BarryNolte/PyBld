"""Public facing interfaces for PyBld."""
from sys import exit

# TODO - Clean up imports so the right things are exported :)
from .decorators import buildTarget
from .utility import Fore, Back
from .configutil import crossMark, checkBox, config, theme
from .pybuild import *
from .jobs import Shell, ProcessControl
from .fileops import RemoveDirectory,
                     CreateMakefile,
                     RenameFile, 
                     CurrentWorkingDirectory, 
                     ChangeDirectory, 
                     Touch, 
                     GetDirectoryFiles, 
                     GetModifyTime
from .environment import GetEnvVariable, SetEnvVariable
from .targetobj import TargetObject, TargetStatus
from .targetfilelist import TargetFileList, TargetFile, MakeStatus


def global_exception_hook(extype, exvalue, tb):
    """Get better exception information."""
    R = Fore.RED
    Y = Fore.YELLOW
    C = Fore.CYAN
    N = Fore.RESET

    print(f'==========================================')
    print(f'=       {R}PyBld E x c e p t i o n{N}          =')
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
    crash = '   '
    for frame in tbList:
        if frame is tbList[-1]:
            hightLight = R
            crash = crossMark
        print(f'{crash} {frame.name:15} {Y}{frame.lineno:-5}{N}   {hightLight}{frame.line:25}{N}  {frame.filename}')

    print('')
    sys.exit(1)


sys.excepthook = global_exception_hook
