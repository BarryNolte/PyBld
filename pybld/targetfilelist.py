"""TargetFileList - Keep track of files with depdencies."""
import os
import fnmatch
import glob
import time
from tabulate import tabulate
from enum import Enum
from pybld.fileops import CurrentWorkingDirectory, CreateDirectory, GetModifyTime
from colorama import Fore
from pybld.configutil import config


class MakeStatus(Enum):
    """Status of the Target."""

    UNKNOWN = 1
    NEEDTOBUILD = 2
    NONEEDTOBUILD = 3


class TargetFile():
    """Represents a source and it's target, along with the staus of the target."""
    
    def __init__(self, sourceFile):
        """Set data to defaults."""
        self.Source = sourceFile
        self.SourceTime = None
        self.Target = None
        self.TargetTime = None
        self.MakeStatus = MakeStatus.UNKNOWN

    def UpdateTarget(self):
        """Update the target modified time and the need to build."""
        if os.path.exists(self.Target):
            self.TargetTime = GetModifyTime(self.Target)
        self.MakeStatus = MakeStatus.NEEDTOBUILD
        if self.TargetTime is not None:
            if self.TargetTime > self.SourceTime:
                self.MakeStatus = MakeStatus.NONEEDTOBUILD



class TargetFileList():
    """List of Source/Target pairs."""

    def __init__(self):
        """Empty the list of Source/Target pairs."""
        self.FileList = []

    def FindSourceFiles(self, root=CurrentWorkingDirectory(), filters=None, recurse=False):
        """Glob for files given the root directory and filter pattern."""
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
        """Given Source files, generate Target files."""
        cwd = CurrentWorkingDirectory()
        bldDir = os.path.join(cwd, builddir)
        CreateDirectory(bldDir)
        for tf in self.FileList:
            file, _ = os.path.splitext(tf.Source)
            tf.Target = os.path.join(bldDir, file + ext)
            tf.Target = os.path.relpath(tf.Target)

            tf.UpdateTarget()
            
        if config['debug'] is True:
            self.PrintTargetFiles()

    def PrintTargetFiles(self):
        """Print list of Source/Target/Status."""
        table = [] # this will be a table of tables
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
            # add a table to the table of tables
            table.append([src, dtSrc, tar, dtTar, tf.MakeStatus])

        Y = Fore.YELLOW
        N = Fore.RESET
        print(tabulate(table, headers=[f'{Y}Source{N}', f'{Y}Source Time{N}', f'{Y}Target{N}', f'{Y}Target Time{N}', f'{Y}Make Status{N}'], tablefmt="psql"))


if __name__ == '__main__':
    x = TargetFileList()
    x.FindSourceFiles(filters=['*.cpp', '*.s'], recurse=True)
    x.SetTargets('.o', 'build')

    x.PrintTargetFiles()
