doctest_dep = dependency(
  'doctest',
  required: get_option('tests'),
  fallback: ['doctest', 'doctest_dep'],
)

test_exe = executable(
  'template_tests',
  'test_template.cpp',
  dependencies: [template_dep, doctest_dep],
)

test('unit', test_exe)
