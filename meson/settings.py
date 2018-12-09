# coding=utf8
#

from collections import namedtuple

BuildParams   = namedtuple('BuildParams', 'prefixrun, mesonargs, cxxflags, linkflags')
BuildTypeConf = namedtuple('BuildTypeConf', 'gcc, clang')

buildroot    = "/tmp/$USER/projects/just.remind.me/build-out"
buildsymlink = "../build-out"
srcroot      = "../src"

common = {
    'cxx-flags'  : '-std=c++17 -Wall -Wextra -Woverloaded-virtual' + \
                    ' -Wunreachable-code -Wvla',
}

debug = BuildTypeConf(
    gcc = BuildParams (
        prefixrun = 'scan-build',
        #prefixrun = '',
        mesonargs = '',
        cxxflags  = '%s %s' % (common['cxx-flags'], '-O0 -g -fno-omit-frame-pointer'),
        linkflags = '',
    ),
    clang = BuildParams (
        prefixrun = 'scan-build',
        #prefixrun = '',
        mesonargs = '',
        cxxflags  = '%s %s' % (common['cxx-flags'], '-O1 -g -fno-omit-frame-pointer -fsanitize=address'),
        linkflags = '',
        # meson pushs cxxflags to ldflags (why?) and as result the adding of -fsanitize=address here produces
        # warning "DEPRECATION: Duplicated values in array option "cpp_link_args" is deprecated"
        #linkflags = '-fsanitize=address',
    ),
)

release = BuildTypeConf(
    gcc = BuildParams (
        prefixrun = '',
        mesonargs = '--unity on',
        cxxflags  = '%s %s' % (common['cxx-flags'], '-O2'),
        linkflags = '',
    ),
    clang = BuildParams (
        prefixrun = '',
        mesonargs = '--unity on',
        cxxflags  = '%s %s' % (common['cxx-flags'], '-O2'),
        linkflags = '',
    ),
)
