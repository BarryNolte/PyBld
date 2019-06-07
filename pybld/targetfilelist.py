import os
import fnmatch
import glob
import time
from tabulate import tabulate
from enum import Enum
from pybld.fileops import CurrentWorkingDirectory, MakeDirectory, GetModifyTime
from colorama import Fore
from configutil import config


class MakeStatus(Enum):
    UNKNOWN = 1
    NEEDTOBUILD = 2
    NONEEDTOBUILD = 3


class TargetFile():
    def __init__(self, sourceFile):
        self.Source = sourceFile
        self.SourceTime = None
        self.Target = None
        self.TargetTime = None
        self.MakeStatus = MakeStatus.UNKNOWN


class TargetFileList():
    def __init__(self):
        self.FileList = []

    def FindSourceFiles(self, root=CurrentWorkingDirectory(), filters=None, recurse=False):
        if filters is None:
            filters = ['*']

        files = glob.glob(os.path.join(root, '**'), recursive=recurse)

        for pattern in filters:
            for filename in fnmatch.filter(files, pattern):
                filePath = os.path.join(root, filename)
                filePath = os.path.relpath(filePath)

                tfo = TargetFile(filePath)
                tfo.SourceTime = os.path.getmtime(filePath)
                self.FileList.append(tfo)

    def SetTargets(self, ext='', builddir=''):
        cwd = CurrentWorkingDirectory()
        bldDir = os.path.join(cwd, builddir)
        MakeDirectory(bldDir)
        for tf in self.FileList:
            file, _ = os.path.splitext(tf.Source)
            tf.Target = os.path.join(bldDir, file + ext)
            tf.Target = os.path.relpath(tf.Target)

            if os.path.exists(tf.Target):
                tf.TargetTime = GetModifyTime(tf.Target)
            tf.MakeStatus = MakeStatus.NEEDTOBUILD
            if tf.TargetTime is not None:
                if tf.TargetTime > tf.SourceTime:
                    tf.MakeStatus = MakeStatus.NONEEDTOBUILD

        if config['debug'] is True:
            self.PrintTargetFiles()

    def PrintTargetFiles(self):
        table = []
        for tf in self.FileList:
            src = ''
            if len(tf.Source) > 32:
                src = '...' + tf.Source[-29:]
            else:
                src = tf.Source
            tar = ''
            if len(tf.Target) > 32:
                tar = '...' + tf.Target[-29:]
            else:
                tar = tf.Target

            dtSrc = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(tf.SourceTime))
            dtTar = 'None'
            if tf.TargetTime is not None:
                dtTar = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(tf.TargetTime))
            table.append([src, dtSrc, tar, dtTar, tf.MakeStatus])

        Y = Fore.YELLOW
        N = Fore.RESET
        print(tabulate(table, headers=[f'{Y}Source{N}', f'{Y}Source Time{N}', f'{Y}Target{N}', f'{Y}Target Time{N}', f'{Y}Make Status{N}'], tablefmt="psql"))


if __name__ == '__main__':
    x = TargetFileList()
    x.FindSourceFiles(filters=['*.cpp', '*.s'], recurse=True)
    x.SetTargets('.o', 'build')

    x.PrintTargetFiles()
