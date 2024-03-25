#!/usr/bin/env python3
# type: ignore
import shutil

from conan import ConanFile
from conan.tools.cmake import CMakeDeps, CMakeToolchain


class PyrlottieRecipe(ConanFile):
    settings = "os", "compiler", "build_type", "arch"

    def requirements(self):
        self.requires("giflib/5.2.1")
        self.requires("libpng/1.6.43")
        self.requires("zlib/1.3.1")
        self.requires("libjpeg/9e")

    def build_requirements(self):
        if not shutil.which("cmake"):
            self.tool_requires("cmake/[>=3.27]")

    def build(self):
        build_type = "Release"  # noqa: F841

    def generate(self):
        tc = CMakeToolchain(self)
        cmake = CMakeDeps(self)
        tc.generate()
        cmake.generate()