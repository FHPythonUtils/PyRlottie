#!/usr/bin/env python3
import os
import platform
import shutil
import subprocess
import sys
from typing import List

from get_arch import conan_archs, get_arch, get_native_arch  # type: ignore


def install_deps(arch: str):
    # Use Conan to install dependencies
    settings: List[str] = []
    build: List[str] = []

    if platform.system() == "Windows":
        settings.append("os=Windows")
        if sys.platform.startswith(("cygwin", "msys")):
            # Need python headers and libraries, but msvc not able to find them
            # If inside cygwin or msys.
            settings.append("compiler=gcc")
            settings.append("compiler.version=10")
            settings.append("compiler.libcxx=libstdc++")
        else:
            settings.append("compiler=msvc")
            settings.append("compiler.runtime=static")
    elif platform.system() == "Darwin":
        settings.append("os=Macos")
        if arch == "armv8":
            settings.append("os.version=11.0")
        else:
            settings.append("os.version=10.9")
        settings.append("compiler=apple-clang")
        settings.append("compiler.libcxx=libc++")
    elif platform.system() == "Linux":
        settings.append("os=Linux")
        settings.append("compiler=gcc")
        settings.append("compiler.version=10")
        settings.append("compiler.libcxx=libstdc++")
    if arch:
        settings.append("arch=" + arch)
    
    if platform.system() == "Linux":
        # Need to compile dependencies if Linux
        build.append("*")
    elif not shutil.which("cmake") and (
        platform.architecture()[0] == "32bit"
        or platform.machine().lower() not in (conan_archs["armv8"] + conan_archs["x86"])
    ):
        build.append("cmake*")

    if build == []:
        build.append("missing")

    print("conan cli settings:")
    print("settings: " + str(settings))
    print("build: " + str(build))

    subprocess.run(["conan", "profile", "detect", "-f"])

    conan_output = os.path.join("conan_output", arch)

    subprocess.run(
        [
            "conan",
            "install",
            *[x for s in settings for x in ("-s", s)],
            *[x for b in build for x in ("-b", b)],
            "-of",
            conan_output,
            "--deployer=direct_deploy",
            ".",
        ]
    )

    return conan_output


def main():
    arch = get_arch()
    install_deps(arch)


if __name__ == "__main__":
    main()