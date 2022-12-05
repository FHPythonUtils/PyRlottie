"""Convert .tgs and .lottie to .webp or .gif using rlottie.

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
"""
from __future__ import annotations

import asyncio
import gzip
import json
import multiprocessing
import os
import platform
import shutil
import subprocess
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Awaitable, cast

import attr
import numpy as np
from PIL import Image

# pylint: disable=too-few-public-methods

THISDIR = str(Path(__file__).resolve().parent)
SEM = asyncio.Semaphore(multiprocessing.cpu_count())


@attr.s
class LottieFile:
	"""LottieFile. Load a lottie/tgs has a path and data (json/dict).

	Args:
		path (str): path to the lottie file
		data (dict): python dict representing the json data. Default=None (file is read)

	Raises:
		ValueError: Failure to parse the lottiefile json
	"""

	path: str = attr.ib()
	data: dict = attr.ib(default=None)

	def __attrs_post_init__(self) -> None:
		"""LottieFile __attrs_post_init__ called by attrs.

		Args:
			path (str): path to the lottie file
			data (dict): python dict representing the json data. Default=None (file is read)

		Raises:
			ValueError: Failure to parse the lottiefile json
		"""
		if self.data is not None:
			return
		try:
			archive = gzip.open(self.path, "rb")
			data = json.load(archive)
			# Update path for lottie2gif
			with NamedTemporaryFile(suffix=".json") as namedTemporaryFile:
				self.path = namedTemporaryFile.name
			Path(self.path).write_text(json.dumps(data), encoding="utf-8")
			archive.close()
		except ValueError as error:
			raise error
		except OSError:
			try:
				data = json.loads(Path(self.path).read_text(encoding="utf-8"))
			except ValueError as error:
				raise error
		self.data = cast(dict, data)


@attr.s
class FileMap:
	"""FileMap. Map a LottieFile to a set of destination/output files.

	Args:
		lottieFile (LottieFile): lottie file
		destFiles (set[str]): set of destination/output files. Default={"out.gif"}
	"""

	lottieFile: LottieFile = attr.ib()
	destFiles: set[str] = attr.ib(default={"out.gif"})


@attr.s
class LottieFrames:
	"""LottieFrames. Dataclass to hold info on lottieframes with LottieFile.data
	and a list of PIL.Image.Image(s) containing frame data.

	Args:
		data (LottieFile): LottieFile.data
		frames (list[Image.Image]): list of PIL.Image.Image(s) containing frame data
	"""

	data: dict = attr.ib()
	frames: list[Image.Image] = attr.ib()


async def _execSubprocess(command: str) -> tuple[int, bytes]:
	"""Execute a command and check for errors.

	Args:
		command (str): commands as a string

	Returns:
		tuple[int, bytes]: tuple of return code (int) and stdout (str)
	"""
	async with SEM:
		process = await asyncio.create_subprocess_shell(
			command,
			stdout=subprocess.PIPE,
			stderr=subprocess.STDOUT,
		)
		out = await process.communicate()
		exitCode = process.returncode
		return exitCode, out[0]  # type: ignore


def _getBinDir() -> str:
	"""Get the binary dir using the current environment (platform.system(), platform.machine()).

	Raises:
		OSError: if the user's environment is not supported

	Returns:
		str: binDir - the binary dir
	"""
	system = platform.system()
	machine = platform.machine()
	binDir = f"{THISDIR}/{system.lower()}_{machine.lower()}"
	if Path(binDir).exists():
		return binDir
	raise OSError(f"Sorry, your environment is not currently supported! {system=} {machine=}")


def _scale(dimen: str, scale: float = 1) -> int | str:
	"""Get a scaled dimen.

	Args:
		dimen (str): dimension in px
		scale (float): scale

	Returns:
		Optional[int, str]: scaled dimen (min=1)
	"""
	if scale == 1:
		return dimen
	return max(int(int(dimen) * scale), 1)


def _getTransparency(image1: np.ndarray, image2: np.ndarray) -> np.ndarray:
	"""Get the transparent pixels from an image with a red bg and an image with a black bg.

	Args:
		background (np.ndarray): image1 (the red image)
		foreground (np.ndarray): image2 (the black image)

	Returns:
		np.ndarray: pixels for the transparent image
	"""
	return np.where(
		image1[:, :, 0:1] - image2[:, :, 0:1] > 128,
		np.dstack(
			(
				image1[:, :, 0:3],
				np.zeros([len(image1[0, :, :]), len(image1[:, 0, :]), 1], dtype=np.uint8),
			)
		),
		image1,
	)


def run(convMethod: Awaitable) -> Any:
	"""Use `pyrlottie.run(convMethod)` or `asyncio.get_event_loop().run_until_complete(convMethod)`
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
	"""
	return asyncio.get_event_loop().run_until_complete(convMethod)


async def convMultLottieTransparentFrames(
	lottieFiles: list[LottieFile],
	frameSkip: int = 0,
	scale: float = 1,
) -> dict[str, LottieFrames]:
	"""Convert multiple lottie files to a dictionary of LottieFile.path to
	LottieFrames (LottieFile.data and a list of PIL.Image.Image frames) with
	transparency.

	Args:
		lottieFiles (list[LottieFile]): the lottie file to convert to frames
		frameSkip (int, optional): skip n number of frames in the interest of
		optimisation with a quality trade-off. Defaults to 0.
		scale (float, optional): upscale/ downscale the images produced. Intended
		for optimisation with a quality trade-off. Defaults to 1.

	Returns:
		dict[str, LottieFrames]: a dictionary of LottieFile.path to LottieFrames
		(LottieFile.data and a list of PIL.Image.Image frames) for each lottieFile
	"""
	lottieFrames = {}
	for future in asyncio.as_completed(
		[
			convSingleLottieTransparentFrames(
				lottieFile=lottieFile,
				frameSkip=frameSkip,
				scale=scale,
			)
			for lottieFile in lottieFiles
		]
	):
		lottieFrames = {**lottieFrames, **(await future)}
	return lottieFrames


async def convSingleLottieTransparentFrames(
	lottieFile: LottieFile,
	frameSkip: int = 0,
	scale: float = 1,
) -> dict[str, LottieFrames]:
	"""Convert a single lottie file to a dictionary of LottieFile.path to
	LottieFrames (LottieFile.data and a list of PIL.Image.Image frames) with
	transparency.

	Args:
		lottieFile (LottieFile): the lottie file to convert to frames
		frameSkip (int, optional): skip n number of frames in the interest of
		optimisation with a quality trade-off. Defaults to 0.
		scale (float, optional): upscale/ downscale the images produced. Intended
		for optimisation with a quality trade-off. Defaults to 1.

	Returns:
		dict[str, LottieFrames]: a dictionary of LottieFile.path to LottieFrames
		(LottieFile.data and a list of PIL.Image.Image frames)
	"""
	image1Frames = (
		await convSingleLottieFrames(
			lottieFile=lottieFile,
			backgroundColour="ff0000",
			frameSkip=frameSkip,
			scale=scale,
		)
	)[lottieFile.path].frames
	frames = []
	for index, layer in enumerate(
		(
			await convSingleLottieFrames(
				lottieFile=lottieFile,
				frameSkip=frameSkip,
				scale=scale,
			)
		)[lottieFile.path].frames
	):
		frames.append(
			Image.fromarray(_getTransparency(np.array(image1Frames[index]), np.array(layer)))
		)
	return {lottieFile.path: LottieFrames(data=lottieFile.data, frames=frames)}


async def convMultLottieFrames(
	lottieFiles: list[LottieFile],
	backgroundColour: str = "000000",
	frameSkip: int = 0,
	scale: float = 1,
) -> dict[str, LottieFrames]:
	"""Convert multiple lottie files to a dictionary of LottieFile.path to
	LottieFrames (LottieFile.data and a list of PIL.Image.Image frames).

	Args:
		lottieFiles (list[LottieFile]): the lottie file to convert to frames
		backgroundColour (str, optional): hex colour in the form rrggbb. Defaults
		to "000000".
		frameSkip (int, optional): skip n number of frames in the interest of
		optimisation with a quality trade-off. Defaults to 0.
		scale (float, optional): upscale/ downscale the images produced. Intended
		for optimisation with a quality trade-off. Defaults to 1.

	Returns:
		dict[str, LottieFrames]: a dictionary of LottieFile.path to LottieFrames
		(LottieFile.data and a list of PIL.Image.Image frames) for each lottieFile
	"""
	lottieFrames = {}
	for future in asyncio.as_completed(
		[
			convSingleLottieFrames(
				lottieFile=lottieFile,
				backgroundColour=backgroundColour,
				frameSkip=frameSkip,
				scale=scale,
			)
			for lottieFile in lottieFiles
		]
	):
		lottieFrames = {**lottieFrames, **(await future)}
	return lottieFrames


async def convSingleLottieFrames(
	lottieFile: LottieFile,
	backgroundColour: str = "000000",
	frameSkip: int = 0,
	scale: float = 1,
) -> dict[str, LottieFrames]:
	"""Convert a single lottie file to a dictionary of LottieFile.path to
	LottieFrames (LottieFile.data and a list of PIL.Image.Image frames).

	Args:
		lottieFile (LottieFile): the lottie file to convert to frames
		backgroundColour (str, optional): hex colour in the form rrggbb. Defaults
		to "000000".
		frameSkip (int, optional): skip n number of frames in the interest of
		optimisation with a quality trade-off. Defaults to 0.
		scale (float, optional): upscale/ downscale the images produced. Intended
		for optimisation with a quality trade-off. Defaults to 1.

	Returns:
		dict[str, LottieFrames]: a dictionary of LottieFile.path to LottieFrames
		(LottieFile.data and a list of PIL.Image.Image frames)
	"""
	with NamedTemporaryFile(suffix=".webp") as namedTemporaryFile:
		placeholderFile = namedTemporaryFile.name
	await convSingleLottie(
		lottieFile=lottieFile,
		destFiles={placeholderFile},
		backgroundColour=backgroundColour,
		frameSkip=frameSkip,
		scale=scale,
	)
	img = Image.open(placeholderFile)
	frames = []
	for index in range(img.n_frames):  # type: ignore
		img.seek(index)
		frames.append(img.copy())
	os.remove(placeholderFile)
	return {lottieFile.path: LottieFrames(data=lottieFile.data, frames=frames)}


async def convMultLottie(
	filemaps: list[FileMap],
	backgroundColour: str = "000000",
	frameSkip: int = 0,
	scale: float = 1,
) -> set[str]:
	"""Convert multiple lottie/tgs to files specified in filemaps
	can convert to .gif or .webp. For other formats use convMultLottieFrames and pillow

	Args:
		filemaps (list[FileMap]): list of FileMap(s) (LottieFiles to destFiles)
		backgroundColour (str, optional): hex colour in the form rrggbb. Defaults
		to "000000".
		frameSkip (int, optional): skip n number of frames in the interest of
		optimisation with a quality trade-off. Defaults to 0.
		scale (float, optional): upscale/ downscale the images produced. Intended
		for optimisation with a quality trade-off. Defaults to 1.

	Raises:
		ValueError: if no LottieFile was passed to the function via lottieFile or filemap
		RuntimeError: in the event of a failure calling lottie2gif or gif2webp
		OSError: if the user's environment is not supported

	Returns:
		set[str]: set of successfully converted files
	"""
	destFiles = set()
	for future in asyncio.as_completed(
		[
			convSingleLottie(
				filemap=filemap,
				backgroundColour=backgroundColour,
				frameSkip=frameSkip,
				scale=scale,
			)
			for filemap in filemaps
		]
	):
		_ = [destFiles.add(destFile) for destFile in await future]
	return destFiles


async def convSingleLottie(  # pylint: disable=too-many-arguments
	lottieFile: LottieFile = None,
	destFiles: set[str] = None,
	filemap: FileMap = None,
	backgroundColour: str = "000000",
	frameSkip: int = 0,
	scale: float = 1,
) -> set[str]:
	"""Convert a single lottie/tgs to files specified in destFiles
	can convert to .gif or .webp. For other formats use convSingleLottieFrames and pillow

	Args:
		lottieFile (LottieFile, optional): the lottiefile to convert. Defaults to None.
		destFiles (set[str], optional): a set of files to convert to (must
		contain either .gif or .webp files - other formats will be ignored).
		Defaults to None (["out.gif"]).
		filemap (FileMap, optional): alternatively, to specify a lottieFile
		and destFiles separately, can use a FileMap. Defaults to None.
		backgroundColour (str, optional): hex colour in the form rrggbb. Defaults
		to "000000".
		frameSkip (int, optional): skip n number of frames in the interest of
		optimisation with a quality trade-off. Defaults to 0.
		scale (float, optional): upscale/ downscale the images produced. Intended
		for optimisation with a quality trade-off. Defaults to 1.

	Raises:
		ValueError: if no LottieFile was passed to the function via lottieFile or filemap
		RuntimeError: in the event of a failure calling lottie2gif or gif2webp
		OSError: if the user's environment is not supported

	Returns:
		set[str]: set of successfully converted files
	"""
	# Check params
	if filemap is not None:
		lottieFile = filemap.lottieFile
		destFiles = filemap.destFiles
	if lottieFile is None:
		raise ValueError
	destFiles = destFiles or {"out.gif"}
	destFiles = {
		destFile
		for destFile in destFiles
		if destFile.rsplit(".", maxsplit=1)[-1] in ("webp", "gif")
	}

	# Get bin location
	binDir = _getBinDir()

	# lottie2gif
	gifFiles = [file for file in destFiles if file.endswith(".gif")]
	if len(gifFiles) < 1:
		with NamedTemporaryFile(suffix=".gif") as namedTemporaryFile:
			gifFiles = [namedTemporaryFile.name]
	cmd = (
		f"{binDir}/lottie2gif {lottieFile.path} {_scale(lottieFile.data['w'], scale)}"
		f"x{_scale(lottieFile.data['h'], scale)} {backgroundColour} {gifFiles[0]} {frameSkip}"
	)
	ret = await _execSubprocess(cmd)
	if ret[0] > 0:
		raise RuntimeError(f"{cmd=}: {ret=}")
	for gifFile in gifFiles[1:]:
		shutil.copy(gifFiles[0], gifFile)

	# gif2webp
	webpFiles = [file for file in destFiles if file.endswith(".webp")]
	if len(webpFiles):
		cmd = f"{binDir}/gif2webp {gifFiles[0]} -o {webpFiles[0]} -mt"
		ret = await _execSubprocess(cmd)
		if ret[0] > 0:
			raise RuntimeError(f"{cmd=}: {ret=}")
		for webpFile in webpFiles[1:]:
			shutil.copy(webpFiles[0], webpFile)

	return destFiles
