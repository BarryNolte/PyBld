"""Make functions for PyBld"""

import os
import sarge

from pybld.utility import Fore, PrintColor, crossMark
from pybld.utility import KillLiveProcesses, WaitOnProcesses

from pybld.config import theme, config

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


def get_dir(path):
    if type(path) is str:
        dir_str = os.path.dirname(path)
        return dir_str
    elif type(path) is list:
        retPaths = []
        for p in path:
            dir_str = os.path.dirname(p)
            retPaths.append(dir_str)
        return retPaths
    else:
        return None


def get_filename(path):
    if type(path) is str:
        dir_str = os.path.basename(path)
        return dir_str
    elif type(path) is list:
        retPaths = []
        for p in path:
            dir_str = os.path.basename(p)
            retPaths.append(dir_str)
        return retPaths
    else:
        return None


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
        success, outputs = ShellAsync(cmd, True)
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
        success, outputs = ShellAsync(cmd, True)
        print(outputs)

        if not success:
            PrintColor(f"Failed to link object files to assemble '{executable}'", theme['error'].Foreground(), theme['error'].Background())
            return False
        else:
            return True
    else:
        return True


def archive(archiver, flags, objects, library):
    if type(objects) is list:
        objs = ' '.join(objects)
    else:
        objs = objects

    objectsList = objs.split()

    satisfactionFlag = False
    if os.path.isfile(library):
        satisfactionFlag = True
        output_mTime = os.path.getmtime(library)
        for obj in objectsList:
            obj_mtime = os.path.getmtime(obj)
            if obj_mtime > output_mTime:
                satisfactionFlag = False
                break

    if not satisfactionFlag:
        PrintColor('Archiving...', theme['target'].Foreground(), theme['target'].Background())
        cmd = f'{archiver} {flags} {library} {objs}'
        success, outputs = ShellAsync(cmd, True)
        print(outputs)

        if not success:
            PrintColor(f"Failed to archive object files to assemble '{library}'", Fore.RED)
            return False
        else:
            return True
    else:
        return True


def normpaths(paths):
    if type(paths) is str:
        dir_str = os.path.normpath(paths)
        return dir_str
    elif type(paths) is list:
        retPaths = []
        for p in paths:
            dir_str = os.path.normpath(p)
            retPaths.append(dir_str)
        return retPaths
    else:
        return None


def join(*args):
    try:
        retV = ' '.join(args)  # this works if all args are str type
        return retV
    except:  # deal with different types
        retV = ''
        for arg in args:
            if type(arg) is list:
                argItems = ' '.join(arg)
                retV += argItems + ' '

            else:  # assume str
                retV += arg + ' '
        return retV


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


def exclude(original, ignors):
    retV = []
    for item in original:
        if item not in ignors:
            retV.append(item)
    return retV


def Shell(cmd):
    '''Run cmd in the shell returning the output'''
    P = sarge.run(cmd, shell=True, stdout=sarge.Capture())
    return P.stdout.text


def ShellAsync(cmd, show_cmd=False, CaptureOutput=False, Timeout=-1):
    if show_cmd:
        print(cmd)
    try:
        if CaptureOutput:
            if Timeout > -1:
                P = sarge.run(cmd, shell=True, stdout=sarge.Capture(), stderr=sarge.Capture(), async_=True)
                sarge.join()
                # sleep(3)
                try:
                    CMD = P.commands[0]  # type: sarge.Command # FIXME: This line generates index exception sometime
                    timed_out = WaitOnProcesses(Timeout, CMD)
                    if timed_out:
                        PrintColor(f'The command "{cmd}" has timed out!', theme['error'].Foreground(), theme['error'].Background())
                    KillLiveProcesses(CMD)
                except:
                    pass
            else:
                P = sarge.run(cmd, shell=True, stdout=sarge.Capture(), stderr=sarge.Capture())
        else:
            if Timeout > -1:
                P = sarge.run(cmd, shell=True, async_=True)
                # sleep(3)
                try:
                    CMD = P.commands[0]  # type: sarge.Command # FIXME: This line generates index exception sometime
                    timed_out = WaitOnProcesses(Timeout, CMD)
                    if timed_out:
                        PrintColor(f'The command "{cmd}" is timed out!', theme['error'].Foreground(), theme['error'].Background())
                    KillLiveProcesses(CMD)
                except:
                    pass
            else:
                P = sarge.run(cmd, shell=True)

        outputs = ''

        if P.stdout and len(P.stdout.text) > 0:
            outputs = P.stdout.text
        if P.stderr and len(P.stderr.text) > 0:
            if outputs == '':
                outputs = P.stderr.text
            else:
                outputs += '\n' + P.stderr.text
        return P.returncode == 0, outputs
    except:
        if config.debug is True:
            from utility import PrintException
            PrintException()

        return False, ''


def run(cmd, show_cmd=False, Highlight=False, Timeout=10):
    """
    :param cmd: (str) the shell command
    :param show_cmd: (bool) print the command before executing it
    :param Highlight: (bool) apply color highlights for the outputs
    :param Timeout: (float) any positive number in seconds
    :return:
    """
    success, outputs = ShellAsync(cmd, show_cmd, False, Timeout)

    return success


def target(func):
    # TODO: Add pre/post functions??
    """
    This is a decorator function
    :param func:
    :return:
    """
    def target_func(*original_args, **original_kwargs):
        # print 'before the func'
        # print original_kwargs
        retV = func(*original_args, **original_kwargs)
        if retV is None or retV is False:
            return False
        else:
            return True
        # print 'after the func'

    return target_func
