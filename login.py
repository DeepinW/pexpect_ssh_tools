#!/usr/bin/python

import ssh_tools
import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Usage:\n  {0} <ipfile>".format(sys.argv[0]))

    cmd = None 

    if len(sys.argv) > 2:
        cmd = sys.argv[2]

    with open(sys.argv[1]) as f:
        (ip, user, password, port) = f.readline().split()
        ssh_tools.login_interact(ip, user, password, port, cmd)

