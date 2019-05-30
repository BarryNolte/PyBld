
# TODO - Clean up imports so the right things are exported :)
from .make import ( find, replace, retarget, 
                    compile, link, archive, run)
from .decorators import target
from .utility import Fore, Back, PrintColor
from .pybuild import *
from .config import config, theme
import better_exchook

# Get better exception information
better_exchook.install()

