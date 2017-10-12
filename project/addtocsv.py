#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Compare CSVs, adding any new items in the first CSV to the second CSV.
import os, sys
import doctest
import argparse
import unicodecsv as csv
from cStringIO import StringIO

def addtocsv(args):
    """ 
        >>> addtocsv({'files': ['tests/data.csv', 'tests/project-longform.csv']})
        """
    if len(args.files[0]) > 1:
        new = csv.DictReader(file(args.files[0][0], 'rb'), encoding='utf-8')
        current = csv.DictReader(file(args.files[0][1], 'rb'), encoding='utf-8')

        # Loop through each item in the new csv.
        # If the new item isn't in the current, add it.
        # If the new item is already in the current but has some changes, overwrite the current's item.
        to_add = []
        to_update = []
        ids = []
        current_items = []
        for i, new in enumerate(new):
            for j, existing in enumerate(current):
                current_items.append(existing)
                if new['id'] == existing['id']:
                    if new['id'] not in ids:
                        ids.append(new['id'])
                        to_update.append(new)
                else:
                    if new['id'] not in ids:
                        ids.append(new['id'])
                        to_add.append(new)
            else:
                if new['id'] not in ids:
                    ids.append(new['id'])
                    to_add.append(new)

        # Write the current csv
        # First write all the update & additions, and record the id's.
        # Then loop through the existing records and if we haven't already written them, write 'em.
        with open(args.files[0][1], 'rb') as csvfile:
            h = csv.reader(csvfile)
            fieldnames = h.next()
            del h

        with open(args.files[0][1], 'wb') as csvfile:
            current = csv.DictReader(file(args.files[0][1], 'rb'), encoding='utf-8')
            writefile = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writefile.writeheader()
            ids = []
            for item in to_add + to_update:
                ids.append(item['id'])
                #print item
                writefile.writerow(item)

            for item in current_items:
                if item['id'] not in ids:
                    if args.verbose:
                        print "NEW", item['id']
                    writefile.writerow(item)

def main(args):
    addtocsv(args)

def build_parser(args):
    """ A method to handle argparse.
        >>> args = build_parser(None)
        >>> print args.verbose
        False
        """
    parser = argparse.ArgumentParser(usage='$ python addtocsv.py file-new.csv file-existing.csv',
                                     description='''Takes a list of CSVs passed as args.
                                                  Returns the items that are in the first one but not in the subsequent ones.''',
                                     epilog='')
    parser.add_argument("-v", "--verbose", dest="verbose", default=False, action="store_true")
    parser.add_argument("--test", dest="test", default=False, action="store_true")
    parser.add_argument("files", action="append", nargs="*")
    return parser.parse_args()

if __name__ == '__main__':
    args = build_parser(sys.argv)

    if args.test:
        doctest.testmod(verbose=args.verbose)

    main(args)
