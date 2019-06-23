[TOC]
# PyBld - A Python based Makefile System
-----
## Defaults
By default, PyBld will look for the file 'makefile.py'.  If for some reason you have a makefile of a different name, it can be changed with the ```'-f'``` option:

```shell
$> pybld -f better_named_makefile.py
```

Without specifying a target on the command line, it will run the ```'all'``` target (if it exists) and any targets that ```'all'``` depends on.

```shell
$> pybld        # This builds the 'all' target
```

```python
config['defaultTargets'] = ['myFavoriteTarget']

    or

config['defaultTargets'] = ['myFavoriteTarget', 'mySecondFavoriteTarget']
```
This value must be in the form of a list.

## Bare Bones Makefile.py
This is the shortest valid makefile:

```python
from PyBld import *

@buildTarget
def all():
    return True
```

## What Makes a PyBld Target?
A PyBld target is simply python function. However, it must be decorated with the```@buildTarget``` decorator.  This allows the function to be depended on by other targets (e.g. the link step depends on the compile step being completed successfully).  If the function returns true, any target that depends on it will be called, if the function returns false, then it will not be called.

## Specifying Dependent Targets Files
Through the```TargetFileList``` function, a search can be done for source files for automatic population of the list.  The list object can then be used as a dependency of a target

```python
binary = 'system.bin'
BUILDdir = './build/'

tfList = TargetFileList(binFile=f'{BUILDdir}{binary}', 
                        targetExt='.o', 
                        builddir=BUILDdir, 
                        filters=['*.cpp', '*.s'])
                        
```
![alt text](./process.svg) Figure 1

## Puting it all together
This is an example of a simple```makefile.py``` that will take all the *.cpp and *.c files in the current directory, compile then link them into```MyApp.exe.```

```python
from PyBld import *
config['debug'] = False # <-- set to True to enable debugging messages

CC = 'gcc'
CFLAGS = '-g'
LINKFLAGS = ''

executable = 'MyApp.exe'
BUILDdir = './Build/'

tfList = TargetFileList(binFile=f'{BUILDdir}{executable}', 
                        targetExt='.o', 
                        builddir=BUILDdir, 
                        filters=['*.cpp', '*.c'])

@buildTarget
def all(link): # depends on Link Target
    print('Build Succeeded')
    return True

@buildTarget
def link(compile): # depends on Compile Target
    if not tfList.IsBinaryTargetBuildComplete():
        strObjFiles = ''
        for target in tfList:
            strObjFiles += target.Target + ' '
      
        _ret, _retCode, _out = Shell(f'{LINK} {LINKFLAGS} {strObjFiles} -o {BUILDdir}{binary}', show_cmd=True, show_output=True)
      
    return tfList.IsBinaryTargetBuildComplete()

@buildTarget
def compile(tfList): # depends on list of source files
    for target in list(filter(lambda tf: tf.MakeStatus == MakeStatus.NEEDTOBUILD, tfList)):
        _ret, _retCode, _out = Shell(f'{CC} {CFLAGS} {target.Target} {target.Source}', show_cmd=True, show_output=True)
    return tfList.IsTargetListBuildComplete()

@buildTarget
def clean():
    RemoveDirectory(BUILDdir)
    return True
"""

```
## Pre/Post functions
Setting one or both of these configuration values will allow for a function to be called before any actions are taken by PyBld and after all actions have been taken by PyBld.  This is useful when a global environment must be created, then destroyed while a build is happening.

```python
config['PreMakeFunction'] = lambda : print('====\nBefore any make file stuff is executed\n====')
config['PostMakeFunction'] = lambda : print('====\nAfter all make file stuff is executed\n====')

```

## Built In Helper Functions
### Files

```python
CurrentWorkingDirectory()   # Return the current working directory
CreateDirectory(name)       # Create directory called 'name'
RemoveDirectory(name)       # Delete directory 'name' and subdirectories
RemoveFile(name)            # Delete the given file name.
RenameFile(old, new)        # Rename file 'old' to 'new'
Touch(name)                 # Touch file 'name', change modified date to now
GetDirectoryFiles(path)     # Return a list of files from 'path'
ChangeDirectory(path)       # Change current directory to 'path'
GetModifyTime(name)         # Get the modified time of file 'name'
```

### Environment
These two functions can get and set environment variables for sub-processes that are launched by PyBld.  This can be used for variables passed to tools like compilers and linkers.

```python
GetEnvVariable(name)           # Get environment variables value
SetEnvVariable(name, value)    # Set environment variable for sub-processes
```
### Debug Setting
Setting the config value 'debug' to 'True' will cause more information to be printed out during the running of PyBld.  This is useful when you need to know how and why PyBld makes some of the decisions it makes with Targets and Dependencies.

```python
config['debug'] = True
```



 

