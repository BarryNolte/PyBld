"""Keeper of the makefile configuration."""
from colorama import Fore, Back, Style

defaultMakefile = './makefile.py'

config = {
    'debug': False,
    'PreMakeFunction': None,
    'PostMakeFunction': None,
    'defines': {},
    'defaultTargets': ['all'],
    'jobs': 4,
}


class ColorPair:
    def __init__(self, fg, bg=''):
        self.fg = fg
        self.bg = bg

    def Background(self):
        return self.bg

    def Foreground(self):
        return self.fg

####
# For later use, termcolor package or terminal-palette
# print_red_on_cyan = lambda x: cprint(x, 'red', 'on_cyan')
# print_red_on_cyan('Hello, World!')
# print_red_on_cyan('Hello, Universe!')


theme = {
    'error': ColorPair(Fore.RED, Back.BLACK),
    'warning': ColorPair(Fore.YELLOW),
    'info': ColorPair(Fore.LIGHTGREEN_EX, Back.BLUE),
    'plain': ColorPair(Fore.LIGHTWHITE_EX),
    'verbose': ColorPair(Fore.WHITE),
    'target': ColorPair(Style.UNDERLINE + Fore.LIGHTGREEN_EX),
    'success': ColorPair(Fore.GREEN),
}

# Fun Emoji's for error reporting
checkBox = u'✅  '
crossMark = u'❌  '
openCircle = u'⭕  '
exclamationMark = u'❗  '
questionMark = u'❓  '
okBox = u'🆗  '
newBox = u'🆕  '
freeBox = u'🆓  '
prohibitedMark = u'🚫  '
warningTriangle = u'⚠  '
bellMark = u'🔔'
fireMark = u'🔥'


if __name__ == '__main__':
    print("")
