# coding=utf8
#

buildroot    = "/tmp/$USER/projects/just.remind.me/build-out"
buildsymlink = "../build-out"

debug = {
    'toolset'    : 'clang',
    'prefix-run' : 'scan-build',
    'meson-args' : '',
}

release = {
    'toolset' : "gcc",
    'prefix-run' : '',
    'meson-args' : '--unity on',
}
