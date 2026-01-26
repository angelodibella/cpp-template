#include <doctest/doctest.h>
#include <template/template.hpp>

TEST_CASE("add works") {
  CHECK(template_lib::add(2, 3) == 5);
}
