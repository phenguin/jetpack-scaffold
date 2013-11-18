#!/usr/bin/env bash
cd /vagrant
echo $(pwd)
echo $(ls)
apt-get update

# Install dependencies
apt-get install -y $(cat env.deps)

# Install python dependencies
pip install $(cat env.pipdeps)

# Background processes
export LC_CTYPE=en_US.UTF-8 
export LC_ALL=en_US.UTF-8
