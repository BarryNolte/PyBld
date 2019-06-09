"""Utility functions for PyBld."""
from colorama import Fore, Back, Style
from traceback import print_exc


def PrintColor(txt, fg='', bg=''):
    print(f"{fg}{bg}{txt}{Fore.RESET}{Back.RESET}{Style.RESET_ALL}")


def Highlight_Custom(txt, pattern, color):
    """Highlight a string.

    type:(str, pattern, tuple[str]) -> str
     if type(txt) is unicode:
        txt = txt.encode('UTF-8')
    """
    from re import Pattern
    retV = txt
    if isinstance(pattern, Pattern):
        founds = pattern.findall(txt)
        newtxt = txt
        for s in founds:
            colored_s = f'{color[0]}{color[1]}{s}{Style.RESET_ALL}'
            newtxt = newtxt.replace(s, colored_s)
        retV = newtxt
    elif isinstance(pattern, str):
        s = pattern
        colored_s = f'{color[0]}{color[1]}{s}{Style.RESET_ALL}'
        retV = txt.replace(s, colored_s)

    return retV


class Indenter():
    """Used for indenting text for output.
    
    Each time this class is constructed, the indent increases
    by one, and each time it goes out of scope, the indent
    decreases by one.
    """

    def __init__(self):
        """Construct."""
        self.indent = 1

    def __del__(self):
        """Delete."""
        self.indent -= 1

    def GetIndent(self):
        """Return our current indent value."""
        return self.indent


if __name__ == '__main__':
    print(Highlight_Custom('foo bar baz', 'bar', [Fore.GREEN, Back.YELLOW]))
