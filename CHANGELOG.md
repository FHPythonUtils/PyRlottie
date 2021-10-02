# Changelog
All major and minor version changes will be documented in this file. Details of
patch-level version changes can be found in [commit messages](../../commits/master).

## 2021.0.3 - 2021/10/02

- build rlottie as a static object (lottie2gif)

	```bash
	$ ./lottie2gif_old
	./lottie2gif_old: error while loading shared libraries: librlottie.so.0: cannot open shared object file: No such file or directory
	$ ./lottie2gif
	Usage:
	lottie2gif [lottieFileName] [Resolution] [bgColor]
	```

- add documentation to preserve x bit for binaries when pip installing in wsl

## 2021.0.2 - 2021/10/02

- bugfix to scaling function

## 2021.0.1 - 2021/10/02

- minor bugfixes
- more verbose errors
- hopefully dll is included for windows

## 2021 - 2021/10/02

- First release. Significant speed and quality improvements over pylottie (between 1.5x and 5x in most cases)
