# Build Steps

- [Build Steps](#build-steps)
	- [linux](#linux)
		- [linux_x86_64 (optional)](#linux_x86_64-optional)
		- [linux_aarch64](#linux_aarch64)
	- [windows](#windows)
		- [windows_amd64](#windows_amd64)
		- [windows_arm64](#windows_arm64)

https://storage.googleapis.com/downloads.webmproject.org/releases/webp/index.html

https://chromium.googlesource.com/webm/libwebp/+/8ea81561d2fdd382da60f57958741a7c23a18eb6

```txt
linux_x86_64  libwebp-1.2.1-linux-x86-64.tar.gz
linux_aarch64 (see linux_aarch64)
windows_amd64 libwebp-1.2.1-windows-x64.zip
windows_arm64
darwin_x86_64 libwebp-1.2.1-mac-10.15.tar.gz
darwin_arm64
```

## linux

### linux_x86_64 (optional)

Requirements:
OS: x86_64 GNU/Linux eg WSL Ubuntu

- cmake
- gcc
- g++
- libgif-dev (gif2webp)

```cmd
cmake -Bbuild_linux_x86_64 -DBUILD_SHARED_LIBS=OFF
cmake --build build_linux_x86_64
-> build_linux_x86_64/gif2webp
```

### linux_aarch64

Requirements:
OS: x86_64 GNU/Linux eg WSL Ubuntu

- cmake
- gcc-aarch64-linux-gnu
- binutils-aarch64-linux-gnu
- g++-aarch64-linux-gnu
- libgif-dev:arm64 (gif2webp)

`sudo vim /etc/apt/sources.list.d/arm-cross-compile-sources.list`

```dpkg
deb [arch=armhf,arm64] http://ports.ubuntu.com/ focal main restricted
deb [arch=armhf,arm64] http://ports.ubuntu.com/ focal-updates main restricted
deb [arch=armhf,arm64] http://ports.ubuntu.com/ focal universe
deb [arch=armhf,arm64] http://ports.ubuntu.com/ focal-updates universe
deb [arch=armhf,arm64] http://ports.ubuntu.com/ focal multiverse
deb [arch=armhf,arm64] http://ports.ubuntu.com/ focal-updates multiverse
deb [arch=armhf,arm64] http://ports.ubuntu.com/ focal-backports main restricted universe multiverse
```

```cmd
sudo dpkg --add-architecture arm64
sudo apt install libgif-dev:arm64
```

```cmd
cmake -Bbuild_linux_aarch64 -DBUILD_SHARED_LIBS=OFF -DCMAKE_C_COMPILER=aarch64-linux-gnu-gcc -DCMAKE_CXX_COMPILER=aarch64-linux-gnu-g++
cmake --build build_linux_aarch64
-> build_linux_aarch64/gif2webp
```

## windows

### windows_amd64

Requirements
OS: Windows 10 amd64

- Visual Studio 16 2019
- cmake

### windows_arm64

Requirements
OS: Windows 10 amd64

- Visual Studio 16 2019 + Desktop Dev with C++ Build tools Arm64
- cmake
