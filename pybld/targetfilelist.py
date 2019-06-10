"""TargetFileList - Keep track of files with depdencies."""
import fnmatch
import glob
import os
import time
from enum import Enum, IntEnum

from pybld.configutil import A, F, checkBox, config, crossMark, openCircle
from pybld.fileops import (CreateDirectory, CurrentWorkingDirectory,
                           GetModifyTime)
from tabulate import tabulate


class MakeStatus(IntEnum):
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



class TargetFileList(list):
    """List of Source/Target pairs."""

    def __init__(self, outFile):
        """Initialize class members."""
        self.binaryTarget = TargetFile("[objFiles]")
        self.binaryTarget.Target = outFile

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
                self.append(tfo)

    def SetTargets(self, ext='', builddir=''):
        """Given Source files, generate Target files."""
        cwd = CurrentWorkingDirectory()
        bldDir = os.path.join(cwd, builddir)
        CreateDirectory(bldDir)
        for tf in self:
            file, _ = os.path.splitext(tf.Source)
            tf.Target = os.path.join(bldDir, file + ext)
            tf.Target = os.path.relpath(tf.Target)

            tf.UpdateTarget()
            
        if config['debug'] is True:
            self.PrintTargetFiles()

    def IsTargetListBuildComplete(self):
        """Are all targets in the NONEEDTOBUILD state."""        
        ret = True
        if list(filter(lambda tf: tf.MakeStatus == MakeStatus.NEEDTOBUILD, self)):
            ret = False
        
        sortedlist = list(sorted(self, key=lambda tf: tf.TargetTime, reverse=True))
        tfLast = sortedlist[0]
        self.binaryTarget.SourceTime = tfLast.TargetTime
        self.binaryTarget.UpdateTarget()

        if config['debug'] is True:
            self.PrintTargetFiles()

        return ret

    def PrintTargetFiles(self):
        """Print list of Source/Target/Status."""
        table = [] # this will be a table of tables
        for tf in self:
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
            graphic = [openCircle, crossMark, checkBox][tf.MakeStatus - 1]
            # add a table to the table of tables
            table.append([graphic, src, dtSrc, tar, dtTar, tf.MakeStatus.name])

        dtSrc = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.binaryTarget.SourceTime))
        dtTar = 'None'
        if self.binaryTarget.TargetTime is not None:
            dtTar = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.binaryTarget.TargetTime))
        table.append(['', self.binaryTarget.Source, dtSrc, self.binaryTarget.Target, dtTar, self.binaryTarget.MakeStatus.name])

        Y = F.Yellow
        N = A.Reset
        print(tabulate(table, headers=[' ', f'{Y}Source{N}', f'{Y}Source Time{N}', f'{Y}Target{N}', f'{Y}Target Time{N}', f'{Y}Make Status{N}'], tablefmt="psql"))


if __name__ == '__main__':
    x = TargetFileList()
    x.FindSourceFiles(filters=['*.cpp', '*.s'], recurse=True)
    x.SetTargets('.o', 'build')

    x.PrintTargetFiles()
