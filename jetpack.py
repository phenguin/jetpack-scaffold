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

parser = argparse.ArgumentParser(description = 'Jetpack deploy script')
parser.add_argument('command', type=str)
parser.add_argument('--project', type=str)

# TODO: Figure out how to make this arg optional
parser.add_argument('--scaffold-repo', type=str, default = 'https://github.com/phenguin/jetpack')

def setup_links(source_base_dir, link_base_dir):
    print "\nLinking scaffolding files to project dir."
    for dirpath, dirnames, filenames in os.walk(source_base_dir):
        if not dirpath.startswith(os.path.join(source_base_dir, '.git')):

            link_base_path = dirpath.replace(source_base_dir, link_base_dir)

            try:
                os.mkdir(link_base_path)
            except OSError:
                pass
            
            for fn in filenames:
                if fn == 'README.md': continue
                source_path = os.path.join(dirpath, fn)
                link_path = os.path.join(link_base_path, fn)

                if os.path.exists(link_path):
                    if os.path.islink(link_path):
                        os.remove(link_path)
                    else:
                        print >>sys.stderr, "Aborting.. Not overwriting non-link file: %s" % (link_path,)
                        sys.exit(1)

                print "Linking %s --> %s" % (source_path, link_path)
                os.symlink(source_path, link_path)

def relink_scaffolding():
    link_path = os.getcwd()
    source_path = os.path.join(link_path, 'scaffolding')
    setup_links(source_path, link_path)

def update_scaffolding():
    cwd = os.getcwd()
    os.chdir('scaffolding')
    res = os.system('git pull --ff-only')
    os.chdir(cwd)

    if res != 0:
        print "Failed to pull changes.. updating links anyways"

    relink_scaffolding()

def init_project(project_name, scaffold_repo = None):
    cwd = os.getcwd()
    project_path = os.path.join(cwd, project_name)

    print "Initializing new project in %s" % (project_path,)

    scaffold_repo = scaffold_repo or 'https://github.com/phenguin/jetpack'

    # Try to get the scaffolding code
    scaffolding_dir = os.path.join(project_path, 'scaffolding')

    try:
        os.mkdir(project_path)
    except OSError:
        print >>sys.stderr, "Error: Directory %s already exists" % (project_name,)
        sys.exit(1)

    print "\nTrying to clone scaffolding from %s" % (scaffold_repo,)
    clone_exit_code = os.system("git clone %s %s" % (scaffold_repo,scaffolding_dir))
    clone_succeded = clone_exit_code == 0 and True or False

    if clone_succeded:
        setup_links(scaffolding_dir, project_path)

def main():
    args = parser.parse_args()
    if args.command == 'init':
        init_project(project_name = args.project)
    elif args.command == 'relink':
        relink_scaffolding()
    elif args.command == 'update':
        update_scaffolding()
    else:
        print "Unrecognized command: %s" % (args.command,)
        sys.exit(1)


if __name__ == '__main__':
    main()
