"""Utility functions for PyBld."""
from traceback import print_exc


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

indent = 0
class Indenter():
    """Used for indenting text for output.
    
    Each time this class is constructed, the indent increases
    by one, and each time it goes out of scope, the indent
    decreases by one.
    """

    def __init__(self):
        """Construct."""
        global indent
        indent += 1

    def __del__(self):
        """Delete."""
        global indent
        indent -= 1

    def GetIndent(self):
        """Return our current indent value."""
        global indent
        return indent


if __name__ == '__main__':
    pass
