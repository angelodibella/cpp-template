#include <doctest.h>

#include <template/template.hpp>

TEST_CASE("add works") { CHECK(template_::add(2, 3) == 5); }
