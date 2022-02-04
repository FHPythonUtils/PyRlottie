# Minimum version of CMake required to build this project
cmake_minimum_required(VERSION 3.0)

# Name of the project
project(lottie2img)

if (WIN32 AND NOT BUILD_SHARED_LIBS)
    set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} /MDd")
    set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} /MDd")
endif()

add_subdirectory("libraries/libwebp")
add_subdirectory("libraries/rlottie")
add_subdirectory("src")
