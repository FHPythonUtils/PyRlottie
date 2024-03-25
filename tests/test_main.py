import sys
from pathlib import Path

from imgcompare import imgcompare
from PIL import Image

THISDIR = str(Path(__file__).resolve().parent)
sys.path.insert(0, str(Path(THISDIR).parent))

from pyrlottie import (
	FileMap,
	LottieFile,
	convMultLottie,
	convSingleLottie,
	convSingleLottieTransparentFrames,
	run,
)

gLottieFile = LottieFile(f"{THISDIR}/data/3d.json")


def test_convSingleLottie() -> None:
	"""test_convSingleLottie"""
	outputFile = f"{THISDIR}/data/convSingleLottie.webp"
	run(
		convSingleLottie(gLottieFile, destFiles={outputFile}),
	)
	output = Image.open(outputFile)
	expected = Image.open(f"{THISDIR}/data/convSingleLottie_expected.webp")
	assert output.n_frames == expected.n_frames
	for frame in range(output.n_frames):
		output.seek(frame)
		expected.seek(frame)
		assert imgcompare.is_equal(
			output,
			expected,
			tolerance=0.2,
		)


def test_convMultLottie() -> None:
	"""test_convMultLottie"""
	run(
		convMultLottie(
			[
				FileMap(
					LottieFile(f"{THISDIR}/data/file_43{i}.tgs"),
					{f"{THISDIR}/data/file_43{i}.webp"},
				)
				for i in range(4, 10)
			]
		)
	)
	for file in [f"{THISDIR}/data/file_43{idx}.webp" for idx in range(4, 10)]:
		assert Path(f"{file}").exists()
		assert (
			Image.open(file).n_frames
			== Image.open(file.replace(".webp", "_expected.webp")).n_frames
		)


def test_convSingleLottieTransparentFrames() -> None:
	"""test_convSingleLottieTransparentFrames"""
	gLottieFrames = run(convSingleLottieTransparentFrames(gLottieFile))
	layers = gLottieFrames[gLottieFile.path].frames
	print(len(layers))
	outputFile = f"{THISDIR}/data/convSingleLottieTransparentFrames.webp"
	layers[0].save(
		outputFile,
		duration=int(1000 / gLottieFile.data["fr"]),
		save_all=True,
		append_images=layers[1:],
	)
	output = Image.open(outputFile)
	expected = Image.open(f"{THISDIR}/data/convSingleLottieTransparentFrames_expected.webp")
	assert output.n_frames == expected.n_frames
	for frame in range(output.n_frames):
		output.seek(frame)
		expected.seek(frame)
		assert imgcompare.is_equal(
			output,
			expected,
			tolerance=0.2,
		)


if __name__ == "__main__":
	test_convSingleLottie()
	test_convMultLottie()
	test_convSingleLottieTransparentFrames()