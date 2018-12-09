# coding=utf8
#

buildroot    = "/tmp/$USER/projects/just.remind.me/build-out"
buildsymlink = "../build-out"
srcroot      = "../src"

common = {
    'cxx-flags'  : '-std=c++17 -Wall -Wextra -Woverloaded-virtual' + \
                    ' -Wunreachable-code -Wvla',
}

debug = {
    'toolset'    : 'clang',
    #'prefix-run' : 'scan-build',
    'prefix-run' : '',
    'meson-args' : '',
    'cxx-flags'  : '%s %s' % (common['cxx-flags'], '-O1 -g'),
}

release = {
    'toolset' : "gcc",
    'prefix-run' : '',
    'meson-args' : '--unity on',
    'cxx-flags'  : '%s %s' % (common['cxx-flags'], '-O2'),
}
