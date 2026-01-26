doxygen = find_program('doxygen', required: get_option('docs'))

if doxygen.found()
  c = configuration_data()
  c.set('PROJECT_NAME', meson.project_name())
  c.set('PROJECT_VERSION', meson.project_version())
  c.set('SRC_DIR', meson.project_source_root())
  c.set('BUILD_DIR', meson.project_build_root())

  doxyfile = configure_file(
    input: 'Doxyfile.in',
    output: 'Doxyfile',
    configuration: c,
  )

  run_target(
    'docs',
    command: [doxygen, doxyfile],
  )
endif
