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
        else:
            self.TargetTime = None

        self.MakeStatus = MakeStatus.NEEDTOBUILD
        if self.TargetTime is not None and self.SourceTime is not None:
            if self.TargetTime > self.SourceTime:
                self.MakeStatus = MakeStatus.NONEEDTOBUILD



class TargetFileList(list):
    """List of Source/Target pairs."""

    def __init__(self, binFile, ext='', builddir='', root=CurrentWorkingDirectory(), filters=None, recurse=False):
        """Initialize class members."""
        # This is a 'virtual' target, the source is the sum of the file list
        self.binaryTarget = TargetFile("[Target Files]")
        self.binaryTarget.Target = os.path.relpath(binFile)

        self.FindSourceFiles(root, filters, recurse)
        self.SetTargets(ext, builddir)

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

        self.binaryTarget.UpdateTarget()

        if config['debug'] is True:
            self.PrintTargetFiles()

    def IsBinaryTargetBuildComplete(self):
        """Is the binary target up to date."""
        self.binaryTarget.UpdateTarget()
        if self.binaryTarget is None:
            return False
        return self.binaryTarget.MakeStatus == MakeStatus.NONEEDTOBUILD

    def IsTargetListBuildComplete(self):
        """Are all targets in the NONEEDTOBUILD state."""
        # Update all the target dates first
        for tf in self:
            tf.UpdateTarget()
        self.binaryTarget.UpdateTarget()

        # If there is any target that is in the 'NEEDTOBUILD' state, then
        # the target list is not 'BuildComplete'
        ret = False if list(filter(lambda tf: tf.MakeStatus == MakeStatus.NEEDTOBUILD, self)) else True
        
        # The virtual source of the binary target has a date of 
        # the *latest* target time
        timeList = []
        for tf in self:
            if tf.TargetTime is not None:
                timeList.append(tf.TargetTime)
        
        tfLast = max(timeList) if timeList else None
        
        self.binaryTarget.SourceTime = tfLast
        self.binaryTarget.UpdateTarget()

        if config['debug'] is True:
            self.PrintTargetFiles()

        return ret

    def PrintTargetFiles(self):
        """Print list of Source/Target/Status."""
        # Update all the target dates first
        for tf in self:
            tf.UpdateTarget()
        self.binaryTarget.UpdateTarget()

        dtFormat = '%Y-%m-%d %H:%M:%S'
        table = [] # this will be a table of tables
        for tf in self:
            src = '...' + tf.Source[-29:] if len(tf.Source) > 32 else tf.Source
            tar = '...' + tf.Target[-29:] if len(tf.Target) > 32 else tf.Target

            dtSrc = time.strftime(dtFormat, time.localtime(tf.SourceTime))
            dtTar = time.strftime(dtFormat, time.localtime(tf.TargetTime)) if tf.TargetTime is not None else 'None'
            graphic = [openCircle, crossMark, checkBox][tf.MakeStatus - 1]
            # add a table to the table of tables
            table.append([graphic, src, dtSrc, tar, dtTar, tf.MakeStatus.name])

        # Add in the virtual binary source/target
        dtSrc = time.strftime(dtFormat, time.localtime(self.binaryTarget.SourceTime))
        dtTar = time.strftime(dtFormat, time.localtime(self.binaryTarget.TargetTime)) if self.binaryTarget.TargetTime is not None else 'None'
            
        graphic = [openCircle, crossMark, checkBox][self.binaryTarget.MakeStatus - 1]
        table.append([graphic, self.binaryTarget.Source, dtSrc, self.binaryTarget.Target, dtTar, self.binaryTarget.MakeStatus.name])

        Y = F.Yellow
        N = F.Reset
        print(tabulate(table, headers=[' ', f'{Y}Source{N}', f'{Y}Source Time{N}', f'{Y}Target{N}', f'{Y}Target Time{N}', f'{Y}Make Status{N}'], tablefmt="psql"))

    def __del__(self):
        """When this gets destroyed, print out the state."""
        if config['debug'] == True:
            self.PrintTargetFiles()


