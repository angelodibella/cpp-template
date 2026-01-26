template_lib_sources = files(
  'template.cpp',
)

libtemplate = library(
  'template',
  template_lib_sources,
  include_directories: template_inc,
  dependencies: [openmp_dep],
  install: true,
  version: meson.project_version(),
  soversion: '0',
)

template_dep = declare_dependency(
  link_with: libtemplate,
  include_directories: template_inc,
  dependencies: [openmp_dep],
)
