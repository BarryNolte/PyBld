"""Common file operations."""
import os
import shutil
from pathlib import Path


def CurrentWorkingDirectory():
    """Return the Current Working Directory, CWD or PWD."""
    return os.getcwd()


def CreateDirectory(name):
    """Create the given directory name."""
    os.makedirs(name, exist_ok=True)


def IsDirectory(path):
    """Return if path is a directory."""
    return os.path.isdir(path)


def RemoveDirectory(path):
    """Remove the given directory name.  This will also remove all subdirecties."""
    shutil.rmtree(path, ignore_errors=False)


def RenameFile(old, new):
    """Rename a given old file name and change it to the given new name."""
    os.rename(old, new)


def Touch(name):
    """Touch the given file, changes the modification time of the given file to the current time."""
    Path.touch(name, exist_ok=True)


def GetDirectoryFiles(path):
    """Return a list of all files in the current directory."""
    return os.listdir(path)


def ChangeDirectory(path):
    """Change our current directory."""
    return os.chdir(path)


def GetModifyTime(name):
    """Get the modification time of the given file."""
    try:
        return os.path.getmtime(name)
    except os.error:
        pass

    return None
