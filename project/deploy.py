#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Concatenate and move CSVs to prod.
import argparse
import os, sys
import doctest
import json
from addtocsv import addtocsv
from collections import OrderedDict

def main(args):
    """ Loop through the files in the csv directory,
        concatenating and saving to the deploy directory.
        """
    base_dir = 'csv'
    if args.base_dir:
        base_dir = args.base_dir

    for dirname, dirnames, filenames in os.walk('%s/' % base_dir):
        for subdirname in dirnames:
            if args.verbose:
                print dirname, subdirname

        dirnames = dirname.split('/')[1:]
        project = dirnames[-1]
        parent = None
        if project != dirnames[0]:
            parent = os.path.join(base_dir, dirnames[0], 'data.csv')
        
        # Run through all the non-data.csv files first, do data.csv last
        # because we need that to be complete if we're going to be importing it
        # anywhere else.
        # Note that this assumes a two-tier-at-most deep directory tree.
        for filename in filenames:
            if 'csv' not in filename:
                continue
            if 'category' in filename:
                project = os.path.join(dirname, filename)
            if 'special' in filename:
                special = os.path.join(dirname, filename)
                
            if args.verbose:
                print dirname, filename

        if parent:
            # Add the above csv to the parent.
            pass

def build_parser(args):
    """ This method allows us to test the args.
        >>> args = build_parser(['--verbose'])
        >>> print args.verbose
        True
        """
    parser = argparse.ArgumentParser(usage='$ python deploy.py',
                                     description='Concatenate the CSV files for production',
                                     epilog='Examply use: python deploy.py')
    parser.add_argument("-v", "--verbose", dest="verbose", default=False, action="store_true")
    parser.add_argument("--test", dest="test", default=False, action="store_true")
    parser.add_argument("-b", "--base_dir", dest="base_dir", default=None)
    parser.add_argument("--freeze", dest="do_freeze", default=False, action="store_true",
                        help="Take a snaphot of the site before uploading.")
    args = parser.parse_args(args)
    return args

if __name__ == '__main__':
    args = build_parser(sys.argv[1:])

    if args.test == True:
        doctest.testmod(verbose=args.verbose)
    main(args)
