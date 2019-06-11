"""Keeper of the makefile configuration."""

defaultMakefile = './makefile.py'

config = {
    'debug': False,
    'PreMakeFunction': None,
    'PostMakeFunction': None,
    'defines': {},
    'defaultTargets': ['all'],
    'jobs': 4,
}

####
# For later use, termcolor package or terminal-palette
# print_red_on_cyan = lambda x: cprint(x, 'red', 'on_cyan')
# print_red_on_cyan('Hello, World!')
# print_red_on_cyan('Hello, Universe!')
class A():
    """Attribute Codes."""
    
    Reset = '\033[0m'
    Bright  = '\033[1m'
    Dim = '\033[2m'
    Underscore = '\033[4m'
    Blink = '\033[5m'
    Reverse = '\033[7m'
    Hidden = '\033[8m'

class F():
    """Forground Color Codes."""

    Black = '\033[30m'
    Red = '\033[31m'
    Green = '\033[32m'
    Yellow = '\033[33m'
    Blue = '\033[34m'
    Magenta = '\033[35m'
    Cyan = '\033[36m'
    White = '\033[37m'
    Reset = '\033[39m'

class B():
    """Background Color Codes."""
    
    Black = '\033[40m'
    Red = '\033[41m'
    Green = '\033[42m'
    Yellow = '\033[43m'
    Blue = '\033[44m'
    Magenta = '\033[45m'
    Cyan = '\033[46m'
    White = '\033[47m'
    Reset = '\033[49m'



# Fun Emoji's for error reporting
checkBox = u'✅'
crossMark = u'❌'
openCircle = u'⭕'
exclamationMark = u'❗'
questionMark = u'❓'
okBox = u'🆗'
newBox = u'🆕'
freeBox = u'🆓'
prohibitedMark = u'🚫'
warningTriangle = u'⚠'
bellMark = u'🔔'
fireMark = u'🔥'


if __name__ == '__main__':
    print("")
