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
sys.path.insert(0, currentdir)
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
    # I know this is not fastest method but it works in any version of python and in any OS
    from glob import glob
    fileList = [y for x in os.walk(srcroot) for y in glob(os.path.join(x[0], '*.cpp'))]
    fileList.sort()
    return fileList

def saveFileList(builddir):
    """
    I don't agree with the position of developers of Meson and CMake that
    specifying target files with a wildcard is a bad thing. For example authors of Meson wrote
    that it is not fast. Yes, I agree that for big projects with a lot of files it can be slow in
    some cases. But for all others it can be fast enough. Why didn't they make it as option?
    I don't know. Variant with external command doesn't work very well and authors of Meson know
    about it. So I needed to make my own solution for that. It is not the best solution
    because it is not integrated in Meson, but it works very well for my case.
    """

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

def genMesonCmdLine(toolset, buildparams, builddir, mesoncmd):

    env = ''
    if toolset == 'clang':
        env = "CC=clang CXX=clang++"
    elif toolset == 'gcc':
        env = "CC=gcc CXX=g++"
    else:
        print("Unknown toolset: %s" % toolset)

    env = env + ' CXXFLAGS="%s"' % buildparams.cxxflags
    env = env + ' LDFLAGS="%s"' % buildparams.linkflags
    mesonargs = buildparams.mesonargs

    # I use 'plain' because for 'debug' and 'release' buid types meson
    # thinks that it knows which flags I need better than me
    mesonargs = mesonargs + " --werror --buildtype=plain"

    cmdline = """
        cd {mesondir};
        {env} {prefixrun} {mesoncmd} {mesonargs} {blddir};
        """.format(env = env, mesondir = currentdir, mesonargs = mesonargs, mesoncmd = mesoncmd,
            blddir = builddir, prefixrun = buildparams.prefixrun)

    return cmdline

def doBuild(buildtype):

    buildtype, toolset = buildtype.split('-', 2)
    params = getattr(getattr(settings, buildtype), toolset)

    if not os.path.exists(buildroot):
        os.makedirs(buildroot)
    if buildsymlink and not os.path.exists(buildsymlink):
        os.symlink(buildroot, buildsymlink)

    #builddir = os.path.join(buildroot, buildtype)
    builddir = os.path.join(buildroot, "%s-%s" % (buildtype, toolset))
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
        cmdline = genMesonCmdLine(toolset, params, builddir, 'meson')
        os.makedirs(builddir)
        saveFileList(builddir)

    shutil.copy2(currentSettingsFilePath, lastSettingsFilePath)

    cmdline = """ {cmdline} cd {blddir}; {prefixrun} ninja;
        """.format(cmdline = cmdline, blddir = builddir, prefixrun = params.prefixrun)

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

    return doBuild(args.action)

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("action", nargs='?', \
        choices=['debug-gcc', 'debug-clang', 'release-gcc', 'release-clang', 'cleanup'], \
        default='debug-gcc', help = "target action, 'debug-gcc' is using by default")

    args = parser.parse_args()
    return run(args)

if __name__ == '__main__':
    sys.exit(main())
