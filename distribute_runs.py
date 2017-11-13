#!/usr/bin/env python
"""
Distributes Herwig runs on multiple machines at THEP in Lund.
"""

import sys
import os
import shutil
import imp
import subprocess
import argparse

import random
import itertools
import time

import load


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
    parser = argparse.ArgumentParser(description='Distribute Herwig runs to the THEP computers.')
    parser.add_argument('-i','--in-file',help='Input file to use as the base file for the runs.')
    parser.add_argument('-R','--nruns',type=check_positive,help='Number of runs per in-file.',required=False,default=1)
    parser.add_argument('-N','--nevents',type=check_positive,help='Number of events per run.',required=False,default=10)
    parser.add_argument('-L','--load',default='low',help='Set load (which computers to run on and number of runs per computer).')
    parser.add_argument('-H','--herwig-path',default='/home/johanthoren/Documents/Herwig/ubuntu_16/Herwig/bin/activate',help='Set the path to the Herwig installation that should be used.')
    parser.add_argument('-a','--analyses-path',default='/home/johanthoren/Documents/Papers/subleading/colorshower2/analyses/exp.sh',help='Set the path to additional analyses that are needed.')
    parser.add_argument('-O','--overwrite',default=False,action='store_true',help='Overwrite without asking.')
    parser.add_argument('-r','--rerun',default=False,action='store_true',help='Rerun an old set of runs, requires a previous run where the clean-up flag was not used (needs a Herwig-scratch folder)')
    parser.add_argument('-c','--clean-up',default=False,action='store_true',help='Clean up Herwig-scratch folder and .run files after finishing.')
    parser.add_argument('--subsequent-shower',default=True,action='store_false',help='Turns off the subsequent shower.')
    parser.add_argument('--p1',nargs = '+',help = '(p1-p5) Arbitrary run parameter. First argument after (p1-p5) is the parameter name, followed by any number of desired values for it.')
    parser.add_argument('--p2',nargs = '+')
    parser.add_argument('--p3',nargs = '+')
    parser.add_argument('--p4',nargs = '+')
    parser.add_argument('--p5',nargs = '+')
    parser.add_argument('-T','--test-nodes',action='store_true',help='Kills processes on the computers defined by load.')
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

def parameterCombinations(parameters):
    """
    Constructs all combinations of extra parameters.
    """
    infile_parameters = []
    for par in parameters:
        if par:
            s = 'set ' + par[0] + ' '
            l = [s + x for x in par[1:]]
            infile_parameters.append(l)
    res = list(itertools.product(*infile_parameters))
    return res

def printRunInfo(sysargv,infile):
    args = get_args(sysargv[1:])

if __name__ == "__main__":
    # Get the arguments
    args = get_args(sys.argv[1:])

    # Do test_nodes

    # Ensure an in file has been provided, and that it exists in the current
    # folder.
    if args.in_file:
        if not os.path.isfile(args.in_file):
            print('There is no in-file named \'{}\' in the current folder.'.format(args.in_file))
            sys.exit()
        if args.in_file[-3:] != '.in':
            print('The file provided for the -i flag, \'{}\', is not a .in file.'.format(args.in_file))
            sys.exit()
    else:
         print('An in-file has to be provided to use this script (except if the --test_nodes flag is used).')
         sys.exit()

    f = open(args.in_file,'r')
    infile = f.readlines()
    f.close()
    infile = [line for line in infile if line.find('saverun') == -1]

    if not args.rerun:
        # Setup the combinations of p1-p5
        parameterSets = parameterCombinations([args.p1,args.p2,args.p3,args.p4,args.p5])
        # Save them in case of a rerun
        with open('parameters','w') as f:
            f.write('parameterSets = '+str(parameterSets))
    else:
        # For a rerun the
        try:
            f = open('parameters','r')
        except IOError:
            print('No parameters file found! It is required for a rerun.')
            sys.exit()
        data = imp.load_source('parameters','',f)
        f.close()
        parameterSets = data.parameterSets


    # If this is a rerun the folder structure should be in place
    if not args.rerun:
        # Create all of the in files and folders
        overwrite = args.overwrite
        for i, par in enumerate(parameterSets):
            d = 'herwig_runs_' + str(i)
            # Create the folder for the runs
            try:
                os.mkdir(d)
            except:
                if not overwrite:
                    ov = raw_input("Looks like you are about to overwrite previous results! Really do that? ([Y]/n): ")
		    if ov=='n':
			sys.exit()
		    else:
			overwrite = True
                try:
                    shutil.rmtree(d)
                except:
                    # hasn't been tested, do that!
                    print('Cannot remove previous result.')
                    sys.exit()
                os.mkdir(d)
            os.chdir(d)

            # Create the in file
            f = open('runs_'+str(i)+'.in','w')
            for line in infile:
                f.write(line + '\n')
            for line in par:
                f.write(line + '\n')
            f.write('saverun runs_' + str(i) + ' EventGenerator')
            f.close()

            # Create script to read with Herwig
            g = open('read.sh','w')
            g.write('#!/bin/bash\n')
            g.write('source ' + args.herwig_path + '\n')
            g.write('source ' + args.analyses_path + '\n')
            g.write('Herwig read runs_' + str(i) + '.in')
            g.close()
            p = subprocess.Popen(['chmod a+x read.sh'],shell=True,stdin=None,stdout=None,stderr=None)
	    while p.poll() is None:
		time.sleep(0.1)

            # Read with Herwig
            try:
                p = subprocess.Popen(['./read.sh > read.log'],shell=True,stdin=None,stdout=None,stderr=None)
                while p.poll() is None:
                    time.sleep(5.0)
            except KeyboardInterrupt:
                p.kill()
                sys.exit()

            os.chdir('..')


    # Setup the seeds
    seeds = randomList(args.nruns,1,999999)
    print(seeds)
    # Set the load
    computers, threads = load.load(args.load)
    print(computers,threads)
    # check in file

    # copy the in file with suitable changes to the relevant folders

    # build Herwig (in multiple folders?)

    # distribute integration

    # distribute runs

    # Debug output
    print("test_nodes = ", args.test_nodes)
