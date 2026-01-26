project(
  'template',
  'cpp',
  version: '0.1.0',
  meson_version: '>= 1.3.0',
  default_options: [
    'cpp_std=c++23',
    'warning_level=3',
    'buildtype=debug',
    'b_ndebug=if-release',
  ],
)

template_inc = include_directories('include')

openmp_dep = dependency('openmp')

# Build library
subdir('src/template')

# Example executable: src/main.cpp
executable(
  'template',
  'src/main.cpp',
  dependencies: [template_dep],
)

# If you have internal modules:
#
# subdir('foo')  # builds something like foo_dep
#
#
# Then executables can depend on both:
#
# executable(
#   'template2',
#   'other_main.cpp',
#   dependencies: [template_dep, foo_dep],
# )

subdir('tests')
subdir('docs')
