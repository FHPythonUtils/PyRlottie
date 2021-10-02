# pyrlottie

> Auto-generated documentation for [pyrlottie](../../pyrlottie/__init__.py) module.

Convert .tgs and .lottie to .webp or .gif using rlottie.

- [Pyrlottie](../README.md#pyrlottie-index) / [Modules](../README.md#pyrlottie-modules) / pyrlottie
    - [Formats](#formats)
    - [Basic Usage](#basic-usage)
    - [FileMap](#filemap)
    - [LottieFile](#lottiefile)
        - [LottieFile().\_\_attrs\_post\_init\_\_](#lottiefile__attrs_post_init__)
    - [LottieFrames](#lottieframes)
    - [convMultLottie](#convmultlottie)
    - [convMultLottieFrames](#convmultlottieframes)
    - [convMultLottieTransparentFrames](#convmultlottietransparentframes)
    - [convSingleLottie](#convsinglelottie)
    - [convSingleLottieFrames](#convsinglelottieframes)
    - [convSingleLottieTransparentFrames](#convsinglelottietransparentframes)

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

## FileMap

[[find in source code]](../../pyrlottie/__init__.py#L126)

```python
attr.s
class FileMap():
```

FileMap. Map a LottieFile to a set of destination/output files.

#### Arguments

- `lottieFile` *LottieFile* - lottie file
- `destFiles` *set[str]* - set of destination/output files. Default=["out.gif"]

## LottieFile

[[find in source code]](../../pyrlottie/__init__.py#L81)

```python
attr.s
class LottieFile():
```

LottieFile. Load a lottie/tgs has a path and data (json/dict).

#### Arguments

- `path` *str* - path to the lottie file
- `data` *dict* - python dict representing the json data. Default=None (file is read)

#### Raises

- `ValueError` - Failure to parse the lottiefile json

### LottieFile().\_\_attrs\_post\_init\_\_

[[find in source code]](../../pyrlottie/__init__.py#L95)

```python
def __attrs_post_init__() -> None:
```

LottieFile __attrs_post_init__ called by attrs.

#### Arguments

- `path` *str* - path to the lottie file
- `data` *dict* - python dict representing the json data. Default=None (file is read)

#### Raises

- `ValueError` - Failure to parse the lottiefile json

## LottieFrames

[[find in source code]](../../pyrlottie/__init__.py#L139)

```python
attr.s
class LottieFrames():
```

LottieFrames. Dataclass to hold info on lottieframes with LottieFile.data
and a list of PIL.Image.Image(s) containing frame data.

#### Arguments

- `data` *LottieFile* - LottieFile.data
- `frames` *list[Image.Image]* - list of PIL.Image.Image(s) containing frame data

## convMultLottie

[[find in source code]](../../pyrlottie/__init__.py#L382)

```python
async def convMultLottie(
    filemaps: list[FileMap],
    backgroundColour: str = '000000',
    frameSkip: int = 0,
    scale: float = 1,
) -> set[str]:
```

Convert multiple lottie/tgs to files specified in filemaps
can convert to .gif or .webp. For other formats use convMultLottieFrames and pillow

#### Arguments

- `filemaps` *list[FileMap]* - list of FileMap(s) (LottieFiles to destFiles)
- `backgroundColour` *str, optional* - hex colour in the form rrggbb. Defaults
to "000000".
- `frameSkip` *int, optional* - skip n number of frames in the interest of
optimisation with a quality trade-off. Defaults to 0.
- `scale` *float, optional* - upscale/ downscale the images produced. Intended
for optimisation with a quality trade-off. Defaults to 1.

#### Returns

- `set[str]` - set of successfully converted files

## convMultLottieFrames

[[find in source code]](../../pyrlottie/__init__.py#L304)

```python
async def convMultLottieFrames(
    lottieFiles: list[LottieFile],
    backgroundColour: str = '000000',
    frameSkip: int = 0,
    scale: float = 1,
) -> dict[(str, LottieFrames)]:
```

Convert multiple lottie files to a dictionary of LottieFile.path to
LottieFrames (LottieFile.data and a list of PIL.Image.Image frames).

#### Arguments

- `lottieFiles` *list[LottieFile]* - the lottie file to convert to frames
- `backgroundColour` *str, optional* - hex colour in the form rrggbb. Defaults
to "000000".
- `frameSkip` *int, optional* - skip n number of frames in the interest of
optimisation with a quality trade-off. Defaults to 0.
- `scale` *float, optional* - upscale/ downscale the images produced. Intended
for optimisation with a quality trade-off. Defaults to 1.

#### Returns

- `dict[str,` *LottieFrames]* - a dictionary of LottieFile.path to LottieFrames
(LottieFile.data and a list of PIL.Image.Image frames) for each lottieFile

## convMultLottieTransparentFrames

[[find in source code]](../../pyrlottie/__init__.py#L225)

```python
async def convMultLottieTransparentFrames(
    lottieFiles: list[LottieFile],
    frameSkip: int = 0,
    scale: float = 1,
) -> dict[(str, LottieFrames)]:
```

Convert multiple lottie files to a dictionary of LottieFile.path to
LottieFrames (LottieFile.data and a list of PIL.Image.Image frames) with
transparency.

#### Arguments

- `lottieFiles` *list[LottieFile]* - the lottie file to convert to frames
- `frameSkip` *int, optional* - skip n number of frames in the interest of
optimisation with a quality trade-off. Defaults to 0.
- `scale` *float, optional* - upscale/ downscale the images produced. Intended
for optimisation with a quality trade-off. Defaults to 1.

#### Returns

- `dict[str,` *LottieFrames]* - a dictionary of LottieFile.path to LottieFrames
(LottieFile.data and a list of PIL.Image.Image frames) for each lottieFile

## convSingleLottie

[[find in source code]](../../pyrlottie/__init__.py#L419)

```python
async def convSingleLottie(
    lottieFile: LottieFile = None,
    destFiles: set[str] = None,
    filemap: FileMap = None,
    backgroundColour: str = '000000',
    frameSkip: int = 0,
    scale: float = 1,
) -> set[str]:
```

Convert a single lottie/tgs to files specified in destFiles
can convert to .gif or .webp. For other formats use convSingleLottieFrames and pillow

#### Arguments

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

- `ValueError` - if no LottieFile was passed to the function via lottieFile or filemap
- `RuntimeError` - in the event of a failure calling lottie2gif or gif2webp

#### Returns

- `set[str]` - set of successfully converted files

#### See also

- [FileMap](#filemap)
- [LottieFile](#lottiefile)

## convSingleLottieFrames

[[find in source code]](../../pyrlottie/__init__.py#L342)

```python
async def convSingleLottieFrames(
    lottieFile: LottieFile,
    backgroundColour: str = '000000',
    frameSkip: int = 0,
    scale: float = 1,
) -> dict[(str, LottieFrames)]:
```

Convert a single lottie file to a dictionary of LottieFile.path to
LottieFrames (LottieFile.data and a list of PIL.Image.Image frames).

#### Arguments

- `lottieFile` *LottieFile* - the lottie file to convert to frames
- `backgroundColour` *str, optional* - hex colour in the form rrggbb. Defaults
to "000000".
- `frameSkip` *int, optional* - skip n number of frames in the interest of
optimisation with a quality trade-off. Defaults to 0.
- `scale` *float, optional* - upscale/ downscale the images produced. Intended
for optimisation with a quality trade-off. Defaults to 1.

#### Returns

- `dict[str,` *LottieFrames]* - a dictionary of LottieFile.path to LottieFrames
(LottieFile.data and a list of PIL.Image.Image frames)

#### See also

- [LottieFile](#lottiefile)

## convSingleLottieTransparentFrames

[[find in source code]](../../pyrlottie/__init__.py#L260)

```python
async def convSingleLottieTransparentFrames(
    lottieFile: LottieFile,
    frameSkip: int = 0,
    scale: float = 1,
) -> dict[(str, LottieFrames)]:
```

Convert a single lottie file to a dictionary of LottieFile.path to
LottieFrames (LottieFile.data and a list of PIL.Image.Image frames) with
transparency.

#### Arguments

- `lottieFile` *LottieFile* - the lottie file to convert to frames
- `frameSkip` *int, optional* - skip n number of frames in the interest of
optimisation with a quality trade-off. Defaults to 0.
- `scale` *float, optional* - upscale/ downscale the images produced. Intended
for optimisation with a quality trade-off. Defaults to 1.

#### Returns

- `dict[str,` *LottieFrames]* - a dictionary of LottieFile.path to LottieFrames
(LottieFile.data and a list of PIL.Image.Image frames)

#### See also

- [LottieFile](#lottiefile)
