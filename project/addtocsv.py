#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Compare CSVs, adding any new items in the first CSV to the second CSV.
import os, sys
import doctest
import argparse
import unicodecsv as csv
from cStringIO import StringIO
from shutil import copyfile

def addtocsv_fromargs(args):
    """ 
        >>> args = build_parser(['--verbose', 'tests/project-longform.csv', 'tests/data.csv'])
        >>> addtocsv_fromargs(args)
        >>> copyfile('tests/bk.csv', args.files[0][1])
        """
    if len(args.files[0]) > 1:
        addtocsv(args.files[0][0], args.files[0][1])

def get_fieldnames(fp):
    """ Given a file pointer (fp), return an array of fieldnames.
        Assumes fieldnames are in the first row.
        >>> print get_fieldnames('tests/data.csv')
        [u'year', u'datestamp', u'title', u'url']
        """
    with open(fp, 'rb') as csvfile:
        h = csv.reader(csvfile)
        fieldnames = h.next()
        del h
    return fieldnames

def addtocsv(new_file, current_file):
    """ Given two filepaths, open the files, compare the items in the file,
        and add any items that are new.
        >>> addtocsv('tests/project-longform.csv', 'tests/data.csv')
        NEW http://interactive.nydailynews.com/2016/12/NYPD-Cold-Case-Squad-faces-daunting-challenges/
        """
    new = csv.DictReader(file(new_file, 'rb'), encoding='utf-8')
    current = csv.DictReader(file(current_file, 'rb'), encoding='utf-8')

    # Loop through each item in the new csv.
    # If the new item isn't in the current, add it.
    # If the new item is already in the current but has some changes, overwrite the current's item.
    to_add = []
    to_update = []
    urls = []
    current_items = []
    # For each item in the 'new' csv, loop through each item in the current.
    for i, new in enumerate(new):
        for j, existing in enumerate(current):
            current_items.append(existing)
            if new['url'] == existing['url']:
                if new['url'] not in urls:
                    urls.append(new['url'])
                    to_update.append(new)
                    # *** TODO: See if there are differences in the record and only if there are make a change
            else:
                if new['url'] not in urls:
                    if args.verbose:
                        print "NEW", new['url']
                    urls.append(new['url'])
                    to_add.append(new)
        else:
            if new['url'] not in urls:
                urls.append(new['url'])
                to_add.append(new)

    # Eliminate duplicates
    #print current_items
    #current_items = list(set(current_items))

    # Write the current csv
    # First write all the update & additions, and record the id's.
    # Then loop through the existing records and if we haven't already written them, write 'em.
    fieldnames = get_fieldnames(current_file)

    if args.verbose:
        print "WRITING TO %s" % current_file

    with open(current_file, 'wb') as csvfile:
        #current = csv.DictReader(file(current_file, 'rb'), encoding='utf-8')
        writefile = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writefile.writeheader()
        urls = []
        for item in to_add + to_update:
            urls.append(item['url'])
            #print item
            if args.verbose:
                print "WRITING NEW %s" % item['url']
            writefile.writerow(item)

        for item in current_items:
            if item['url'] not in urls:
                if args.verbose:
                    print "WRITING EXISTING %s" % item['url']
                writefile.writerow(item)

def main(args):
    addtocsv_fromargs(args)

def build_parser(args):
    """ A method to handle argparse.
        >>> args = build_parser(['--verbose'])
        >>> print args.verbose
        True
        """
    parser = argparse.ArgumentParser(usage='$ python addtocsv.py file-new.csv file-existing.csv',
                                     description='''Takes a list of CSVs passed as args.
                                                  Returns the items that are in the first one but not in the subsequent ones.''',
                                     epilog='')
    parser.add_argument("-v", "--verbose", dest="verbose", default=False, action="store_true")
    parser.add_argument("--test", dest="test", default=False, action="store_true")
    parser.add_argument("files", action="append", nargs="*")
    args = parser.parse_args(args)
    return args

if __name__ == '__main__':
    args = build_parser(sys.argv)

    if args.test:
        doctest.testmod(verbose=args.verbose)

    main(args)
