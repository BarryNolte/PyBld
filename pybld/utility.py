'''Utility functions for PyBld '''
from colorama import Fore, Back, Style
from time import time, sleep
from traceback import print_exc


def PrintException():
    PrintColor('Crash: (Program Exception)', Fore.BLACK, Back.LIGHTGREEN_EX)
    print_exc()


def PrintColor(txt, fg='', bg='', bold=False):
    print(f"{fg}{bg}{txt}{Fore.RESET}{Back.RESET}{Style.RESET_ALL}")


def WaitOnProcesses(Timeout, Proc, Print_statusTime=-1):
    cindex = 0
    timeStep = 0.1
    sec_count = 1.0
    CountDown = Timeout

    T1 = time()
    tdiff = time() - T1
    while tdiff < Timeout:
        alive = Proc.poll()
        if alive is not None:
            print('\r                          \r')
            return False
        sleep(timeStep)
        sec_count -= timeStep
        tdiff = time() - T1
        CountDown = int(Timeout - tdiff)
        if tdiff >= Print_statusTime and sec_count <= 0:
            sec_count = 1.0
            if cindex == 0:
                print('\r                          \r')
                PrintColor('\rwaiting... [%d]' % CountDown, bg=Back.YELLOW)
                cindex = 1
            else:
                print('\r                          \r')
                PrintColor('\rwaiting... [%d]' % CountDown, bg=Back.CYAN)
                cindex = 0

    print('\r          \r')
    return True  # The Process is Timed Out


def Highlight_Custom(txt, pattern, color):
    # type:(str, pattern, tuple[str]) -> str
    # if type(txt) is unicode:
    #    txt = txt.encode('UTF-8')
    from re import Pattern
    retV = txt
    if type(pattern) is Pattern:
        founds = pattern.findall(txt)
        newtxt = txt
        for s in founds:
            colored_s = f'{color[0]}{color[1]}{s}{Style.RESET_ALL}'
            newtxt = newtxt.replace(s, colored_s)
        retV = newtxt
    elif type(pattern) is str:
        s = pattern
        colored_s = f'{color[0]}{color[1]}{s}{Style.RESET_ALL}'
        retV = txt.replace(s, colored_s)

    return retV


def KillLiveProcesses(Proc):
    alive = Proc.poll()
    if alive is None:
        try:
            Proc.kill()
        except:
            pass


indent = 0


class Indenter():

    def __init__(self):
        global indent
        indent += 1

    def __del__(self):
        global indent
        indent -= 1

    def GetIndent(self):
        global indent
        return indent


def foo():
    Indenter()


if __name__ == '__main__':
    '''Test Functions'''
    print(Highlight_Custom('foo bar baz', 'bar', [Fore.GREEN, Back.YELLOW]))
    foo()
