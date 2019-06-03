import sarge


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

    P = sarge.run(cmd,
                  shell=True,
                  stdout=sarge.Capture(),
                  stderr=sarge.Capture(),
                  async_=False)

    print(P.stderr.text)

    if show_output:
        print(P.stdout.text)

    return P.returncode == 0, P.returncode, P.stdout.text


def ShellAsync(cmds, show_cmd=False):
    if show_cmd:
        for cmd in cmds:
            print(cmd)

    procs = []
    for cmd in cmds:
        P = sarge.run(cmd, shell=True, stdout=sarge.Capture(), stderr=sarge.Capture(), async_=True)
        procs.append(P)

    return procs


def WaitOnProcesses(Procs, show_output=False):
    for p in Procs:
        p.wait()
        print(p.stderr.text)
        if show_output:
            print(p.stdout.text)


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
         'sleep 7 && echo 7',
         'sleep 3 && echo 3',
         'sleep 9 && echo 9',
         'sleep 12 && echo 12'], show_cmd=True)

    WaitOnProcesses(procs, show_output=True)
