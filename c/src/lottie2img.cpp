

// Stdlib
#include <stdio.h>
#include <math.h>
#include <fstream>

#include <string>

// Third party
#include "webp/encode.h"
#include "webp/mux.h"
#include "rlottie.h"
#include "gif.h"

/*
help function outputs text to stdout
*/
int help()
{
	printf(
		"Usage: lottie2img [LOTTIEFILENAME] [WIDTH_PX] [HEIGHT_PX] "
		"[BGCOLOR_ARGB]\n");
	printf(" \n");
	printf("Options:\n");
	printf("  -h / -help ............. this help\n");
	printf("  -gif [GIF] ............. encode to gif\n");
	printf("  -webp [WEBP] ........... encode to webp\n");
	printf("  -fs [FS] ........... frameskip\n");
	printf("Examples:\n");
	printf("  lottie2img 3d.json 500 500 00ff00ff\n");
	printf("  lottie2img 3d.json 500 500 00ff00ff -gif 3d.gif\n");
	return 1;
}

int error(std::string s)
{
	printf(s.c_str());
	return 2;
}

/*
main entry point
*/
int main(int argc, char **argv)
{
	if (argc < 5)
	{
		return help();
	}
	std::string lottiefilename = argv[1];
	int width_px = atoi(argv[2]);
	int height_px = atoi(argv[3]);
	int bgcolor_argb = strtol(argv[4], NULL, 16);

	uint8_t bgcolor_a = ((bgcolor_argb & 0xff000000) >> 24);
	uint8_t bgcolor_r = ((bgcolor_argb & 0xff0000) >> 16);
	uint8_t bgcolor_g = ((bgcolor_argb & 0x00ff00) >> 8);
	uint8_t bgcolor_b = ((bgcolor_argb & 0x0000ff));

	char *gif = nullptr;
	char *webp = nullptr;
	int frame_skip = 0;
	for (int c = 5; c < argc; ++c)
	{
		int parse_error = 0;
		if (!strcmp(argv[c], "-h") || !strcmp(argv[c], "-help"))
		{
			return help();
		}
		else if (!strcmp(argv[c], "-gif") && c < argc - 1)
		{
			gif = argv[++c];
		}
		else if (!strcmp(argv[c], "-webp") && c < argc - 1)
		{
			webp = argv[++c];
		}
		else if (!strcmp(argv[c], "-fs") && c < argc - 1)
		{
			frame_skip = atoi(argv[++c]);
		}

		auto player = rlottie::Animation::loadFromFile(lottiefilename);
		if (!player)
		{
			return error("Failed to parse lottie file\n");
		}

		auto buffer = std::unique_ptr<uint32_t[]>(new uint32_t[width_px * height_px]);
		size_t frameCount = player->totalFrame();
		int step = (frame_skip + 1);
		size_t delay_ms = (size_t)round(1000 * step / player->frameRate());
		size_t delay_cs = (size_t)round(100 * step / player->frameRate());

		// GIF
		GifWriter handle;
		GifBegin(&handle, gif, width_px, height_px, delay_cs);

		// WEBP
		WebPAnimEncoderOptions enc_options;
		WebPConfig config;
		WebPAnimEncoder *enc;
		WebPData webp_data;
		WebPPicture pic;

		WebPAnimEncoderOptionsInit(&enc_options);
		WebPConfigInit(&config);
		WebPDataInit(&webp_data);
		WebPPictureInit(&pic);

		config.lossless = 0;
		config.method = 0;

		enc_options.kmin = config.lossless ? 9 : 3;
		enc_options.kmax = config.lossless ? 17 : 5;

		pic.use_argb = 1;
		pic.width = width_px;
		pic.height = height_px;

		enc = WebPAnimEncoderNew(width_px, height_px, &enc_options);

		for (size_t i = 0; i < frameCount; i += step)
		{
			rlottie::Surface surface(buffer.get(), width_px, height_px,
									 width_px * 4);
			player->renderSync(i, surface);
			uint8_t *buffer = reinterpret_cast<uint8_t *>(surface.buffer());
			uint32_t totalBytes = surface.height() * surface.bytesPerLine();

			for (uint32_t i = 0; i < totalBytes; i += 4)
			{
				unsigned char a = buffer[i + 3];
				// compute only if alpha is non zero
				if (a)
				{
					unsigned char r = buffer[i + 2];
					unsigned char g = buffer[i + 1];
					unsigned char b = buffer[i];

					if (a != 255)
					{ // un premultiply
						unsigned char r2 =
							(unsigned char)((float)bgcolor_r *
											((float)(255 - a) / 255));
						unsigned char g2 =
							(unsigned char)((float)bgcolor_g *
											((float)(255 - a) / 255));
						unsigned char b2 =
							(unsigned char)((float)bgcolor_b *
											((float)(255 - a) / 255));
						buffer[i] = r + r2;
						buffer[i + 1] = g + g2;
						buffer[i + 2] = b + b2;
					}
					else
					{
						// only swizzle r and b
						buffer[i] = r;
						buffer[i + 2] = b;
					}
				}
				else
				{
					buffer[i + 2] = bgcolor_b;
					buffer[i + 1] = bgcolor_g;
					buffer[i] = bgcolor_r;
				}
			}
			// GIF
			if (gif)
			{
				GifWriteFrame(&handle, reinterpret_cast<uint8_t *>(surface.buffer()),
							  surface.width(), surface.height(), delay_cs);
			}

			// WEBP
			if (webp)
			{
				WebPPictureImportRGBA(&pic, buffer, width_px * 4);
				WebPAnimEncoderAdd(enc, &pic, round(delay_ms * i), &config);
			}
		}

		// GIF
		if (gif)
		{
			GifEnd(&handle);
		}

		// WEBP
		if (webp)
		{
			WebPAnimEncoderAdd(enc, NULL, round(delay_ms * frameCount), NULL);
			WebPAnimEncoderAssemble(enc, &webp_data);
			WebPAnimEncoderDelete(enc);

			std::ofstream file;
			file.open(webp, std::ios_base::binary);
			file.write((const char *)webp_data.bytes, webp_data.size);
			file.close();
		}
	}

	return 0;
}
