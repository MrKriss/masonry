
import subprocess
import shlex


def run_and_capture(command, give_feedback=True):

    p = subprocess.run(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if p.returncode != 0 and give_feedback:
        print('Error in executing "%s"' % command)
        print(p.stderr.decode().strip())
    elif p.returncode == 0 and give_feedback:
        print('Executed "%s"' % command)

    return p
