#!/usr/bin/env python
# -*- coding: utf-8 -*-

# chksumdir
import os
import argparse
import hashlib

# github snippet for directory checks via argparse
# https://gist.github.com/brantfaircloth/1443543

class FullPaths(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, os.path.abspath(os.path.expanduser(values)))

def is_dir(dirname):
    if not os.path.isdir(dirname):
        msg = "{0} is not a directory".format(dirname)
        raise argparse.ArgumentTypeError(msg)
    else:
        return dirname

def calculate_hash(filename, bs=2**16):
    with open(filename, 'rb') as filep:
        sha256gen = hashlib.sha256()
        while True:
            data = filep.read(bs)
            if not data:
                break
            sha256gen.update(data)
        return sha256gen.hexdigest()

parser = argparse.ArgumentParser(description="""Checksumming directories and files.""")
parser.add_argument('path', help="The directory to checksum", \
    action=FullPaths, type=is_dir)
args = vars(parser.parse_args())

givenpath = args['path']

filelist = os.walk(givenpath)
for root,dir,files in filelist:
    for name in files:
        whatnext = os.path.join(root, name)
        print "{0} {1}".format(calculate_hash(whatnext), whatnext)
