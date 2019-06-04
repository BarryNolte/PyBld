import subprocess
import shlex


def Shell(cmd, show_cmd=False, show_output=False):
    '''
    Run cmd in the shell returning the output
    :param cmd: (str) command to run in the available shell
    :param show_cmd: (bool) print command to console
    :param show_output: (bool) print command stdout to console
    :return: (bool, int, str) returns pass/fail, return code and the generated text from the shell command
    '''
    if show_cmd:
        print(cmd)

    args = shlex.split(cmd)
    P = subprocess.Popen(args, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    P.wait()
    out, err = P.communicate()

    print(err)

    if show_output:
        print(out)

    return P.returncode == 0, P.returncode, out


def ShellAsync(cmds, show_cmd=False):
    if show_cmd:
        for cmd in cmds:
            print(cmd)

    procs = []
    for cmd in cmds:
        # args = shlex.split(cmd)
        P = subprocess.Popen(cmd, shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        procs.append(P)

    return procs


def WaitOnProcesses(Procs, show_output=False):
    while len(Procs) > 0:
        for p in Procs:
            ret = p.poll()
            if ret is not None:
                Procs.remove(p)
                out, err = p.communicate()
                if err:
                    print('Error: ' + err, end='')
                if show_output and out:
                    print(out, end='')


def KillProcesses(Procs):
    for p in Procs:
        try:
            p.kill()
        except:
            pass


if __name__ == '__main__':
    # Tests
    procs = ShellAsync(
        ['sleep 5 && echo 5',
         'sleep 2 && echo 2',
         'sleep 1 && echo 1',
         'sleep 10 && echo 10',
         'sleep 7 && echo 7 >&2',
         'sleep 3 && echo 3',
         'sleep 9 && echo 9',
         'sleep 12 && echo 12'], show_cmd=True)

    WaitOnProcesses(procs, show_output=True)
