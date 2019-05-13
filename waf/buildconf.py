# coding=utf8
#

import sys, os
from collections import namedtuple

PROJECTROOT  = ".."
PROJECTNAME  = 'just.remind.me'
BUILDROOT    = "/tmp/$USER/projects/%s/build-out" % PROJECTNAME
BUILDSYMLINK = os.path.join(PROJECTROOT, "build-out")
SRCROOT      = os.path.join(PROJECTROOT, "src")

BuildParams   = namedtuple('BuildParams', 'prefixrun, wafargs, cxxflags, linkflags')
BuildTypeConf = namedtuple('BuildTypeConf', 'gcc, clang')

common = {
    'cxx-flags'  : '-std=c++17 -Wall -Wextra -Woverloaded-virtual' + \
                    ' -Wunreachable-code -Wvla',
}

debug = BuildTypeConf(
    gcc = BuildParams (
        prefixrun = 'scan-build',
        #prefixrun = '',
        wafargs = '',
        cxxflags  = '%s %s' % (common['cxx-flags'], '-O0 -g -fno-omit-frame-pointer'),
        linkflags = '',
    ),
    clang = BuildParams (
        prefixrun = 'scan-build',
        #prefixrun = '',
        wafargs = '',
        cxxflags  = '%s %s' % (common['cxx-flags'], '-O1 -g -fno-omit-frame-pointer -fsanitize=address'),
        linkflags = '-fsanitize=address',
    ),
)

release = BuildTypeConf(
    gcc = BuildParams (
        prefixrun = '',
        wafargs = '',
        cxxflags  = '%s %s' % (common['cxx-flags'], '-O2'),
        linkflags = '',
    ),
    clang = BuildParams (
        prefixrun = '',
        wafargs = '',
        cxxflags  = '%s %s' % (common['cxx-flags'], '-O2'),
        linkflags = '',
    ),
)
