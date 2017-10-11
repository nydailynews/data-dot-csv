#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Concatenate and move CSVs to prod.
import argparse
import os, sys
import doctest
import json
from addtocsv import addtocsv

def main(args):
    for dirname, dirnames, filenames in os.walk('csv/'):
        for subdirname in dirnames:
            if args.verbose:
                print dirname, subdirname

        dirnames = dirname.split('/')[1:]
        project = dirnames[-1]
        parent = None
        if project != dirnames[0]:
            parent = os.path.join('csv', dirnames[0], 'data.csv')
            print "P", parent
            
        for filename in filenames:
            if parent:
                pass
                
            if args.verbose:
                print dirname, filename
                #print(os.path.join(dirname, filename))

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
    parser.add_argument("--freeze", dest="do_freeze", default=False, action="store_true",
                        help="Take a snaphot of the site before uploading.")
    args = parser.parse_args(args)
    return args

if __name__ == '__main__':
    args = build_parser(sys.argv[1:])

    if args.test == True:
        doctest.testmod(verbose=args.verbose)
    main(args)
