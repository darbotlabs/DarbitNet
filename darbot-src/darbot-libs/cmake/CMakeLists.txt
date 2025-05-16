cmake_minimum_required(VERSION 3.14)
project("darbot-libs" C CXX)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

if (NOT XCODE AND NOT MSVC AND NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
    set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

set(CMAKE_CXX_STANDARD_REQUIRED true)
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED true)
set(THREADS_PREFER_PTHREAD_FLAG ON)

find_package(Threads REQUIRED)

add_subdirectory(bin)
add_subdirectory(include)
add_subdirectory(lib)
add_subdirectory(scripts)
add_subdirectory(docs)
add_subdirectory(licenses)

install(DIRECTORY bin/ DESTINATION ${CMAKE_INSTALL_BINDIR})
install(DIRECTORY include/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
install(DIRECTORY lib/ DESTINATION ${CMAKE_INSTALL_LIBDIR})
install(DIRECTORY scripts/ DESTINATION ${CMAKE_INSTALL_BINDIR})
install(DIRECTORY docs/ DESTINATION ${CMAKE_INSTALL_DOCDIR})
install(DIRECTORY licenses/ DESTINATION ${CMAKE_INSTALL_DOCDIR})
