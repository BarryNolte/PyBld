
# TODO - Clean up imports so the right things are exported :)
from .make import ( find, replace, retarget, 
                    compile, link, archive, run)
from .decorators import target
from .utility import Fore, Back, PrintColor
from .pybuild import *
from .config import config, theme

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
    
    tbList = traceback.extract_tb(tb)

    startOfMyCode = 0
    for i, e in reversed(list(enumerate(tbList))):
        if e.name == '<module>':
            startOfMyCode = i
            break
    
    print(f'{C}')
    print(f'  Function Name    Line   Code                       File Name')
    print(f'-----------------|------|--------------------------|----------------------------')
    print(f'{N}')
    lastItem = len(tbList)
    hightLight = ''
    for idx in range(startOfMyCode, lastItem):
        frame = tbList[idx]
        if idx == lastItem - 1:
            hightLight = R
        print(f'  {frame.name:15} {Y}{frame.lineno:-5}{N}   {hightLight}{frame.line:25}{N}  {frame.filename}')
        
    print('')
    sys.exit(1)

sys.excepthook = global_exception_hook
