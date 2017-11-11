#!/usr/bin/env python
"""
Distributes Herwig runs on multiple machines at THEP in Lund.
"""

import argparse
import sys
import random


# Debug output
print(sys.argv[1:])

def check_positive(value):
    """
    Type check for the argument parser, checks if a number is a positive integer.
    """
    try:
        ivalue = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("invalid positive int value: \'%s\'" % value)
    if ivalue <= 0:
         raise argparse.ArgumentTypeError("invalid positive int value: %s" % value)
    return ivalue

def get_args(args):
    """
    Get command line options
    """
    parser = argparse.ArgumentParser(description='Distribute Herwig runs to the THEP computers')
    parser.add_argument('-N','--nevents',type=check_positive,help='Number of events to run per infile',required = False, default = 10)

    parser.add_argument('--p1',nargs = '+',help = '(p1-p5) Arbitrary run parameter. First argument after (p1-p5) is the parameter name, followed by any number of desired values for it.')
    parser.add_argument('--p2',nargs = '+')
    parser.add_argument('--p3',nargs = '+')
    parser.add_argument('--p4',nargs = '+')
    parser.add_argument('--p5',nargs = '+')
    parser.add_argument('-T','--test_nodes',type=bool,default = False)
    return parser.parse_args(args)

def randomList(l,imin,imax):
    """
    Creates a list of unique random integers between imin and imax. Used to seed the events.
    """
    n = 0
    rlist = []
    attempts = 0
    maxattempts = 1000
    while n < l:
        r = random.randint(imin,imax)
        if r not in rlist:
            rlist.append(r)
            n += 1
        else:
            attempts += 1
        if attempts > maxattempts:
            break
    return rlist



if __name__ == "__main__":
    args = get_args(sys.argv[1:])
    # Debug output
    print("test_nodes = ", args.test_nodes)

    # build Herwig (in multiple folders?)

    # distribute integration

    # distribute runs

