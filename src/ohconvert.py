#!/usr/bin/env python
"""\
Usage: %prog path ...

Output Hudson SLOCCountPlugin compatible data collected with ohcount.\
"""
usage = __doc__

import os.path
import sys
from optparse import OptionParser
from subprocess import Popen, PIPE

def count(names):
    """Create ouptut equivalent to::
    sloccount --duplicates --wide --details path ...
    """
    if len(names) == 1:
        directory = os.path.abspath(names[0])
        paths = [os.path.join(directory, name) for name in os.listdir(directory) if not name.startswith('.')]
    else:
        paths = [os.path.abspath(name) for name in names]
    directories = [path for path in paths if os.path.isdir(path)]
    top_dir = [path for path in paths if path not in directories]
    if top_dir:
        yield "Have a non-directory at the top, so creating directory top_dir"
        for path in top_dir:
            yield "Adding %s to top_dir" % path
    for entry in directories:
        yield "Creating filelist for %s" % entry
    yield "Categorizing files."
    yield "Computing results.\n\n"
    for output in count_paths('top_dir', top_dir):
        yield output
    for directory in directories:
        for output in count_directory(directory):
            yield output

def count_directory(directory):
    directoryname = os.path.basename(directory)
    stdout, stderr = Popen(['ohcount', '-d', directory], stdout=PIPE).communicate()
    lines = (line.split('\t') for line in stdout.split('\n')[:-1])
    paths = (path for lang, path in lines if lang != '(null)')
    for output in count_paths(directoryname, paths):
        yield output

def count_paths(directoryname, paths):
    for path in paths:
        output = ohcount_file(path, directoryname)
        if output is not None:
            yield output

def ohcount_file(path, directoryname):
        stdout, stderr = Popen(['ohcount', '-i', path], stdout=PIPE).communicate()
        result = stdout.split('\n')[4]
        if result:
            lang, code = result.split()[:2]
            return '\t'.join((code, lang, directoryname, path))

def add_newlines(lines):
    for line in lines:
        yield line
        yield '\n'

def main():
    parser = OptionParser(usage=usage)
    parser.add_option("-o", "--output", metavar="sloccount.sc",
                      help="Output filename (instead of stdout)",
                      dest="output", default=None)
    options, args = parser.parse_args()
    if not args:
        parser.error("You must specify a path to be counted.")
    if options.output is None:
        out = sys.stdout
    else:
        out = open(options.output, 'wt')
    out.writelines(add_newlines(count(args)))

if __name__ == '__main__':
    main()
