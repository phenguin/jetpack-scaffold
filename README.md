jetpack-scaffold
=======

Project scaffolding generator. 
jetpack-scaffold helps to reuse common utility code between projects while maintaining separation of common code, and project specific code.  Using a git submodule, the common scaffolding code is kept separate from the main project code, but is integrated with symlinks.  This allows utility code to be easily shared between projects no matter where the original edit was made. 


### Install
Requirements: python

To install:

    * git clone https://github.com/phenguin/jetpack-scaffold SOMEDIR/jetpack-scaffold
    * ln -s SOMEDIR/jetpack-scaffold/jetpack.py [SOMEWHEREONYOURPATH]/jetpack

### Usage

#### Initialize a project with project scaffolding located at GITREPO:

    * cd ~/code
    * jetpack init --project PROJECTNAME [ --scaffold-repo GITREPO ]
    * cd PROJECTNAME

    If GITREPO not specified, defaults to jetpack scaffolding located at 
    https://github.com/phenguin/jetpack

#### Recreate symlinks into project dir when new files are added to scaffolding:

    * cd PROJECTDIR
    * jetpack relink

#### Update the scaffolding folder from upstream then update symlinks into project dir:

    * cd PROJECTDIR
    * jetpack update

