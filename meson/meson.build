
project('just.remind.me', 'cpp')

compiler = meson.get_compiler('cpp')

incdir = include_directories('../src')

deps = []
deps += dependency('threads')
deps += compiler.find_library('m')

c = run_command('get_sources.sh', 'engine')
sources = c.stdout().strip().split('\n')
engine_lib = shared_library('jrm-engine', sources, include_directories : incdir,
    version : '0.0.0', soversion : '0')

c = run_command('get_sources.sh', 'runner')
sources = c.stdout().strip().split('\n')
#sources = ['../src/runner/main.cpp', '../src/runner/application.cpp']

deps = []
executable('just.remind.me', sources, include_directories : incdir,
    dependencies : deps, link_with : engine_lib)
