"""Basic tests for pyrlottie.
"""
from __future__ import annotations

import asyncio
import sys
import time
from pathlib import Path

THISDIR = str(Path(__file__).resolve().parent)
sys.path.insert(0, str(Path(THISDIR).parent))

from pyrlottie import (
	FileMap,
	LottieFile,
	convMultLottie,
	convMultLottieFrames,
	convSingleLottie,
	convSingleLottieFrames,
)

gLottieFile = LottieFile(f"{THISDIR}/data/3d.json")

# convSingleLottie
teststart = start = time.time()
print(
	asyncio.run(
		convSingleLottie(gLottieFile, destFiles={f"{THISDIR}/data/convSingleLottie.webp"}),
	)
)

end = time.time()
print(f"Time taken (convSingleLottie) - {(end - start):.3f}s")

# convMultLottie
start = time.time()
print(
	asyncio.run(
		convMultLottie([FileMap(gLottieFile, {f"{THISDIR}/data/convMultLottie.webp"})] * 10),
	)
)

end = time.time()
print(f"Time taken (convMultLottie) - {(end - start):.3f}s")

# convMultLottie
start = time.time()
print(
	asyncio.run(
		convMultLottie(
			[
				FileMap(
					LottieFile(f"{THISDIR}/data/file_43{i}.tgs"),
					{f"{THISDIR}/data/file_43{i}.webp"},
				)
				for i in range(4, 10)
			]
			* 3
		)
	)
)

end = time.time()
print(f"Time taken (convMultLottie:tgs) - {(end - start):.3f}s")

# convSingleLottieFrames
start = time.time()
print(len((asyncio.run(convSingleLottieFrames(gLottieFile)))[gLottieFile.path].frames))
end = time.time()
print(f"Time taken (convSingleLottieFrames) - {(end - start):.3f}s")

# convMultLottieFrames
start = time.time()
print(len(asyncio.run(convMultLottieFrames([gLottieFile for _ in range(10)]))))
end = time.time()
print(f"Time taken (convMultLottieFrames) - {(end - start):.3f}s")

# convSingleLottieFrames
start = time.time()
gLottieFrames = asyncio.run(convSingleLottieFrames(gLottieFile))
layers = gLottieFrames[gLottieFile.path].frames
print(len(layers))
layers[0].save(
	f"{THISDIR}/data/convSingleLottieFrames.webp",
	duration=int(1000 / gLottieFile.data["fr"]),
	save_all=True,
	append_images=layers[1:],
)
end = time.time()
print(f"Time taken (convSingleLottieFrames) - {(end - start):.3f}s")

# convMultLottieFrames
start = time.time()
print(len(asyncio.run(convMultLottieFrames([gLottieFile for _ in range(10)]))))
end = time.time()
print(f"Time taken (convMultLottieFrames) - {(end - start):.3f}s")

# convMultLottieFrames
start = time.time()
print(
	len(
		asyncio.run(
			convMultLottieFrames(
				[LottieFile(f"{THISDIR}/data/file_43{i}.tgs") for i in range(4, 10)]
			)
		)
	)
)
end = time.time()
print(f"Time taken (convMultLottieFrames:tgs) - {(end - start):.3f}s")

# convMultLottieFrames
start = time.time()
print(
	len(
		asyncio.run(
			convMultLottieFrames(
				[LottieFile(f"{THISDIR}/data/file_43{i}.tgs") for i in range(4, 10)], 1
			)
		)
	)
)
end = time.time()
print(f"Time taken (convMultLottieFrames:tgs:frameSkip=1=30fps) - {(end - start):.3f}s")

print(f"## Total time taken - {(time.time() - teststart):.3f}s")
