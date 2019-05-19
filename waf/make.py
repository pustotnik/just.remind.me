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

    # use of Options.lockfile is not enough
    os.environ['WAFLOCK'] = '.lock-wafbuild'
    from waflib import Scripting

    # WAF_DIR and utils.SCRIPTS_ROOTDIR are the same because WAF_DIR is directory where waflib
    # is located and utils.SCRIPTS_ROOTDIR is directory where file wscript is located.
    cwd = SCRIPTS_ROOTDIR
    Scripting.waf_entry_point(cwd, WAF_VERSION, WAF_DIR)
    return 0

if __name__ == '__main__':
    sys.exit(main())
