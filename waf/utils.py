# coding=utf8
#

import sys, os

SCRIPTS_ROOTDIR = os.path.dirname(os.path.abspath(__file__))

def unfoldPath(cwd, path):
    if not path:
        return path

    if not os.path.isabs(path):
        path = os.path.join(cwd, path)

    path = os.path.expandvars(path)
    path = os.path.expanduser(path)
    path = os.path.abspath(path)
    return os.path.normpath(path)
