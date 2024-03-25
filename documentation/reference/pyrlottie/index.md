# Pyrlottie

[Pyrlottie Index](../README.md#pyrlottie-index) / Pyrlottie

> Auto-generated documentation for [pyrlottie](../../../pyrlottie/__init__.py) module.

- [Pyrlottie](#pyrlottie)
  - [FileMap](#filemap)
  - [LottieFile](#lottiefile)
    - [LottieFile().__attrs_post_init__](#lottiefile()__attrs_post_init__)
  - [LottieFrames](#lottieframes)
  - [_execSubprocess](#_execsubprocess)
  - [_getBinDir](#_getbindir)
  - [_getTransparency](#_gettransparency)
  - [_scale](#_scale)
  - [convMultLottie](#convmultlottie)
  - [convMultLottieFrames](#convmultlottieframes)
  - [convMultLottieTransparentFrames](#convmultlottietransparentframes)
  - [convSingleLottie](#convsinglelottie)
  - [convSingleLottieFrames](#convsinglelottieframes)
  - [convSingleLottieTransparentFrames](#convsinglelottietransparentframes)
  - [run](#run)

## FileMap

[Show source in __init__.py:129](../../../pyrlottie/__init__.py#L129)

FileMap. Map a LottieFile to a set of destination/output files.

#### Arguments

----
 - `lottieFile` *LottieFile* - lottie file
 - `destFiles` *set[str]* - set of destination/output files. Default={"out.gif"}

#### Signature

```python
class FileMap: ...
```



## LottieFile

[Show source in __init__.py:81](../../../pyrlottie/__init__.py#L81)

LottieFile. Load a lottie/tgs has a path and data (json/dict).

#### Arguments

----
 - `path` *str* - path to the lottie file
 - `data` *dict* - python dict representing the json data. Default=None (file is read)

#### Raises

------
 - `ValueError` - Failure to parse the lottiefile json

#### Signature

```python
class LottieFile: ...
```

### LottieFile().__attrs_post_init__

[Show source in __init__.py:98](../../../pyrlottie/__init__.py#L98)

LottieFile __attrs_post_init__ called by attrs.

#### Arguments

----
 - [path](#lottiefile) *str* - path to the lottie file
 - [data](#lottiefile) *dict* - python dict representing the json data. Default=None (file is read)

#### Raises

------
 - `ValueError` - Failure to parse the lottiefile json

#### Signature

```python
def __attrs_post_init__(self) -> None: ...
```



## LottieFrames

[Show source in __init__.py:144](../../../pyrlottie/__init__.py#L144)

LottieFrames. Dataclass to hold info on lottieframes with LottieFile.data
and a list of PIL.Image.Image(s) containing frame data.

#### Arguments

----
 - `data` *LottieFile* - LottieFile.data
 - `frames` *list[Image.Image]* - list of PIL.Image.Image(s) containing frame data

#### Signature

```python
class LottieFrames: ...
```



## _execSubprocess

[Show source in __init__.py:159](../../../pyrlottie/__init__.py#L159)

Execute a command and check for errors.

#### Arguments

----
 - `command` *str* - commands as a string

#### Returns

-------
 - `tuple[int,` *bytes]* - tuple of return code (int) and stdout (str)

#### Signature

```python
async def _execSubprocess(command: str) -> tuple[int, bytes]: ...
```



## _getTransparency

[Show source in __init__.py:221](../../../pyrlottie/__init__.py#L221)

Get the transparent pixels from an image with a red bg and an image with a black bg.

#### Arguments

----
 - `image1` *np.ndarray* - image1 (the red image)
 - `image2` *np.ndarray* - image2 (the black image)

#### Returns

-------
 - `np.ndarray` - pixels for the transparent image

#### Signature

```python
def _getTransparency(image1: np.ndarray, image2: np.ndarray) -> np.ndarray: ...
```



## _scale

[Show source in __init__.py:203](../../../pyrlottie/__init__.py#L203)

Get a scaled dimen.

#### Arguments

----
 - `dimen` *str* - dimension in px
 - `scale` *float* - scale

#### Returns

-------
 - `Optional[int,` *str]* - scaled dimen (min=1)

#### Signature

```python
def _scale(dimen: str, scale: float = 1) -> int | str: ...
```



## convMultLottie

[Show source in __init__.py:438](../../../pyrlottie/__init__.py#L438)

Convert multiple lottie/tgs to files specified in filemaps
can convert to .gif or .webp. For other formats use convMultLottieFrames and pillow.

#### Arguments

----
 - `filemaps` *list[FileMap]* - list of FileMap(s) (LottieFiles to destFiles)
 - `backgroundColour` *str, optional* - hex colour in the form rrggbb. Defaults
 to "000000".
 - `frameSkip` *int, optional* - skip n number of frames in the interest of
 optimisation with a quality trade-off. Defaults to 0.
 - `scale` *float, optional* - upscale/ downscale the images produced. Intended
 for optimisation with a quality trade-off. Defaults to 1.

#### Raises

------
 - `ValueError` - if no LottieFile was passed to the function via lottieFile or filemap
 - `RuntimeError` - in the event of a failure calling lottie2gif or gif2webp
 - `OSError` - if the user's environment is not supported

#### Returns

-------
 - `set[str]` - set of successfully converted files

#### Signature

```python
async def convMultLottie(
    filemaps: list[FileMap],
    backgroundColour: str = "000000",
    frameSkip: int = 0,
    scale: float = 1,
) -> set[str]: ...
```

#### See also

- [FileMap](#filemap)



## convMultLottieFrames

[Show source in __init__.py:354](../../../pyrlottie/__init__.py#L354)

Convert multiple lottie files to a dictionary of LottieFile.path to
LottieFrames (LottieFile.data and a list of PIL.Image.Image frames).

#### Arguments

----
 - `lottieFiles` *list[LottieFile]* - the lottie file to convert to frames
 - `backgroundColour` *str, optional* - hex colour in the form rrggbb. Defaults
 to "000000".
 - `frameSkip` *int, optional* - skip n number of frames in the interest of
 optimisation with a quality trade-off. Defaults to 0.
 - `scale` *float, optional* - upscale/ downscale the images produced. Intended
 for optimisation with a quality trade-off. Defaults to 1.

#### Returns

-------
 - `dict[str,` *LottieFrames]* - a dictionary of LottieFile.path to LottieFrames
 (LottieFile.data and a list of PIL.Image.Image frames) for each lottieFile

#### Signature

```python
async def convMultLottieFrames(
    lottieFiles: list[LottieFile],
    backgroundColour: str = "000000",
    frameSkip: int = 0,
    scale: float = 1,
) -> dict[str, LottieFrames]: ...
```

#### See also

- [LottieFile](#lottiefile)
- [LottieFrames](#lottieframes)



## convMultLottieTransparentFrames

[Show source in __init__.py:269](../../../pyrlottie/__init__.py#L269)

Convert multiple lottie files to a dictionary of LottieFile.path to
LottieFrames (LottieFile.data and a list of PIL.Image.Image frames) with
transparency.

#### Arguments

----
 - `lottieFiles` *list[LottieFile]* - the lottie file to convert to frames
 - `frameSkip` *int, optional* - skip n number of frames in the interest of
 optimisation with a quality trade-off. Defaults to 0.
 - `scale` *float, optional* - upscale/ downscale the images produced. Intended
 for optimisation with a quality trade-off. Defaults to 1.

#### Returns

-------
 - `dict[str,` *LottieFrames]* - a dictionary of LottieFile.path to LottieFrames
 (LottieFile.data and a list of PIL.Image.Image frames) for each lottieFile

#### Signature

```python
async def convMultLottieTransparentFrames(
    lottieFiles: list[LottieFile], frameSkip: int = 0, scale: float = 1
) -> dict[str, LottieFrames]: ...
```

#### See also

- [LottieFile](#lottiefile)
- [LottieFrames](#lottieframes)



## convSingleLottie

[Show source in __init__.py:484](../../../pyrlottie/__init__.py#L484)

Convert a single lottie/tgs to files specified in destFiles
can convert to .gif or .webp. For other formats use convSingleLottieFrames and pillow.

#### Arguments

----
 - `lottieFile` *LottieFile, optional* - the lottiefile to convert. Defaults to None.
 - `destFiles` *set[str], optional* - a set of files to convert to (must
 contain either .gif or .webp files - other formats will be ignored).
 Defaults to None (["out.gif"]).
 - `filemap` *FileMap, optional* - alternatively, to specify a lottieFile
 and destFiles separately, can use a FileMap. Defaults to None.
 - `backgroundColour` *str, optional* - hex colour in the form rrggbb. Defaults
 to "000000".
 - `frameSkip` *int, optional* - skip n number of frames in the interest of
 optimisation with a quality trade-off. Defaults to 0.
 - `scale` *float, optional* - upscale/ downscale the images produced. Intended
 for optimisation with a quality trade-off. Defaults to 1.

#### Raises

------
 - `ValueError` - if no LottieFile was passed to the function via lottieFile or filemap
 - `RuntimeError` - in the event of a failure calling lottie2gif or gif2webp
 - `OSError` - if the user's environment is not supported

#### Returns

-------
 - `set[str]` - set of successfully converted files

#### Signature

```python
async def convSingleLottie(
    lottieFile: LottieFile | None = None,
    destFiles: set[str] | None = None,
    filemap: FileMap | None = None,
    backgroundColour: str = "000000",
    frameSkip: int = 0,
    scale: float = 1,
) -> set[str]: ...
```



## convSingleLottieFrames

[Show source in __init__.py:395](../../../pyrlottie/__init__.py#L395)

Convert a single lottie file to a dictionary of LottieFile.path to
LottieFrames (LottieFile.data and a list of PIL.Image.Image frames).

#### Arguments

----
 - `lottieFile` *LottieFile* - the lottie file to convert to frames
 - `backgroundColour` *str, optional* - hex colour in the form rrggbb. Defaults
 to "000000".
 - `frameSkip` *int, optional* - skip n number of frames in the interest of
 optimisation with a quality trade-off. Defaults to 0.
 - `scale` *float, optional* - upscale/ downscale the images produced. Intended
 for optimisation with a quality trade-off. Defaults to 1.

#### Returns

-------
 - `dict[str,` *LottieFrames]* - a dictionary of LottieFile.path to LottieFrames
 (LottieFile.data and a list of PIL.Image.Image frames)

#### Signature

```python
async def convSingleLottieFrames(
    lottieFile: LottieFile,
    backgroundColour: str = "000000",
    frameSkip: int = 0,
    scale: float = 1,
) -> dict[str, LottieFrames]: ...
```

#### See also

- [LottieFile](#lottiefile)
- [LottieFrames](#lottieframes)



## convSingleLottieTransparentFrames

[Show source in __init__.py:307](../../../pyrlottie/__init__.py#L307)

Convert a single lottie file to a dictionary of LottieFile.path to
LottieFrames (LottieFile.data and a list of PIL.Image.Image frames) with
transparency.

#### Arguments

----
 - `lottieFile` *LottieFile* - the lottie file to convert to frames
 - `frameSkip` *int, optional* - skip n number of frames in the interest of
 optimisation with a quality trade-off. Defaults to 0.
 - `scale` *float, optional* - upscale/ downscale the images produced. Intended
 for optimisation with a quality trade-off. Defaults to 1.

#### Returns

-------
 - `dict[str,` *LottieFrames]* - a dictionary of LottieFile.path to LottieFrames
 (LottieFile.data and a list of PIL.Image.Image frames)

#### Signature

```python
async def convSingleLottieTransparentFrames(
    lottieFile: LottieFile, frameSkip: int = 0, scale: float = 1
) -> dict[str, LottieFrames]: ...
```

#### See also

- [LottieFile](#lottiefile)
- [LottieFrames](#lottieframes)



## run

[Show source in __init__.py:246](../../../pyrlottie/__init__.py#L246)

Run until the future (an instance of Future) has completed.
If the argument is a coroutine object it is implicitly scheduled to run as a asyncio.Task.
Return the Future's result or raise its exception.

Use `pyrlottie.run(convMethod)` or `asyncio.get_event_loop().run_until_complete(convMethod)`
in place of `asyncio.run(convMethod)`
See https://github.com/awestlake87/pyo3-asyncio/issues/19#issuecomment-846686814
for more information

#### Arguments

----
 - `convMethod` *Awaitable* - Awaitable to run. eg.
 convSingleLottie(gLottieFile, destFiles={"test_data/convSingleLottie.webp"})

#### Returns

-------
 - `Any` - the Awaitable's result or raise its exception.

#### Signature

```python
def run(convMethod: Awaitable) -> Any: ...
```