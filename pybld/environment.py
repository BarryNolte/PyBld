"""Environment Variable Helpers.

These can be used to pass information to other proccess
or makefiles.
"""
import os


def GetEnvVariable(name):
    """Get a named environment variable."""
    return os.environ.get(name)


def SetEnvVariable(name, value):
    """Set a named environment variable with a given value."""
    os.environ[name] = str(value)
