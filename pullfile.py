#!/usr/bin/python

import ssh_tools
import sys

if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.exit("Usage:\n  {0} <ipfile> <from_path> <to_path>".format(sys.argv[0]))

    with open(sys.argv[1]) as f:
        (ip, user, password, port) = f.readline().split()
        ssh_tools.scp_interact(ip, user, password, port, 
                src = sys.argv[2], 
                dst = sys.argv[3], 
                pullfile = True)

