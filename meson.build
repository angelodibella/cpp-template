project(
  'template',
  'cpp',
  meson_version: '>= 1.3.0',
  version: '0.1',
  default_options: ['warning_level=3', 'cpp_std=c++23'],
)

dependencies = []

sources = [
  'template.cpp',
]

inc = include_directories(include)

exe = executable(
  'template',
  sources,
  include_directories: inc,
  dependencies: dependencies,
  install: true,
)

test('basic', exe)
