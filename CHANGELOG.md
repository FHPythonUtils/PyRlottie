# Changelog
All major and minor version changes will be documented in this file. Details of
patch-level version changes can be found in [commit messages](../../commits/master).

## 2021.1.1 - 2021/10/14

- Use pre-commit to enforce reasonable standards + consistency
- Update readme with improved docs on installing and running python (fairly generic)
- Remove classifiers for license + python versions and rely on poetry to generate these
- Update tooling config (pyproject.toml)

## 2021.1 - 2021/10/03

- Throw an `OSError` if the user's environment is unsupported rather than exit
- Use `asyncio.Semaphore` to limit the number of processes spawned to
  `multiprocessing.cpu_count() * 2` (previously unlimited)
  - However, this breaks `asyncio.run(convMethod)`

	```md
	Use `pyrlottie.run(convMethod)` or `asyncio.get_event_loop().run_until_complete(convMethod)`
	in place of `asyncio.run(convMethod)`

	See https://github.com/awestlake87/pyo3-asyncio/issues/19#issuecomment-846686814
	for more information

	Run until the future (an instance of Future) has completed.

	If the argument is a coroutine object it is implicitly scheduled to run as a asyncio.Task.

	Return the Future’s result or raise its exception.

	Args:
		convMethod (Awaitable): Awaitable to run. eg.
		convSingleLottie(gLottieFile, destFiles={"test_data/convSingleLottie.webp"})

	Returns:
		Any: the Awaitable's result or raise its exception.
	```

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
