"""Basic tests for pyrlottie."""

from __future__ import annotations

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
	convMultLottieTransparentFrames,
	convSingleLottie,
	convSingleLottieFrames,
	convSingleLottieTransparentFrames,
	run,
)

gLottieFile = LottieFile(f"{THISDIR}/data/3d.json")

# convSingleLottie
teststart = start = time.time()
print(
	run(
		convSingleLottie(gLottieFile, destFiles={f"{THISDIR}/data/convSingleLottie.webp"}),
	)
)

end = time.time()
print(f"Time taken (convSingleLottie) - {(end - start):.3f}s")

# convMultLottie
start = time.time()
print(
	run(
		convMultLottie([FileMap(gLottieFile, {f"{THISDIR}/data/convMultLottie.webp"})] * 10),
	)
)

end = time.time()
print(f"Time taken (convMultLottie) - {(end - start):.3f}s")

# convMultLottie
start = time.time()
print(
	run(
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
print(len((run(convSingleLottieFrames(gLottieFile)))[gLottieFile.path].frames))
end = time.time()
print(f"Time taken (convSingleLottieFrames) - {(end - start):.3f}s")

# convMultLottieFrames
start = time.time()
print(len(run(convMultLottieFrames([gLottieFile for _ in range(10)]))))
end = time.time()
print(f"Time taken (convMultLottieFrames) - {(end - start):.3f}s")

# convSingleLottieTransparentFrames
start = time.time()
gLottieFrames = run(convSingleLottieTransparentFrames(gLottieFile))
layers = gLottieFrames[gLottieFile.path].frames
print(len(layers))
layers[0].save(
	f"{THISDIR}/data/convSingleLottieTransparentFrames.webp",
	duration=int(1000 / gLottieFile.data["fr"]),
	save_all=True,
	append_images=layers[1:],
)
end = time.time()
print(f"Time taken (convSingleLottieTransparentFrames) - {(end - start):.3f}s")

# convMultLottieTransparentFrames
start = time.time()
print(len(run(convMultLottieTransparentFrames([gLottieFile for _ in range(10)]))))
end = time.time()
print(f"Time taken (convMultLottieTransparentFrames) - {(end - start):.3f}s")

# convMultLottieTransparentFrames
start = time.time()
print(
	len(
		run(
			convMultLottieTransparentFrames(
				[LottieFile(f"{THISDIR}/data/file_43{i}.tgs") for i in range(4, 10)]
			)
		)
	)
)
end = time.time()
print(f"Time taken (convMultLottieTransparentFrames:tgs) - {(end - start):.3f}s")

# convMultLottieTransparentFrames
start = time.time()
print(
	len(
		run(
			convMultLottieTransparentFrames(
				[LottieFile(f"{THISDIR}/data/file_43{i}.tgs") for i in range(4, 10)], 1
			)
		)
	)
)
end = time.time()
print(f"Time taken (convMultLottieTransparentFrames:tgs:frameSkip=1=30fps) - {(end - start):.3f}s")

print(f"## Total time taken - {(time.time() - teststart):.3f}s")
