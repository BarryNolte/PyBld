'''Utility functions for PyBld '''
from colorama import Fore, Back, Style
from re import sub, IGNORECASE, Pattern
from time import time, sleep
from traceback import print_exc
from inspect import stack


def get_makefile_var(var_str):
    # TODO: this is a hack at best
    """
    :param var_str: str
    :return:
    """
    outerframe = stack()[1][0]
    outerframe = outerframe.f_back.f_back
    outerframeGlobals = outerframe.f_globals

    try:
        var = outerframeGlobals[var_str]
        return var
    except:
        return None


def Print_Exception():
    print_color('Crash: (Program Exception)', Fore.WHITE, Back.LIGHTGREEN_EX)
    print_exc()


def print_color(txt, fg='', bg='', bold=False):
    print(f"{fg}{bg}{txt}{Fore.RESET}{Back.RESET}{Style.RESET_ALL}")


def xHighlightWarnings(txt):
    return sub('warning', f'{Fore.RED}Warning{Fore.RESET}', txt, flags=IGNORECASE)


def xHighlightErrors(txt):
    return sub('error', f'{Fore.RED}Error{Fore.RESET}', txt, flags=IGNORECASE)


def xHighlightNotes(txt):
    t = sub('note', f'{Fore.CYAN}Note{Fore.RESET}', txt, flags=IGNORECASE)
    return sub('info', f'{Fore.CYAN}Info{Fore.RESET}', t, flags=IGNORECASE)


def wait_process(Timeout, Proc, Print_statusTime=-1):
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
                print_color('\rwaiting... [%d]' % CountDown, bg=Back.YELLOW)
                cindex = 1
            else:
                print('\r                          \r')
                print_color('\rwaiting... [%d]' % CountDown, bg=Back.CYAN)
                cindex = 0

    print('\r          \r')
    return True  # The Process is Timed Out


def Highlight_Custom(txt, pattern, color):
    # type:(str, pattern, tuple[str]) -> str
    # if type(txt) is unicode:
    #    txt = txt.encode('UTF-8')
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


def kill_alive_process(Proc):
    alive = Proc.poll()
    if alive is None:
        try:
            Proc.kill()
        except:
            pass


if __name__ == '__main__':
    '''Test Functions'''
    print(Highlight_Custom('foo bar baz', 'bar', [Fore.GREEN, Back.YELLOW]))
