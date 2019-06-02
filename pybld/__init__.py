
# TODO - Clean up imports so the right things are exported :)
from .make import find, replace, retarget, compile, link
from .decorators import target
from .utility import Fore, Back, PrintColor
from .config import crossMark
from .pybuild import *
from .config import config, theme
from .jobs import Shell, ShellAsync
from .fileops import *
from .environment import *

# Get better exception information
def global_exception_hook(type, value, tb):
    R = Fore.RED
    Y = Fore.YELLOW
    C = Fore.CYAN
    N = Fore.RESET
    
    print(f'==========================================')
    print(f'=       {R}PyBld E x c e p t i o n{N}          =')
    print(f'==========================================')
    print('')
    print(f' Type  : {Y}{type}{N}')
    print(f' Value : {Y}{value}{N}')
    
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
