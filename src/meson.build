# Build library first
subdir('template')

# Example executable: src/main.cpp
executable(
  'template',
  'main.cpp',
  dependencies: [template_dep],
  install: true,
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
