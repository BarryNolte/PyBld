import os
from pathlib import Path


def CurrentWorkingDirectory():
    return os.getcwd()


def MakeDirectory(name):
    os.makedirs(name, exist_ok=True)


def RemoveDirectory(name):
    os.removedirs(name)


def RenameFile(old, new):
    os.rename(old, new)


def Touch(name):
    Path.touch(name, exist_ok=True)


def GetDirectoryFiles(path):
    return os.listdir(path)


def ChangeDirectory(path):
    return os.chdir(path)


def GetModifyTime(path):
    try:
        return os.path.getmtime(path)
    except os.error:
        pass

    return None
