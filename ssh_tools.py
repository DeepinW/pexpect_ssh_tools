#!/usr/bin/python

import pexpect
import sys
import struct, fcntl, termios, signal

child = None
window_sz = None

def get_window_size():
    s = struct.pack("HHHH", 0, 0, 0, 0)
    a = struct.unpack('hhhh', fcntl.ioctl(sys.stdout.fileno(),
        termios.TIOCGWINSZ , s))

    return a

def sig_win_chg(sig, data):
    global child

    if child:
        child.setwinsize(window_sz[0], window_sz[1])

def login_interact(ip, user, password, port, cmd):
    bin = 'ssh'

    args = ["{0}@{1}".format(user, ip), 
            "-p{0}".format(port), 
            "-o",
            "StrictHostKeyChecking=no"]

    if cmd:
        args.append(cmd)

    global child
    child = pexpect.spawn(bin, args)

    while True:

        ret = child.expect(['password.+', 'yes/no.+'], timeout = 8)

        global window_sz
        window_sz = get_window_size()

        child.setwinsize(window_sz[0], window_sz[1])

        signal.signal(signal.SIGWINCH, sig_win_chg)

        if ret == 0:
            child.send("{0}\n".format(password))
            # set escape_character to None to avoid 
            # escape character break the ssh session.
            child.interact(escape_character = None)
            break
        elif ret == 1:
            child.send("yes\n")
        else:
            print "Login fail: ret={0}".format(ret)
            break

def scp_interact(ip, user, password, port, src, dst, pullfile = False):
    bin = 'scp'

    from_path = None
    to_path = None

    if pullfile:
        from_path = "{0}@{1}:{2}".format(user, ip, src)
        to_path = dst
    else:
        from_path = src
        to_path = "{0}@{1}:{2}".format(user, ip, dst)

    args = ["-P{0}".format(port), 
            "-r",
            from_path,
            to_path
            ]

    global child
    child = pexpect.spawn(bin, args)

    while True:

        ret = child.expect(['password.+', 'yes/no.+'], timeout = 8)

        sz = get_window_size()
        child.setwinsize(sz[0],sz[1])

        if ret == 0:
            child.send("{0}\n".format(password))
            child.interact()
            break
        elif ret == 1:
            child.send("yes\n")
        else:
            print "Transfer file fail: ret={0}".format(ret)
            break

