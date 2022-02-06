# Build Steps

- [Build Steps](#build-steps)
	- [Linux (Ubuntu 20.04)](#linux-ubuntu-2004)
	- [linux_x86_64](#linux_x86_64)
	- [linux_aarch64](#linux_aarch64)
	- [windows](#windows)
		- [windows_amd64](#windows_amd64)
		- [windows_arm64](#windows_arm64)

## Linux (Ubuntu 20.04)

Use vagrant (`$Env:VAGRANT_VAGRANTFILE='Vagrantfile_linux.rb'; vagrant up`) or
set up an Ubuntu machine/ vm with the following tools installed listed in each
section. These instructions are for x86_64 Ubuntu 20.04

## linux_x86_64

Requirements: x86_64 Ubuntu 20.04

- cmake
- gcc
- g++
- libgif-dev

```sh
cmake -Bbuild_linux_x86_64 -DBUILD_SHARED_LIBS=OFF
cmake --build build_linux_x86_64
-> build_linux_x86_64/gif2webp
```

## linux_aarch64

Requirements: x86_64 Ubuntu 20.04

- cmake
- gcc-aarch64-linux-gnu
- binutils-aarch64-linux-gnu
- g++-aarch64-linux-gnu
- libgif-dev:arm64

`sudo vim /etc/apt/sources.list.d/arm-cross-compile-sources.list`

```dpkg
deb [arch=arm64] http://ports.ubuntu.com/ focal main restricted
deb [arch=arm64] http://ports.ubuntu.com/ focal-updates main restricted
deb [arch=arm64] http://ports.ubuntu.com/ focal universe
deb [arch=arm64] http://ports.ubuntu.com/ focal-updates universe
deb [arch=arm64] http://ports.ubuntu.com/ focal multiverse
deb [arch=arm64] http://ports.ubuntu.com/ focal-updates multiverse
deb [arch=arm64] http://ports.ubuntu.com/ focal-backports main restricted universe multiverse
```

```sh
sudo dpkg --add-architecture arm64
sudo apt install libgif-dev:arm64
```

```sh
cmake -Bbuild_linux_aarch64 -DBUILD_SHARED_LIBS=OFF -DCMAKE_C_COMPILER=aarch64-linux-gnu-gcc -DCMAKE_CXX_COMPILER=aarch64-linux-gnu-g++
cmake --build build_linux_aarch64
-> build_linux_aarch64/gif2webp
```

## windows

### windows_amd64

Requirements: amd64 Windows 10

- Visual Studio 16 2019
- cmake

```sh
cmake -Bbuild_windows_amd64 -DBUILD_SHARED_LIBS=OFF
cmake --build build_windows_amd64 --config Release
-> build_windows_amd64\src\Release\lottie2img.exe
```

### windows_arm64

Requirements: amd64 Windows 10

- Visual Studio 16 2019 + Desktop Dev with C++ Build tools Arm64
- cmake

```sh
cmake -Bbuild_windows_arm64 -DBUILD_SHARED_LIBS=OFF -AARM64
cmake --build build_windows_arm64 --config Release
-> build_windows_arm64\src\Release\lottie2img.exe
```
