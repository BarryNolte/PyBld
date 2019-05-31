import sarge
from time import time, sleep
from pybld.utility import PrintColor, Back
from pybld.config import theme


def Shell(cmd, show_cmd=False, show_output=False):
    '''
    Run cmd in the shell returning the output
    :param cmd: (str) command to run in the available shell
    :return: (bool, int, str) returns pass/fail, return code and the generated text from the shell command
    '''
    if show_cmd:
        print(cmd)

    P = sarge.run(cmd, shell=True, stdout=sarge.Capture())

    if show_output:
        print(P.stdout.text)

    return P.returncode == 0, P.returncode, P.stdout.text


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
        return P.returncode == 0, P.returncode, outputs
    except:
        raise

    return False, P.returncode, ''


def WaitOnProcesses(Timeout, Proc, Print_statusTime=-1):
    cindex = 0
    timeStep = 0.1
    sec_count = 1.0
    CountDown = Timeout

    T1 = time()
    tdiff = time() - T1
    while tdiff < Timeout:
        alive = Proc.poll()
        if alive is not None:
            print('\r                          \r')
            return False
        sleep(timeStep)
        sec_count -= timeStep
        tdiff = time() - T1
        CountDown = int(Timeout - tdiff)
        if tdiff >= Print_statusTime and sec_count <= 0:
            sec_count = 1.0
            if cindex == 0:
                print('\r                          \r')
                PrintColor('\rwaiting... [%d]' % CountDown, bg=Back.YELLOW)
                cindex = 1
            else:
                print('\r                          \r')
                PrintColor('\rwaiting... [%d]' % CountDown, bg=Back.CYAN)
                cindex = 0

    print('\r          \r')
    return True  # The Process is Timed Out


def KillLiveProcesses(Proc):
    alive = Proc.poll()
    if alive is None:
        try:
            Proc.kill()
        except:
            pass
