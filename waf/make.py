#!/usr/bin/env python
# coding=utf8
#

import sys, os
if sys.hexversion < 0x2070ef0:
    raise ImportError('Python >= 2.7 is required')

SCRIPTDIR = os.path.dirname(os.path.abspath(sys.argv[0]))

WAF_VERSION = "2.0.15"
WAF_DIR     = SCRIPTDIR

# load settings
sys.path.insert(0, SCRIPTDIR)
# Avoid writing .pyc files
sys.dont_write_bytecode = True
import settings
sys.dont_write_bytecode = False

def getPath(path):
    if not path:
        return path

    if not os.path.isabs(path):
        path = os.path.join(SCRIPTDIR, path)

    path = os.path.expandvars(path)
    path = os.path.expanduser(path)
    path = os.path.abspath(path)
    return path

BUILDROOT    = getPath(settings.BUILDROOT)
BUILDSYMLINK = getPath(settings.BUILDSYMLINK)

def main():

    if not os.path.exists(BUILDROOT):
        os.makedirs(BUILDROOT)
    if BUILDSYMLINK and not os.path.exists(BUILDSYMLINK):
        os.symlink(BUILDROOT, BUILDSYMLINK)

    if SCRIPTDIR != WAF_DIR:
        sys.path.insert(0, WAF_DIR)

    from waflib import Scripting
    Scripting.waf_entry_point(SCRIPTDIR, WAF_VERSION, WAF_DIR)

if __name__ == '__main__':
    sys.exit(main())
