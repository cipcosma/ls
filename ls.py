#!/usr/bin/env python
'''
Implements ls

- implemented parameters
    l - long form
    a - all
    R - recursive
    h - human readable form
    t - sort by time

@license: "GPL"
@author: "Ciprian Cosma"
'''


import argparse
import os
import sys
import stat
import pwd
import grp
import time


def parse_arguments(args):
    parser = argparse.ArgumentParser(add_help=False)
    # argparse maps -h to help so we will implement the help message manually
    parser.add_argument("-h", dest="hum_read", action="store_true",
                        default=False)
    parser.add_argument("-l", dest="long_form", action="store_true",
                        default=False)
    parser.add_argument("-R", dest="recursive", action="store_true",
                        default=False)
    parser.add_argument("-a", dest="all", action="store_true",
                        default=False)
    parser.add_argument("-t", dest="time_sort", action="store_true",
                        default=False)
    parser.add_argument("--help", dest="print_help", action="store_true",
                        default=False)
    parser.add_argument("file", nargs='*')
    args = parser.parse_args(args)
    if args.print_help:
        print "Usage: ls [OPTION]... [FILE].."
        print "List information about the FILEs"\
              " (the current directory by default)."
        sys.exit()
    # if no positional arguments, set the cwd as the requested directory
    if len(args.file) == 0:
        args.file.append(os.getcwd())
    return args.hum_read, args.long_form, args.recursive, args.all, args.time_sort,\
           args.print_help, args.file


def directory_crawler(topdir):
    '''Returns a tuple of a dirname and a list of files

    if the recursive flag is set, it descends recusively
    '''
    # try to reconstruct the path
    absdir = os.path.abspath(topdir)
    visited_dirs[absdir] = True
    # is this a real dir ?
    try:
        os.lstat(absdir)
    except OSError:
        print "No such file or directory"
        sys.exit()
    dir_content = os.listdir(absdir)
    # sort the list by name or ctime
    if not time_sort:
        dir_content.sort()
    else:
        # using a lambda function to use the ctime as key
        dir_content.sort(key=lambda i: os.lstat(absdir + "/" + i).st_ctime,
                         reverse=True)
    if recursive:
        yield dir_content, topdir
        # get a list of subdirectories
        to_visit = []
        for i in dir_content:
            if os.path.isdir(absdir + "/" + i) and\
               (absdir + "/" + i not in visited_dirs):
                to_visit.append(topdir + "/" + i)
        for j in to_visit:
            for d, c in directory_crawler(j):
                yield d, c
    else:
        yield dir_content, topdir


def printer(file_list, directory=None):
    '''prints a file or directory

    with a single file argument, print just the file without the header
    with two arguments print the directory header and the files 
    observes the long, all and human options
    only prints one file per line
    does not support sticky bits
    '''

    if directory is not None:
        print directory +":"
        print "total " + str(os.lstat(directory).st_blocks/2)
        for i in file_list:
            if i[0] == "." and not all_option:
                pass
            else:
                print_file(i, directory)
        print


def print_file(file_name, directory=None):
    if directory is not None:
        long_i = os.path.join(os.getcwd(), directory, file_name)
    else:
        long_i = os.path.join(os.getcwd(), file_name)
    if long_form:
        file_stat = os.lstat(long_i)
        if os.path.isdir(long_i):
            sys.stdout.write("d")
        elif os.path.islink(long_i):
            sys.stdout.write("l")
        else:
            sys.stdout.write("-")
        file_rights = int(oct(stat.S_IMODE(file_stat.st_mode)))%1000
        try:
            sys.stdout.write(MODES_DICT[file_rights/100]+MODES_DICT[file_rights%100/10]+\
                  MODES_DICT[file_rights%10] + " ")
        except:
            print '---------',
        sys.stdout.write(str(file_stat.st_nlink) +" ")
        sys.stdout.write(pwd.getpwuid(file_stat.st_uid)[0] + " ")
        sys.stdout.write(grp.getgrgid(file_stat.st_gid)[0] + " ")
        sys.stdout.write(str(file_stat.st_size) + " ")
        sys.stdout.write(time.ctime(file_stat.st_ctime) + " ")
        print file_name
    else:
        print file_name


if __name__ == '__main__':
    # we will keep a global dictionary of visited dirs to avoid loops
    visited_dirs = {}
    # dictionary for printing
    MODES_DICT = {0: '---', 1: '--x', 2: '-w-', 3: '-wx',
                  4: 'r--', 5: 'r-x', 6: 'rw-', 7: 'rwx'}
    # get the arguments
    hum_read, long_form, recursive, all_option,\
    time_sort, print_help, file_list = parse_arguments(sys.argv[1:])
    for f in file_list:
        if os.path.isfile(os.path.join(os.getcwd(), f)):
            print_file(f)
        else:
            for i, j in directory_crawler(f):
                printer( i, j)

