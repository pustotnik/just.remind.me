# coding=utf8
#

import os, getpass, tempfile

username = getpass.getuser()     # portable way to get user name
tmpdir   = tempfile.gettempdir() # portable way to get temp directory

project = dict(
    name     = 'just.remind.me',
    version  = '0.0.1',
    root     = ".",
)

"""
Using 'buildroot' and 'buildsymlink' at the same time has sense mostly on linux
where '/tmp' is usualy on tmpfs filesystem nowadays. Such a way can improve speed of building.

NOTICE:
If you changed the way of using 'buildsymlink' (added or removed) you should firstly
call command 'distclean' without any other WAF commands or remove old build directory
and symlink manually. It is because of some technical problem of using of WAF.
"""
buildroot    = os.path.join(tmpdir, username, 'projects', project['name'], 'build')
buildsymlink = os.path.join(project['root'], 'build')
# Variant without using of buildsymlink
#buildroot    = os.path.join(project['root'], 'build')

# root directory for all source files to compile
srcroot      = os.path.join(project['root'], 'src')

"""
Here is description of supported fields for project 'tasks'

'name' = {
    # String with WAF task generator features.
    # Useful values for C  : c cshlib cstlib cprogram
    # Useful values for C++: cxx cxxshlib cxxstlib cxxprogram
    # See WAF documention and examples for more details
    'features'

    # Source files for compiler. See details below.
    'sources'

    # Target name for building
    'target'

    # Include paths are used by the C/C++ compilers for finding headers. It can be list.
    'includes'

    # The attribute use enables the link against libraries (static or shared),
    # or the inclusion of object files. See https://waf.io/book for details
    'use'

    # List of names of system libraries as dependencies
    'sys-libs'

    # Optional paths to find system libs
    'sys-lib-path'

    # Optional list of paths to hard-code into the binary during linking time
    'rpath'

    # Enforce version numbering on shared libraries. It can be used with features
    # 'cshlib', 'cxxshlib', 'dshlib', 'fcshlib'
    'ver-num'

    # Default compiler flags, optional
    'cflags'
    'cxxflags'

    # List of flags added at the end of compilation commands
    'cppflags'

    # Default linker flags, optional
    'linkflags'

    # Default defines, optional
    'defines'

    # List of build type configs.
    # Each param in each build type here overrides any such a param from current
    # project if such a param exists.
    'buildtypes' = {
        # 'release-gcc', 'debug-clang', etc - these are just names, they can be any
        'release-gcc' = {
            'toolchain' : 'g++' # 'clang++', 'c++' (auto), ...
            'cxxflags'
            'linkflags'
            'defines'
        },
        'release-clang' = {
        },
        'release' : 'release-gcc', # alias

        # special alias for default build type
        'default' : 'release'
    }

    build types for parent project can be made with 2 ways:
    1) explicit declaration based on buildtypes of subprojects
    2) auto implicit declaration from all existing build types of subprojects
    The first way has no big problems but requires more details in config. The second has one
    question: what to do with unmatched build types?
}

For 'source' field it can be string with path or list of such strings or dict (dictionary).
Type 'dict' is used for ant_glob function. Format of patterns for ant_glob see 
on https://waf.io/book/. Many examples of patterns you also can find in waflib directory.
Such a dict can contain fields:
    'include'    # ant patterns or list of patterns to include, required field,
    'exclude'    # optional, ant patterns or list of patterns to exclude
    'ignorecase' # optional, ignore case while matching (False by default)

For string you can use such a form: 'main.c about.c'
Another way for the same result: ['main.c', 'about.c']

NOTICE:
Any path or pattern for 'source' should be relative to 'srcroot'
Paths for 'includes' should be relative to 'srcroot' or absolute. 
But last variant is not recommended.
"""

# It's just for suitable using and it isn't used by wscript
common = {
    'cxxflags' : '-std=c++14 -Wall -Wextra -Woverloaded-virtual'
                 ' -Wunreachable-code -Wvla',
    #'linkflags' : '-Wl,-rpath,. -Wl,--as-needed',
    'linkflags' : '-Wl,--as-needed',
    #'linkflags' : '',
}

# config of buildtypes, this var is used by wscript
buildtypes = {
    'debug-gcc' : {
        'toolchain' : 'g++',
        'cxxflags'  : common['cxxflags'] + ' -O0 -g -fno-omit-frame-pointer -fsanitize=address',
        'linkflags' : common['linkflags'] + ' -fsanitize=address',
    },
    'debug-clang' : {
        'toolchain' : 'clang++',
        'cxxflags'  : common['cxxflags'] + ' -O0 -g -fno-omit-frame-pointer -fsanitize=address',
        'linkflags' : common['linkflags'] + ' -fsanitize=address',
    },
    'release-gcc' : {
        'toolchain' : 'g++',
        'cxxflags'  : common['cxxflags'] + ' -O2',
        'linkflags' : common['linkflags'],
    },
    'release-clang' : {
        'toolchain' : 'clang++',
        'cxxflags'  : common['cxxflags'] + ' -O2',
        'linkflags' : common['linkflags'],
    },
    'debug'   : 'debug-clang',
    'release' : 'release-gcc',
    'default' : 'debug',
}

"""
buildtype by wildcard: release (build all release), gcc (build all gcc)

buildtypes = debug, release, fastdebug, ...
platforms = linux, windows, android, ..
toolchains = auto, gcc, g++, clang, clang++, msvc, ndk, ...

# In most cases you don't need to use this var.
# You can override built-in toolchains or add your own ones. 
toolchains = {
    'g++': {
        # here you can set/override env vars like 'CXX', 'LINK_CXX', ...
        'CXX'     : 'g++', 
        'LINK_CXX': 'g++',
        'AR'      : 'ar',
    },
}

# List of supported platforms with list of supported build types for each of them.
# You don't need this param if you build everything on one platform
platforms = {
    'linux'  : ['debug-gcc', 'debug-clang', 'release-gcc', 'release-clang' ],
    'windows': [],
}

for each system/platform check at least one possible buildtype/toolschain
"""

# config of tasks, this var is used by wscript
tasks = {
    'engine' : {
        'features'   : 'cxx cxxshlib',
        'source'     :  dict( include = 'engine/**/*.cpp' ),
        'target'     : 'jrm-engine',
        'includes'   : '.',
        'sys-libs'   : ['m', 'rt'],
        'ver-num'    : project['version'],
        # just example
        #'toolchain'  : 'g++',
        # defines     : ['LINUX=1', 'POSIX'],
    },
    'runner' : {
        'features'   : 'cxx cxxprogram',
        'source'     :  dict( include = 'runner/**/*.cpp' ),
        #'target'     : 'runner',
        'includes'   : '.',
        'use'        : 'engine',
        # just example
        #'buildtypes' : {
        #    'debug-clang' : {
        #        'cxxflags'  : common['cxxflags'] + ' -O1',
        #    },
        #},
    },
}

waf = dict(
    # Execute the configuration automatically, optional, 'True' by default
    autoconfig = True,
)
