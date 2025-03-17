include(FetchContent)

cmake_minimum_required(VERSION 3.22)
project(project_template
        VERSION 0.0.1
        LANGUAGES CXX
)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_DEBUG ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE ${CMAKE_SOURCE_DIR}/bin)

# Matplot++ added as an existing source.
add_subdirectory(lib/matplotplusplus)

# Catch2 added directly into the build folder.
find_package(Catch2 3)
if (NOT Catch2_FOUND)
    FetchContent_Declare(
            Catch2
            GIT_REPOSITORY https://github.com/catchorg/Catch2.git
            GIT_TAG v3.5.2)
    FetchContent_MakeAvailable(Catch2)
endif ()

# Add `common` library.
add_library(common STATIC src/lib/common/util.cpp)
target_include_directories(common PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
target_link_libraries(common PUBLIC matplot)
target_compile_options(common PRIVATE
        "$<$<CONFIG:Debug>:-O0;-g3;-Wall;-Wextra>"
        "$<$<CONFIG:Release>:-O3>"
)  # Probably change this...

# Add `phm` executable.
add_executable(phm src/pmacro.cpp src/pmacro/parser.cpp)
target_include_directories(phm PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/include)
target_link_libraries(phm PRIVATE common)
target_compile_options(phm PRIVATE
        "$<$<CONFIG:Debug>:-O0;-g3;-Wall;-Wextra>"
        "$<$<CONFIG:Release>:-O3>"
)

# Add `test_phm` executable.
add_executable(test_phm test/src/test_phm.cpp test/src/test_util.cpp)
target_include_directories(test_phm PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/test/include)
target_link_libraries(test_phm PRIVATE common Catch2::Catch2WithMain)
target_compile_options(test_phm PRIVATE -Og -Wall -Wextra)
