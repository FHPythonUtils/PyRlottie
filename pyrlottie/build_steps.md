# Build Steps

- [Build Steps](#build-steps)
	- [linux](#linux)
		- [linux_x86_64](#linux_x86_64)
		- [linux_aarch64](#linux_aarch64)
	- [windows](#windows)
		- [windows_amd64](#windows_amd64)
		- [windows_arm64](#windows_arm64)

## linux

### linux_x86_64

Requirements:
OS: x86_64 GNU/Linux eg WSL Ubuntu

- cmake
- gcc
- g++

```cmd
cmake -Bbuild_linux_x86_64 -DBUILD_SHARED_LIBS=OFF
cmake --build build_linux_x86_64
-> build_linux_x86_64/example/lottie2gif
```

### linux_aarch64

Requirements:
OS: x86_64 GNU/Linux eg WSL Ubuntu

- cmake
- gcc-aarch64-linux-gnu
- binutils-aarch64-linux-gnu
- g++-aarch64-linux-gnu

```cmd
cmake -Bbuild_linux_aarch64 -DBUILD_SHARED_LIBS=OFF -DCMAKE_C_COMPILER=aarch64-linux-gnu-gcc -DCMAKE_CXX_COMPILER=aarch64-linux-gnu-g++
cmake --build build_linux_aarch64
-> build_linux_aarch64/example/lottie2gif
```

## windows

### windows_amd64

Requirements
OS: Windows 10 amd64

- Visual Studio 16 2019
- cmake

```cmd
cmake -Bbuild_windows_amd64 -DBUILD_SHARED_LIBS=OFF
cmake --build build_windows_amd64
-> build_windows_amd64\example\Debug\lottie2gif.exe
```

### windows_arm64

Requirements
OS: Windows 10 amd64

- Visual Studio 16 2019 + Desktop Dev with C++ Build tools Arm64
- cmake

```cmd
cmake -Bbuild_windows_arm64 -DBUILD_SHARED_LIBS=OFF -AARM64
cmake --build build_windows_arm64
-> build_windows_arm64\example\Debug\lottie2gif.exe
```
