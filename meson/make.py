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
srcroot      = getPath(settings.srcroot)

def getFileList():
    from glob import glob
    fileList = [y for x in os.walk(srcroot) for y in glob(os.path.join(x[0], '*.cpp'))]
    fileList.sort()
    return fileList

def saveFileList(builddir):
    fileList = getFileList()
    fileListPathName = os.path.join(builddir, "._file-list_.txt")
    fileListPathNameNew = fileListPathName + ".new"
    with open(fileListPathNameNew, 'w') as f:
        for name in fileList:
            f.write("{}\n".format(name))
    if not os.path.exists(fileListPathName):
        os.rename(fileListPathNameNew, fileListPathName)
        return True

    import filecmp
    isEqual = filecmp.cmp(fileListPathNameNew, fileListPathName)
    os.remove(fileListPathName)
    os.rename(fileListPathNameNew, fileListPathName)
    return not isEqual

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

    cmdline = ""
    if not os.path.exists(builddir):
        mesonargs = params['meson-args']
        mesonargs = mesonargs + " --buildtype=" + buildtype
        cmdline = """
            cd {mesondir};
            {env} {prefixrun} meson {mesonargs} {blddir};
            """.format(env = env, mesondir = currentdir, mesonargs = mesonargs, blddir = builddir,
                prefixrun = params['prefix-run'])

        os.makedirs(builddir)
        saveFileList(builddir)
    else:
        listWasChanged = saveFileList(builddir)
        if listWasChanged:
            # touch file meson.build
            os.utime(os.path.join(currentdir, 'meson.build'), None)

    cmdline = """ {cmdline} cd {blddir}; {prefixrun} ninja;
        """.format(cmdline = cmdline, blddir = builddir, prefixrun = params['prefix-run'])

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
