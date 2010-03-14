from __future__ import with_statement

import os
import sys

HEADER = """\
Creating filelist for %(folder)s
Categorizing files.
Computing results.


"""

LINE = "%(loc)s\t%(language)s\t%(folder)s\t%(path)s\n"


def main(directory=os.path.curdir):
    """Creates a slocount.sc file compatible with the Hudson plugin, but
    based on the more complete ohcount data.
    """
    base = os.path.abspath(os.path.curdir)
    directory = os.path.abspath(directory)
    directoryname = os.path.basename(directory)

    os.system('ohcount -i %s > ohcount.sc' % directory)

    infile = os.path.join(base, 'ohcount.sc')
    if not os.path.exists(infile):
        sys.exit(1)

    lines = None
    with open(infile, 'r') as fd:
        lines = fd.readlines()

    # Chop of header
    if len(lines) < 5:
        print "ohcount file header didn't match our format assumptions."
        sys.exit(1)
    lines = lines[4:]

    result = []
    files = []
    for line in lines:
        columns = line.split()
        filename = columns[-1]
        files.append(filename)
        result.append(dict(
            language=columns[0],
            filename=filename,
            loc=columns[-2],
        ))

    # What follows is a bit of a hack. Unfortunately ohcount only reports
    # filenames in its output, but we need full paths. The reported filenames
    # aren't unique, so for example `__init__.py` occurs quite often.

    # Build a list of full paths for each file
    paths = []
    for (dirpath, dirnames, filenames) in os.walk(directory):
        if '.svn' not in dirpath:
            for f in filenames:
                if not f.endswith('pyc'):
                    paths.append((f, os.path.join(dirpath, f)))

    # Build a dict pointing to the paths. We use the index in the files list
    # as the key. paths contains more values than files, as the former only
    # containes files recognized by ohcount. The order of appearance in those
    # two lists isn't the same, so we have to start looking for the correct
    # file from the beginning each time
    indexedfiles = {}
    i = 0
    for f in files:
        for f_, p in paths:
            if f_ == f:
                index = paths.index((f_, p))
                indexedfiles[i] = p
                paths.pop(index)
                break
        i += 1

    outfile = os.path.join(base, 'sloccount.sc')
    with open(outfile, 'w') as fd:
        fd.write(HEADER % dict(folder=directoryname))
        i = 0
        # result and files have the same index positions
        for r in result:
            # 15 python  folder  /path/to/folder/filename.ext
            fd.write(LINE % dict(
                loc=r['loc'],
                language=r['language'],
                folder=directoryname,
                path=indexedfiles[i],
            ))
            i += 1


if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        print "You have to specify a directory to be counted."
        sys.exit(1)
    main(directory=args[0])
