#include <iostream>
#include <template/template.hpp>

auto main() -> int {
    std::cout << template_::add(2, 3) << "\n";
    return 0;
}
