from colorama import Fore, Back

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

fg = 0  # Index offsets into color array
bg = 1
theme = {
    'error': [Fore.RED, Back.BLACK],
    'warning': [Fore.YELLOW, Back.BLACK],
    'info': [Fore.LIGHTWHITE_EX, Back.BLACK],
    'verbose': [Fore.WHITE, Back.BLACK],
    'task': [Fore.CYAN, Back.BLUE],
    'success': [Fore.GREEN, Back.BLACK],
}

# Fun Emoji's for error reporting
checkBox = u' \u2705  '
crossMark = u' \u274c  '

if __name__ == '__main__':
    '''Test Functions'''
    print("")
