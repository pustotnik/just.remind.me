#!/usr/bin/env python
# coding=utf8
#

import sys, os
if sys.hexversion < 0x2070ef0:
    raise ImportError('Python >= 2.7 is required')

import argparse
import subprocess
import shutil
import filecmp

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
    # I know this is not fastest way but it works in any version of python
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

    isEqual = filecmp.cmp(fileListPathNameNew, fileListPathName)
    os.remove(fileListPathName)
    os.rename(fileListPathNameNew, fileListPathName)
    return not isEqual

def genMesonCmdLine(buildparams, builddir, mesoncmd):

    env = ''
    if buildparams['toolset'] == 'clang':
        env = "CC=clang CXX=clang++"
    elif buildparams['toolset'] == 'gcc':
        env = "CC=gcc CXX=g++"
    else:
        print("Unknown toolset: %s" % buildparams['toolset'])

    env = env + ' CXXFLAGS="%s"' % buildparams['cxx-flags']
    mesonargs = buildparams['meson-args']

    # I use 'plain' because for 'debug' and 'release' buid types meson
    # thinks that it knows which flags I need better than me
    mesonargs = mesonargs + " --werror --buildtype=plain"

    cmdline = """
        cd {mesondir};
        {env} {prefixrun} {mesoncmd} {mesonargs} {blddir};
        """.format(env = env, mesondir = currentdir, mesonargs = mesonargs, mesoncmd = mesoncmd,
            blddir = builddir, prefixrun = buildparams['prefix-run'])

    return cmdline

def doBuild(buildtype):
    params = getattr(settings, buildtype)

    if not os.path.exists(buildroot):
        os.makedirs(buildroot)
    if buildsymlink and not os.path.exists(buildsymlink):
        os.symlink(buildroot, buildsymlink)

    #builddir = os.path.join(buildroot, buildtype)
    builddir = os.path.join(buildroot, "%s-%s" % (buildtype, params['toolset']))
    lastSettingsFilePath    = os.path.join(builddir, 'settings.py')
    currentSettingsFilePath = os.path.join(currentdir, 'settings.py')

    cmdline = ""
    if os.path.exists(builddir):
        needToConfigure = saveFileList(builddir)
        if not needToConfigure:
            needToConfigure = not filecmp.cmp(currentSettingsFilePath, lastSettingsFilePath)

        if needToConfigure:
            # touching of meson.build doesn't work for my case so I need to delete build directory
            shutil.rmtree(builddir, ignore_errors = True)

    if not os.path.exists(builddir):
        cmdline = genMesonCmdLine(params, builddir, 'meson')
        os.makedirs(builddir)
        saveFileList(builddir)

    shutil.copy2(currentSettingsFilePath, lastSettingsFilePath)

    cmdline = """ {cmdline} cd {blddir}; {prefixrun} ninja;
        """.format(cmdline = cmdline, blddir = builddir, prefixrun = params['prefix-run'])

    rv = subprocess.call(cmdline, shell = True)
    return rv

def doCleanUp():

    if buildsymlink and os.path.lexists(buildsymlink):
        os.remove(buildsymlink)

    if os.path.exists(buildroot):
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
