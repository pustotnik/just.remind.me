# coding=utf8
#

from collections import namedtuple

BUILDROOT    = "/tmp/$USER/projects/just.remind.me/build-out"
BUILDSYMLINK = "../build-out"
PROJECTROOT  = ".."
SRCROOT      = "../src"

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
