project(
  'template',
  'cpp',
  meson_version: '>= 1.3.0',
  version: '0.1',
  default_options: ['warning_level=3', 'cpp_std=c++23'],
)

inc = include_directories(include)

### Project Library ###

libtemplate = library(
  'libtemplate',
  'src/template/*.cpp',
  include_directories: inc,
)

libtemplate_dep = declare_dependency(
  link_with: libtemplate,
  include_directories: inc,
)

sources = [
  'template.cpp',
]

### Executables ###

exe = executable(
  'template',
  sources,
  include_directories: inc,
  dependencies: dependencies,
)

### Tests ###

test_exe = executable(
  'test',
  [],
  include_directories: inc,
  dependencies: [dependency(doctest)],
)

test('basic', test_exe)
