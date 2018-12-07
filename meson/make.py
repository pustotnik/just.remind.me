#!/usr/bin/env python
# coding=utf8
#

import sys, os
if sys.hexversion < 0x2070ef0:
    raise ImportError('Python >= 2.7 is required')

import argparse
import subprocess
from collections import defaultdict

# Avoid writing .pyc files
sys.dont_write_bytecode = True
currentdir = os.path.dirname(os.path.abspath(sys.argv[0]))

# load settings
sys.path.insert(0, os.getcwd())
import settings

def getPath(path):
    if not path:
        return path

    if not os.path.isabs(path):
        path = os.path.join(currentdir, path)

    path = os.path.expandvars(path)
    path = os.path.expanduser(path)
    path = os.path.abspath(path)
    return path

buildroot    = getPath(settings.buildroot)
buildsymlink = getPath(settings.buildsymlink)

def doBuild(buildtype):
    params = getattr(settings, buildtype)

    env = ''
    if params['toolset'] == 'clang':
        env = "CC=clang CXX=clang++"
    elif params['toolset'] == 'gcc':
        env = "CC=gcc CXX=g++"
    else:
        print("Unknown toolset: %s" % params['toolset'])
        return 1

    if not os.path.exists(buildroot):
        os.makedirs(buildroot)
    if buildsymlink and not os.path.exists(buildsymlink):
        os.symlink(buildroot, buildsymlink)

    #builddir = os.path.join(buildroot, buildtype)
    builddir = os.path.join(buildroot, "%s-%s" % (buildtype, params['toolset']))
    if not os.path.exists(builddir):
        os.makedirs(builddir)

    mesonargs = params['meson-args']
    mesonargs = mesonargs + " --buildtype=" + buildtype
    cmdline = """
        export {env};
        cd {mesondir};
        {prefixrun} meson {mesonargs} {blddir};
        cd {blddir};
        {prefixrun} ninja;
        """.format(env = env, mesondir = currentdir, mesonargs = mesonargs, blddir = builddir,
            prefixrun = params['prefix-run'])

    rv = subprocess.call(cmdline, shell = True)
    return rv

def doCleanUp():

    if buildsymlink and os.path.lexists(buildsymlink):
        os.remove(buildsymlink)

    if os.path.exists(buildroot):
        import shutil
        shutil.rmtree(buildroot, ignore_errors = True)

    return 0

def run(args):

    if args.action == 'cleanup':
        return doCleanUp()

    if args.action in ('debug', 'release'):
        return doBuild(args.action)

    print("Unknown action: %s" % args.action)
    return 1

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("action", nargs='?', choices=['debug', 'release', 'cleanup'], \
        default='debug', help = "target action, 'debug' by default")

    args = parser.parse_args()
    return run(args)

if __name__ == '__main__':
    sys.exit(main())
