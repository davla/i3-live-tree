from xvfbwrapper import Xvfb

import subprocess

# from i3ipc.aio import Connection



def main():
    subprocess.run('i3', shell=True)
    # subprocess.run('xfce4-terminal', shell=True)


with Xvfb() as xvfb:
    main()


if __name__ == '__main__':
    main()
