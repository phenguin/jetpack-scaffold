#!/usr/bin/env python

import argparse
import sys
import os
import os.path
import shutil

abs_file_path = os.path.abspath(__file__)

# Do the right thing with symlinks
while os.path.islink(abs_file_path):
    abs_file_path = os.readlink(abs_file_path)

root_dir = os.path.split(abs_file_path)[0]
print "__file__: ", __file__
print "root_dir: ", root_dir
scaffolding_dir = os.path.join(root_dir, 'scaffolding')

parser = argparse.ArgumentParser(description = 'Jetpack deploy script')
parser.add_argument('command', type=str)
parser.add_argument('--project', type=str)

def init_project(project_name):
    cwd = os.getcwd()
    project_path = os.path.join(cwd, project_name)
    print "Initializing new project in %s" % (project_path,)

    try:
        os.mkdir(project_path)
    except OSError:
        print >>sys.stderr, "Error: Directory %s already exists" % (project_name,)
        sys.exit(1)

    print "Copying template into new project root"

    # Better way to do this?
    os.system("cp -r %s/* %s" % (scaffolding_dir, project_path))

def main():
    args = parser.parse_args()
    if args.command == 'init':
        init_project(project_name = args.project)
    else:
        print "Unrecognized command: %s" % (args.command,)
        sys.exit(1)


if __name__ == '__main__':
    main()
