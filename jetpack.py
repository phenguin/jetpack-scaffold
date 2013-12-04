#!/usr/bin/env python

import argparse
import sys
import os
import os.path
import shutil
from contextlib import contextmanager

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
parser.add_argument('--forcelinks', action='store_true')

# Figure out how to make this arg optional
parser.add_argument('--scaffold-repo', type=str, default = 'https://github.com/phenguin/jetpack')

@contextmanager
def chdir(new_dir):
    try:
        saved_cwd = os.getcwd()
        abspath = os.path.abspath(new_dir)
        os.chdir(abspath)
        yield abspath
    finally:
        os.chdir(saved_cwd)

# TODO: Use sensible variable names here.. getting hard to read
def setup_links(source_base_dir, link_base_dir, force_links = False):
    print "\nLinking scaffolding files to project dir."

    if not os.path.isdir(source_base_dir):
        print >>sys.stderr, "Aborting. Scaffolding directory, %s, does not exist" % (source_base_dir, )

    for dirpath, dirnames, filenames in os.walk(source_base_dir):
        if not dirpath.startswith(os.path.join(source_base_dir, '.git')):

            link_base_path = dirpath.replace(source_base_dir, link_base_dir)

            try:
                os.mkdir(link_base_path)
            except OSError:
                pass
            else:
                print "Created directory: %s" % (link_base_path,)
            
            for fn in filenames:

                if fn == 'README.md' or fn.startswith('.') : continue

                source_path = os.path.join(dirpath, fn)
                link_path = os.path.join(link_base_path, fn)
                rel_dirpath = os.path.relpath(dirpath, link_base_dir)
                rel_to_base_dir = os.path.relpath(link_base_dir, link_base_path)
                rel_source_path = os.path.join(rel_to_base_dir, rel_dirpath, fn)

                if os.path.exists(link_path):
                    if os.path.islink(link_path):
                        print "Removing symlink: %s" % (link_path,)
                        os.remove(link_path)
                    else:
                        if force_links:
                            print "force_links set.. Removing file: %s" % (link_path,)
                            os.remove(link_path)
                        else:
                            print >>sys.stderr, "Aborting.. Not overwriting non-link file: %s" % (link_path,)
                            sys.exit(1)

                print "Linking %s --> %s" % (rel_source_path, link_path)
                os.symlink(rel_source_path, link_path)

def find_jetpack_root_from(start_path):
    if not os.path.isdir(start_path):
        start_path = os.path.dirname(start_path)

    dot_jetpack_path = os.path.join(start_path, '.jetpack')

    if os.path.exists(dot_jetpack_path):
        return os.path.dirname(dot_jetpack_path)

    up_path, remainder = os.path.split(start_path)

    if remainder == '': # Then we are at top level directory
        return None
    else:
        return find_jetpack_root_from(up_path)

def get_jetpack_base():
    cwd = os.getcwd()
    # Try to find a .jetpack file in the directories above this one
    # but if one can't be found then just assume we should use cwd
    return find_jetpack_root_from(cwd) or cwd

def relink_scaffolding(force_links = False):
    link_path = get_jetpack_base()
    source_path = os.path.join(link_path, 'scaffolding')
    setup_links(source_path, link_path, force_links = force_links)

def update_scaffolding(force_links = False):
    cwd = os.getcwd()

    with chdir('scaffolding'):
        res1 = os.system('git submodule init')
        res2 = os.system('git submodule update')

    if res1 != 0 or res2 != 0:
        print "Failed to pull changes.. updating links anyways"

    relink_scaffolding(force_links = force_links)

def init_project(project_name, scaffold_repo = None, force_links = False):
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

    with chdir(project_path):
        git_init_res = os.system("git init")
        if git_init_res != 0:
            print >>sys.stderr, "Abort: Could not instantiate git repository in %s.  Is git installed?" % (project_path,)
            sys.exit(1)

        print "\nTrying to clone scaffolding from %s" % (scaffold_repo,)
        clone_exit_code = os.system("git submodule add %s %s" % (scaffold_repo,scaffolding_dir))
        os.system("git commit -am 'Add scaffolding submodule'")

    clone_succeded = clone_exit_code == 0 and True or False

    if clone_succeded:
        setup_links(scaffolding_dir, project_path, force_links = force_links)
        print

        with chdir(project_path):

            # Create .jetpack file in root
            print '\nCreating .jetpack file in project root..'
            with open('.jetpack', 'a'):
                pass

            # Updating newly created git repo with scaffolding
            os.system("git add .")
            os.system("git commit -m 'Link in scaffolding files'")

    print "\nDone!"

def main():
    args = parser.parse_args()
    if args.command == 'init':
        init_project(project_name = args.project, force_links = args.forcelinks)
    elif args.command == 'relink':
        relink_scaffolding(force_links = args.forcelinks)
    elif args.command == 'update':
        update_scaffolding(force_links = args.forcelinks)
    else:
        print "Unrecognized command: %s" % (args.command,)
        sys.exit(1)


if __name__ == '__main__':
    main()
