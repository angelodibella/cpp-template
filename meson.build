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

subdir('src')
subdir('tests')
subdir('docs')
