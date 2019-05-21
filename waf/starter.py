#!/usr/bin/env python
# coding=utf8
#

import sys, os
if sys.hexversion < 0x2070ef0:
    raise ImportError('Python >= 2.7 is required')

SCRIPTS_ROOTDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPTS_ROOTDIR)

WAF_VERSION = "2.0.15"
WAF_DIR     = SCRIPTS_ROOTDIR

def main():

    # Avoid writing .pyc files
    sys.dont_write_bytecode = True
    import assist
    sys.dont_write_bytecode = False

    if not os.path.exists(assist.BUILDROOT):
        os.makedirs(assist.BUILDROOT)
    if assist.BUILDSYMLINK and not os.path.exists(assist.BUILDSYMLINK):
        assist.mksymlink(assist.BUILDROOT, assist.BUILDSYMLINK)

    # We regard WAF_DIR as a directory where file 'wscript' is located
    assist.mksymlink(os.path.join(WAF_DIR, 'wscript'), os.path.join(assist.BUILDROOT, 'wscript'))

    assist.mksymlink(assist.SRCROOT, assist.SRCSYMLINK)

    # use of Options.lockfile is not enough
    os.environ['WAFLOCK'] = '.lock-wafbuild'
    from waflib import Scripting

    cwd = assist.BUILDROOT
    Scripting.waf_entry_point(cwd, WAF_VERSION, WAF_DIR)

    if(len(assist.wafcommands) == 1 and assist.wafcommands[0] == 'distclean'):
        assist.fullclean()

    return 0
