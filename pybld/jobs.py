"""Shell Functions for synchronous or asynchronous running of commands."""
import shlex
import subprocess


def Shell(cmd, show_cmd=False, show_output=True):
    """Run cmd in the shell returning the output.
    
    :param cmd: (str) command to run in the available shell
    :param show_cmd: (bool) print command to console
    :param show_output: (bool) print command stdout to console
    :return: (bool, int, str) returns pass/fail, return code and the generated text from the shell command
    """
    if show_cmd:
        print(cmd)

    P = subprocess.Popen(cmd, shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    P.wait()
    out, err = P.communicate()

    if err:
        print(err)

    if show_output:
        if out:
            print(out)

    return P.returncode == 0, P.returncode, out


class ProcessControl:
    """Keeps track of a group of asyncronous sub-processes."""

    def __init__(self, jobs=4):
        """Initialize everything we need to launch sub-processes."""
        self.Procs = []
        self.Cmds = []
        self.Jobs = jobs

    def InsertMoreProcs(self):
        """Start sub-process.
        
        Then insert them into our list of 
        sub-processes, but don't allow more than the number
        defined in Jobs to run concurrently
        """
        while len(self.Procs) < self.Jobs and self.Cmds:
            cmd = self.Cmds.pop()
            P = subprocess.Popen(cmd, shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.Procs.insert(0, P)

    def ShellAsync(self, cmds, show_cmd=False):
        """Take a list of shell commands and begins running them."""
        self.Cmds = cmds
        if show_cmd:
            for cmd in cmds:
                print(cmd)

        self.InsertMoreProcs()

    def WaitOnProcesses(self, show_output=True):
        """Wait until all the sub-processes finish before returning."""
        while self.Procs or self.Cmds:
            procsToScan = self.Procs
            for p in procsToScan:
                ret = p.poll()
                if ret is not None:
                    out, err = p.communicate()
                    if err:
                        print('Error: ' + err, end='')
                    if show_output and out:
                        print(out, end='')
                    self.Procs.remove(p)
                    break
            self.InsertMoreProcs()

    def KillProcesses(self):
        """Kill all the active sub-proccess and prevent new ones from being created."""
        self.Cmds = []  # Empty the list of commands
        for p in self.Procs:
            try:
                p.kill()
            except(BaseException):
                pass


if __name__ == '__main__':
    # Tests
    po = ProcessControl()
    po.ShellAsync(
        ['sleep 5 && echo 5',
         'sleep 2 && echo 2',
         'sleep 1 && echo 1',
         'sleep 10 && echo 10',
         'sleep 7 && echo 7 >&2',
         'sleep 3 && echo 3',
         'sleep 9 && echo 9',
         'sleep 12 && echo 12'], show_cmd=True)

    po.WaitOnProcesses(show_output=True)
