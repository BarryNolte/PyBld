"""Template text for PyBld."""

makeFileTemplate = """

from PyBld import *
config['debug'] = True # <-- set it to True to enable more debugging messages

CC = 'gcc'
CFLAGS = '-g -O2 -std=c99'
LINKFLAGS = ''

executable = 'MyApp.exe'
BUILDdir = './Build/'

tfList = TargetFileList(f'{BUILDdir}{binary}')
tfList.FindSourceFiles(filters=['*.cpp', '*.c', '*.s'])
tfList.SetTargets('.o', BUILDdir)

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
    Shell(f'rm -r {BUILDdir}')
    return True
"""
