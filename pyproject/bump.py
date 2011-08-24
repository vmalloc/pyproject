#! /usr/bin/python
from __future__ import print_function
import argparse
import os
import re
import sys
import subprocess

parser = argparse.ArgumentParser(usage="%(prog)s [options] args...")
parser.add_argument("--minor", dest="minor_bump", action="store_true", default=False)
parser.add_argument("--major", dest="major_bump", action="store_true", default=False)

def main(args):
    version_filename = _get_version_filename(args)
    if version_filename is None:
        print("Version file not found!", file=sys.stderr)
        return -1
    old_version = _get_version(version_filename)
    new_version = _bump(old_version, args)
    print("Bumped from", _stringify(old_version), "to", _stringify(new_version), file=sys.stderr)
    with open(version_filename, "w") as outfile:
        print('__version__ = "{}"'.format(_stringify(new_version)),
              file=outfile)
    _shell("git commit -a -m 'bump version'")
    _shell("git tag v{}".format(_stringify(new_version)))
    return 0

def _bump(version, args):
    returned = version[:]
    if args.major_bump:
        returned = [returned[0] + 1] + [0 for x in returned[1:]]
    elif args.minor_bump:
        returned = [returned[0], returned[1] + 1] + [0 for x in returned[2:]]
    else:
        returned[-1] += 1
    return returned

def _stringify(v):
    return ".".join(map(str, v))

def _shell(cmd):
    returncode = subprocess.call(cmd, shell=True)
    if returncode != 0:
        raise Exception("shell command failed: {!r}".format(cmd))

def _get_version_filename(args):
    matched = []
    for path, dirnames, filenames in os.walk("."):
        if path == ".":
            for excluded in ['build', '.tox']:
                if excluded in dirnames:
                    dirnames.remove(excluded)
        for filename in filenames:
            if filename == "__version__.py":
                matched.append(os.path.join(path, filename))
    if not matched:
        return None
    if len(matched) > 1:
        raise Exception("Too many version files found: {}".format(matched))
    return matched[0]

def _get_version(filename):
    content = open(filename, "rb").read()
    match = re.match(r"^__version__\s+=\s+\"(\d)\.(\d+)\.(\d+)\"\s*$", content.decode('utf-8'), re.S | re.M)
    if not match:
        raise NotImplementedError() # pragma: no cover
    return list(map(int, match.groups()))

#### For use with entry_points/console_scripts
def main_entry_point():
    args = parser.parse_args()
    sys.exit(main(args))
if __name__ == '__main__':
    main_entry_point()
