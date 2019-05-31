import os


def GetEnvVariable(name):
    return os.environ.get(name)


def SetEnvVariable(name, value):
    os.environ[name] = str(value)
