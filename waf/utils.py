# coding=utf8
#

import sys, os

SCRIPTS_ROOTDIR = os.path.dirname(os.path.abspath(__file__))

def unfoldPath(path):
    if not path:
        return path

    if not os.path.isabs(path):
        path = os.path.join(SCRIPTS_ROOTDIR, path)

    path = os.path.expandvars(path)
    path = os.path.expanduser(path)
    path = os.path.abspath(path)
    return os.path.normpath(path)
