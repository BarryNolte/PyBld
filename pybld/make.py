"""Make functions for PyBld"""

import os

from pybld.utility import Fore, PrintColor
from pybld.config import crossMark
from pybld.config import theme
from pybld.jobs import Shell

import fnmatch


def find(root='./', filter='*', recursive=False, abslute=False, DirOnly=False):
    '''Find Files'''
    srcfiles = []
    rootdir = os.path.abspath(root) if abslute else os.path.normpath(root)
    if recursive:
        for cur_root, dir, files in os.walk(rootdir):
            if DirOnly:
                srcfiles.extend([cur_root + '/' + e for e in dir])
            else:
                for srcfile in fnmatch.filter(files, filter):
                    srcfiles.append(cur_root + '/' + srcfile)
    else:
        for cur_root, dir, files in os.walk(rootdir):
            if DirOnly:
                srcfiles.extend([cur_root + '/' + e for e in dir])
            else:
                for srcfile in fnmatch.filter(files, filter):
                    srcfiles.append(cur_root + '/' + srcfile)
            break

    if DirOnly:
        # add the current root directory to the list
        rootdir = os.path.abspath(root) if abslute else os.path.normpath(root)
        srcfiles.append(rootdir)
    return srcfiles


def compile(compiler, flags, sources, objects):
    PrintColor('Compiling ...', theme['target'].Foreground(), theme['target'].Background())

    if type(sources) is list:
        srcs = sources
    else:  # in the case of str
        srcs = sources.split()

    if type(objects) is list:
        objs = objects
    else:  # in the case of str
        objs = objects.split()

    if len(srcs) != len(objs):
        print(f'{Fore.RED}Error:{Fore.RESET} the length of the source files list does not match with objects files list')
        return False

    for i, item in enumerate(srcs):
        cmd = f'{compiler} {flags} -c {item} -o {objs[i]}'

        srcFile = os.path.basename(item)
        objFile = os.path.basename(objs[i])
        srcFile = srcFile.split('.')[0]
        objFile = objFile.split('.')[0]
        if srcFile != objFile:
            print(f'{crossMark}Compiling Error: source file "{item}" and object file "{objs[i]}" do not match./nMake sure that the source and the object files lists are correspondent')
            return False
        if os.path.isfile(objs[i]):  # if the object file already exists
            src_mTime = os.path.getmtime(item)
            obj_mtime = os.path.getmtime(objs[i])
            if src_mTime <= obj_mtime:
                continue
        else:  # no obj file exists
            objDir = os.path.dirname(objs[i])
            objDir = os.path.normpath(objDir)
            if not os.path.exists(objDir):
                os.makedirs(objDir)

        PrintColor(f'Compiling: {item}', theme['target'].Foreground(), theme['target'].Background())
        success, retcode, outputs = Shell(cmd, True)
        print(outputs)

        if not success:
            PrintColor(f'{crossMark}Error: failed to compile, \n    {cmd}')
            return False

    return True


def link(linker, flags, objects, executable):
    if type(objects) is list:
        objs = ' '.join(objects)
    else:
        objs = objects.strip().strip('\n')

    objectsList = objs.split()

    linkFlag = True
    if os.path.isfile(executable):
        linkFlag = False
        exe_mTime = os.path.getmtime(executable)
        for obj in objectsList:
            obj_mtime = os.path.getmtime(obj)
            if obj_mtime > exe_mTime:
                linkFlag = True
                break

    if linkFlag:
        PrintColor('Linking ...', theme['target'].Foreground(), theme['target'].Background())
        cmd = f'{linker} {flags} {objs} -o {executable}'
        success, retcode, outputs = Shell(cmd, True)
        print(outputs)

        if not success:
            PrintColor(f"Failed to link object files to assemble '{executable}'", theme['error'].Foreground(), theme['error'].Background())
            return False
        else:
            return True
    else:
        return True


def replace(srclist, term, repwith):
    if type(srclist) is list:
        retV = []
        for item in srclist:
            x = item.replace(term, repwith)
            retV.append(x)

        return retV
    else:
        retV = srclist.replace(term, repwith)
        return retV


def retarget(srclist, targetP, omit=''):
    if targetP.endswith('/'):
        targetP = targetP[:-1]

    if type(srclist) is list:
        retV = []
        for item in srclist:
            x = item.replace(omit, '')
            x = targetP + '/' + x
            x = os.path.normpath(x)
            retV.append(x)

        return retV
    else:
        x = srclist.replace(omit, '')
        x = targetP + '/' + x
        x = os.path.normpath(x)
        retV = x
        return retV
