from colorama import Fore, Back, Style

defaultMakefile = './makefile.py'

config = {
    'name': 'main.exe',
    'cflags': ['/DNDEBUG', '/DUNICODE', '/O2', '/Wall'],
    'lflags': ['/MACHINE:AMD64'],

    'includepaths': [
        r'C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\include',
        r'C:\Program Files (x86)\Windows Kits\10\Include\10.0.10586.0\shared',
        r'C:\Program Files (x86)\Windows Kits\10\Include\10.0.10586.0\ucrt',
        r'C:\Program Files (x86)\Windows Kits\10\Include\10.0.10586.0\um'
    ],

    'libpaths': [
        r'C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\lib\amd64',
        r'C:\Program Files (x86)\Windows Kits\10\Lib\10.0.10586.0\ucrt\x64',
        r'C:\Program Files (x86)\Windows Kits\10\Lib\10.0.10586.0\um\x64'
    ],

    'libs': ['kernel32.lib', 'user32.lib'],

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
    'info': ColorPair(Fore.LIGHTWHITE_EX),
    'verbose': ColorPair(Fore.WHITE),
    'target': ColorPair(Style.UNDERLINE + Fore.GREEN),
    'success': ColorPair(Fore.GREEN),
}

# Fun Emoji's for error reporting
checkBox = u' \u2705  '
crossMark = u' \u274c  '

if __name__ == '__main__':
    '''Test Functions'''
    print("")
