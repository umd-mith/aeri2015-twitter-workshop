#!/usr/bin/env python3

"""
Copy latest notebooks into user workspaces. Also creates symlink to shared
data area if it is not already there. Needs to be run as root. Sorry.
"""

import os
import shutil
import subprocess

data = '/var/jupyterhub/data'
source_user = 'ubuntu'
source_dir = '/home/%s/aeri2015-twitter-workshop' % source_user

# blow away changes?
overwrite = input("overwrite? (y/n) ").lower() == "y"

# where to copy notebooks to
targets = os.listdir('/home')
targets.remove(source_user)

# create data symlink if necessary
for target in targets:
    link = os.path.join('/home', target, 'data')
    if not os.path.islink(link):
        print("linking %s to %s" % (data, link))
        os.symlink(data, link)

# copy each notebook
for file in os.listdir(source_dir):
    if file.endswith('.ipynb'):
        src = os.path.join(source_dir, file)
        for target in targets:
            target = os.path.join('/home/', target, file)
            if not os.path.isfile(target) or overwrite:
                print("copying %s to %s" % (src, target))
                shutil.copyfile(src, target)

# make sure it's writeable by the user
for target in targets:
    dir = os.path.join("/home", target)
    print(['chown', '-R', '%s:%s' % (target, target), dir])
    subprocess.call(['chown', '-R', '%s:%s' % (target, target), dir])
