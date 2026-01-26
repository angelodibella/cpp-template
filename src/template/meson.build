template_lib_sources = files(
  'template.cpp',
)

libtemplate = static_library(
  'template',
  template_lib_sources,
  include_directories: template_inc,
  dependencies: [openmp_dep],
)

template_dep = declare_dependency(
  link_with: libtemplate,
  include_directories: template_inc,
  dependencies: [openmp_dep],
)
