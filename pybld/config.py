from colorama import Fore, Back, Style

defaultMakefile = './makefile.py'

config = {
    'debug': False,
    'name': 'main.exe',
    'cflags': [],
    'lflags': [],

    'includepaths': [],

    'libpaths': [],

    'libs': [],

    'bindir': 'bin',
    'objdir': 'obj',
    'srcdir': 'src'
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
# For later use, termcolor package
# print_red_on_cyan = lambda x: cprint(x, 'red', 'on_cyan')
# print_red_on_cyan('Hello, World!')
# print_red_on_cyan('Hello, Universe!')


theme = {
    'error': ColorPair(Fore.RED, Back.BLACK),
    'warning': ColorPair(Fore.YELLOW),
    'info': ColorPair(Fore.LIGHTGREEN_EX, Back.BLUE),
    'verbose': ColorPair(Fore.WHITE),
    'target': ColorPair(Style.UNDERLINE + Fore.LIGHTGREEN_EX),
    'success': ColorPair(Fore.GREEN),
}

# Fun Emoji's for error reporting
checkBox = u'✅  '
crossMark = u'❌  '

if __name__ == '__main__':
    '''Test Functions'''
    print("")
