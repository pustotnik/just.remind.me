#!/usr/bin/env python
# coding=utf8
#

import sys, os

BUILDTOOL_DIRNAME = "waf"
CURRENT_DIR   = os.path.dirname(os.path.abspath(__file__))
BUILDTOOL_DIR = os.path.join(CURRENT_DIR, BUILDTOOL_DIRNAME)

sys.path.insert(0, BUILDTOOL_DIR)

def main():

    # Avoid writing .pyc files
    sys.dont_write_bytecode = True
    import starter
    sys.dont_write_bytecode = False
    return starter.main()


if __name__ == '__main__':
    sys.exit(main())
