"""Template text for PyBld."""

makeFileTemplate = """

from PyBld import *
config['debug'] = True # <-- set it to True to enable more debugging messages

CC = 'gcc'
CFLAGS = '-g'
LINKFLAGS = ''

executable = 'MyApp.exe'
BUILDdir = './Build/'

tfList = TargetFileList(binFile=f'{BUILDdir}{executable}', 
                        targetExt='.o', 
                        builddir=BUILDdir, 
                        filters=['*.cpp', '*.s'])

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
