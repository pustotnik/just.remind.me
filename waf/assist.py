# coding=utf8
#

import sys, os
import shutil

joinpath  = os.path.join
abspath   = os.path.abspath

# Avoid writing .pyc files
sys.dont_write_bytecode = True
import buildconf
sys.dont_write_bytecode = False

wafcommands = []

def mksymlink(src, dst, force = True):
    """
    Make symlink, force delete if destination exists already
    """
    if force and os.path.exists(dst):
        os.unlink(dst)
    os.symlink(src, dst)

def collectFilesWithWildcard(cwd, pattern):
    from glob import glob
    result = [y for x in os.walk(cwd) for y in glob(_joinpath(x[0], pattern))]
    #print(result)
    return result

def unfoldPath(cwd, path):
    if not path:
        return path

    if not os.path.isabs(path):
        path = joinpath(cwd, path)

    path = os.path.expandvars(path)
    path = os.path.expanduser(path)
    path = abspath(path)
    return os.path.normpath(path)

BUILDCONF_DIR  = os.path.dirname(abspath(buildconf.__file__))
PROJECTNAME    = buildconf.PROJECTNAME
BUILDROOT      = unfoldPath(BUILDCONF_DIR, buildconf.BUILDROOT)
BUILDSYMLINK   = unfoldPath(BUILDCONF_DIR, buildconf.BUILDSYMLINK)
PROJECTROOT    = unfoldPath(BUILDCONF_DIR, buildconf.PROJECTROOT)
SRCROOT        = unfoldPath(BUILDCONF_DIR, buildconf.SRCROOT)
SRCSYMLINKNAME = '%s-%s' %(os.path.basename(PROJECTROOT), os.path.basename(SRCROOT))
SRCSYMLINK     = joinpath(BUILDROOT, SRCSYMLINKNAME)

def fullclean():

    from waflib import Options, Logs

    if BUILDSYMLINK and os.path.isdir(BUILDSYMLINK) and os.path.exists(BUILDSYMLINK):
        Logs.info("Removing directory '%s'" % BUILDSYMLINK)
        shutil.rmtree(BUILDSYMLINK, ignore_errors = True)

    if BUILDSYMLINK and os.path.islink(BUILDSYMLINK) and os.path.lexists(BUILDSYMLINK):
        Logs.info("Removing symlink '%s'" % BUILDSYMLINK)
        os.remove(BUILDSYMLINK)

    if os.path.exists(BUILDROOT):
        Logs.info("Removing directory '%s'" % BUILDROOT)
        shutil.rmtree(BUILDROOT, ignore_errors = True)

    lockfile = os.path.join(PROJECTROOT, Options.lockfile)
    if os.path.exists(lockfile):
        Logs.info("Removing lockfile '%s'" % lockfile)
        os.remove(lockfile)

    lockfile = os.path.join(PROJECTROOT, 'waf', Options.lockfile)
    if os.path.exists(lockfile):
        Logs.info("Removing lockfile '%s'" % lockfile)
        os.remove(lockfile)
