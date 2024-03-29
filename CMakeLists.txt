cmake_minimum_required(VERSION 3.17)
cmake_policy(SET CMP0074 NEW)

find_package(PythonInterp 3 REQUIRED)

set(GET_ARCH_CMD ${PYTHON_EXECUTABLE} "${CMAKE_SOURCE_DIR}/scripts/get_arch.py")
set(GET_DEPS_CMD ${PYTHON_EXECUTABLE} "${CMAKE_SOURCE_DIR}/scripts/get_deps.py")
set(APPLY_PATCHES_CMD ${PYTHON_EXECUTABLE} "-m" "patch")

message(STATUS "Executing get_arch.py")
execute_process(
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    COMMAND ${GET_ARCH_CMD}
    OUTPUT_VARIABLE PYRLOTTIE_COMPILE_TARGET
)
message(STATUS "Finished get_arch.py")
message(STATUS "PYRLOTTIE_COMPILE_TARGET is ${PYRLOTTIE_COMPILE_TARGET}")

message(STATUS "Executing get_deps.py")
execute_process(
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    COMMAND ${GET_DEPS_CMD}
)
message(STATUS "Finished get_deps.py")

file(GLOB PATCH_FILES "${CMAKE_SOURCE_DIR}/patches/*.patch")
foreach(PATCH_FILE ${PATCH_FILES})
    message(STATUS "Applying patch ${PATCH_FILE}")
    execute_process(
        WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
        COMMAND ${APPLY_PATCHES_CMD} ${PATCH_FILE}
        COMMAND_ERROR_IS_FATAL ANY
    )
    message(STATUS "Finished applying patch ${PATCH_FILE}")
endforeach()

if (MSVC)
    set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")
    set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} /MT")
    set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} /MTd")
    set(CMAKE_CXX_FLAGS_RELWITHDEBINFO "${CMAKE_CXX_FLAGS_RELWITHDEBINFO} /Zi /Ob0 /Od /RTC1")
elseif (LINUX)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC")
elseif (APPLE)
    if("${PYRLOTTIE_COMPILE_TARGET}" STREQUAL "armv8")
        set(CMAKE_OSX_DEPLOYMENT_TARGET "11.0")
    else()
        set(CMAKE_OSX_DEPLOYMENT_TARGET "10.9")
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++0x -stdlib=libc++")
    endif()
endif()

set(BUILD_SHARED_LIBS OFF)
set(ZLIB_USE_STATIC_LIBS ON)
set(PNG_USE_STATIC_LIBS ON)

# Add conan packages
set(CONAN_ROOT ${CMAKE_SOURCE_DIR}/conan_output/${PYRLOTTIE_COMPILE_TARGET})
set(CONAN_TOOLCHAIN "${CONAN_ROOT}/conan_toolchain.cmake")

if (EXISTS ${CONAN_TOOLCHAIN})
    include(${CONAN_TOOLCHAIN})
else()
    message(FATAL_ERROR "The conan_toolchain file could not be found: ${CONAN_TOOLCHAIN}")
endif()

project(pyrlottie)

add_subdirectory(libwebp)
add_subdirectory(rlottie)

# Install the module
install(TARGETS lottie2gif gif2webp
        EXCLUDE_FROM_ALL
        RUNTIME DESTINATION ${PY_BUILD_CMAKE_MODULE_NAME}
        COMPONENT python_module)