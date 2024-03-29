#!/usr/bin/env python3
import os
import platform
import sys

conan_archs = {
    "x86_64": ["amd64", "x86_64", "x64"],
    "x86": ["i386", "i686", "x86"],
    "armv8": ["arm64", "aarch64", "aarch64_be", "armv8b", "armv8l"],
    "ppc64le": ["ppc64le", "powerpc"],
    "s390x": ["s390", "s390x"],
}


def get_native_arch() -> str:
    for k, v in conan_archs.items():
        if platform.machine().lower() in v:
            return k

    # Failover
    return platform.machine().lower()


def get_arch() -> str:
    arch_env = os.getenv("PYRLOTTIE_COMPILE_TARGET")
    if isinstance(arch_env, str):
        arch = arch_env
    else:
        arch = get_native_arch()

    return arch


def main():
    arch = get_arch()
    sys.stdout.write(arch)


if __name__ == "__main__":
    main()