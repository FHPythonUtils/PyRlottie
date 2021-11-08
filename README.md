[![GitHub top language](https://img.shields.io/github/languages/top/FHPythonUtils/PyRlottie.svg?style=for-the-badge)](../../)
[![Repository size](https://img.shields.io/github/repo-size/FHPythonUtils/PyRlottie.svg?style=for-the-badge)](../../)
[![Issues](https://img.shields.io/github/issues/FHPythonUtils/PyRlottie.svg?style=for-the-badge)](../../issues)
[![License](https://img.shields.io/github/license/FHPythonUtils/PyRlottie.svg?style=for-the-badge)](/LICENSE.md)
[![Commit activity](https://img.shields.io/github/commit-activity/m/FHPythonUtils/PyRlottie.svg?style=for-the-badge)](../../commits/master)
[![Last commit](https://img.shields.io/github/last-commit/FHPythonUtils/PyRlottie.svg?style=for-the-badge)](../../commits/master)
[![PyPI Downloads](https://img.shields.io/pypi/dm/pyrlottie.svg?style=for-the-badge)](https://pypistats.org/packages/pyrlottie)
[![PyPI Total Downloads](https://img.shields.io/badge/dynamic/json?style=for-the-badge&label=total%20downloads&query=%24.total_downloads&url=https%3A%2F%2Fapi.pepy.tech%2Fapi%2Fprojects%2Fpyrlottie)](https://pepy.tech/project/pyrlottie)
[![PyPI Version](https://img.shields.io/pypi/v/pyrlottie.svg?style=for-the-badge)](https://pypi.org/project/pyrlottie)

<!-- omit in TOC -->
# PyRlottie

<img src="readme-assets/icons/name.png" alt="Project Icon" width="750">

Convert .tgs and .lottie to .webp or .gif using rlottie.

- [Formats](#formats)
- [Basic Usage](#basic-usage)
- [Documentation](#documentation)
- [Supported Environments (64bit)](#supported-environments-64bit)
- [Install With PIP](#install-with-pip)
	- [WSL](#wsl)
- [Language information](#language-information)
	- [Built for](#built-for)
- [Install Python on Windows](#install-python-on-windows)
	- [Chocolatey](#chocolatey)
	- [Windows - Python.org](#windows---pythonorg)
- [Install Python on Linux](#install-python-on-linux)
	- [Apt](#apt)
	- [Dnf](#dnf)
- [Install Python on MacOS](#install-python-on-macos)
	- [Homebrew](#homebrew)
	- [MacOS - Python.org](#macos---pythonorg)
- [How to run](#how-to-run)
	- [Windows](#windows)
	- [Linux/ MacOS](#linux-macos)
- [Download Project](#download-project)
	- [Clone](#clone)
		- [Using The Command Line](#using-the-command-line)
		- [Using GitHub Desktop](#using-github-desktop)
	- [Download Zip File](#download-zip-file)
- [Community Files](#community-files)
	- [Licence](#licence)
	- [Changelog](#changelog)
	- [Code of Conduct](#code-of-conduct)
	- [Contributing](#contributing)
	- [Security](#security)
	- [Support](#support)
	- [Rationale](#rationale)

## Formats

convMultLottie, convSingleLottie
| Format | Animated |
| ------ | -------- |
| .gif   | ✔        |
| .webp  | ✔        |

convMultLottieFrames,
convMultLottieTransparentFrames,
convSingleLottieFrames,
convSingleLottieTransparentFrames,
| Format | Animated |
| ------ | -------- |
| .gif   | ✔        |
| .webp  | ✔        |
| .apng  | ✔        |
| .png   | :x:      |
| .jpg   | :x:      |
| etc... | ...      |

https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html

## Basic Usage

Convert multiple tgs files to webp

```py
# convMultLottie
print(
	run(
		convMultLottie(
			[
				FileMap(LottieFile(f"test_data/file_43{i}.tgs"), {f"test_data/file_43{i}.webp"})
				for i in range(4, 10)
			]
		)
	)
)
```

Convert multiple tgs files to transparent frames dictionary of lottie file paths
to LottieFrames. The list of pillow images can be accessed with .frames for each
lottie file path

```py
frames = run(
	convMultLottieTransparentFrames(
		[LottieFile(f"test_data/file_43{i}.tgs") for i in range(4, 10)], 1
	)
)["test_data/file_434.tgs"].frames

```

## Documentation
See the [Docs](/DOCS/) for more information.

## Supported Environments (64bit)

| Environment | Supported |
| ----------- | --------- |
|linux_x86_64 | ✔         |
|linux_aarch64| :x:       |
|windows_amd64| ✔         |
|darwin_x86_64| :x:       |
|darwin_arm64 | :x:       |

For a full list of machine architecures for Linux see https://stackoverflow.com/questions/45125516/possible-values-for-uname-m

## Install With PIP

```cmd
pip install pyrlottie
```

### WSL
Need to preserve execute bits

```cmd
mkdir pip-tmp
TMPDIR='./pip-tmp' pip install pyrlottie && rmdir pip-tmp
```

https://github.com/pypa/pip/issues/7666
https://github.com/pypa/pip/issues/6364

Head to https://pypi.org/project/pyrlottie/ for more info

## Language information

### Built for
This program has been written for Python versions 3.7 - 3.10 and has been tested with both 3.7 and
3.10

## Install Python on Windows

### Chocolatey

```powershell
choco install python
```

### Windows - Python.org
To install Python, go to https://www.python.org/downloads/windows/ and download the latest
version.

## Install Python on Linux

### Apt

```bash
sudo apt install python3.x
```

### Dnf

```bash
sudo dnf install python3.x
```

## Install Python on MacOS

### Homebrew

```bash
brew install python@3.x
```

### MacOS - Python.org
To install Python, go to https://www.python.org/downloads/macos/ and download the latest
version.

## How to run

### Windows

- Module
	`py -3.x -m [module]` or `[module]` (if module installs a script)

- File
	`py -3.x [file]` or `./[file]`

### Linux/ MacOS

- Module
	`python3.x -m [module]` or `[module]` (if module installs a script)

- File
	`python3.x [file]` or `./[file]`

## Download Project

### Clone

#### Using The Command Line

1. Press the Clone or download button in the top right
2. Copy the URL (link)
3. Open the command line and change directory to where you wish to
clone to
4. Type 'git clone' followed by URL in step 2

	```bash
	git clone https://github.com/FHPythonUtils/PyRlottie
	```

More information can be found at
https://help.github.com/en/articles/cloning-a-repository

#### Using GitHub Desktop

1. Press the Clone or download button in the top right
2. Click open in desktop
3. Choose the path for where you want and click Clone

More information can be found at
https://help.github.com/en/desktop/contributing-to-projects/cloning-a-repository-from-github-to-github-desktop

### Download Zip File

1. Download this GitHub repository
2. Extract the zip archive
3. Copy/ move to the desired location

## Community Files

### Licence
MIT License
Copyright (c) FredHappyface
(See the [LICENSE](/LICENSE.md) for more information.)

### Changelog
See the [Changelog](/CHANGELOG.md) for more information.

### Code of Conduct
Online communities include people from many backgrounds. The *Project*
contributors are committed to providing a friendly, safe and welcoming
environment for all. Please see the
[Code of Conduct](https://github.com/FHPythonUtils/.github/blob/master/CODE_OF_CONDUCT.md)
 for more information.

### Contributing
Contributions are welcome, please see the
[Contributing Guidelines](https://github.com/FHPythonUtils/.github/blob/master/CONTRIBUTING.md)
for more information.

### Security
Thank you for improving the security of the project, please see the
[Security Policy](https://github.com/FHPythonUtils/.github/blob/master/SECURITY.md)
for more information.

### Support
Thank you for using this project, I hope it is of use to you. Please be aware that
those involved with the project often do so for fun along with other commitments
(such as work, family, etc). Please see the
[Support Policy](https://github.com/FHPythonUtils/.github/blob/master/SUPPORT.md)
for more information.

### Rationale
The rationale acts as a guide to various processes regarding projects such as
the versioning scheme and the programming styles used. Please see the
[Rationale](https://github.com/FHPythonUtils/.github/blob/master/RATIONALE.md)
for more information.
