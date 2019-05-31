'''Utility functions for PyBld '''
from colorama import Fore, Back, Style
from traceback import print_exc


def PrintException():
    PrintColor('Crash: (Program Exception)', Fore.BLACK, Back.LIGHTGREEN_EX)
    print_exc()


def PrintColor(txt, fg='', bg='', bold=False):
    print(f"{fg}{bg}{txt}{Fore.RESET}{Back.RESET}{Style.RESET_ALL}")


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


if __name__ == '__main__':
    '''Test Functions'''
    print(Highlight_Custom('foo bar baz', 'bar', [Fore.GREEN, Back.YELLOW]))
