import os
import time
import subprocess


LIB = 'neural_style.py'
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
LIB_PATH = os.path.join(DIR_PATH, 'lib/neural-style-tf-master/')
OUTPUT_PATH = os.path.join(DIR_PATH, 'lib/neural-style-tf-master/image_output/')

SKIP_STYLE_COLOR = ['abstract-mediterranean-landscape.jpg', '']

for content_img in os.listdir(os.path.join(LIB_PATH, 'image_input')):
	print(f'--------------- {content_img} ---------------')

	for style_img in os.listdir(os.path.join(LIB_PATH, 'styles')):
		print(f'\n{style_img}')

		output_img =  style_img[:-4] + '-all-famous-art-' +content_img[:-4]
		original_colors_output_img =  style_img[:-4] + '-original-colors-all-famous-art-' +content_img[:-4]		
		output_pixel_max = 512

		if os.path.isdir(os.path.join(OUTPUT_PATH, output_img)):
			print(f'Erorr: duplicate exists\nskipping {output_img}')
			continue

		tic = time.time()



		if 'original-colors-only' in style_img:
			pass
		else:
			subprocess.run(['python', os.path.join(LIB_PATH, LIB),
				'--style_imgs', style_img,
				'--content_img', content_img,
				'--img_name', output_img,
				'--max_size', str(output_pixel_max),
				'--device', '/gpu:0'],
				capture_output=True, cwd=LIB_PATH)


		if 'skip-original' in style_img:
			pass
		else:	
			subprocess.run(['python', os.path.join(LIB_PATH, LIB),
				'--style_imgs', style_img,
				'--content_img', content_img,
				'--img_name', original_colors_output_img,
				'--max_size', str(output_pixel_max),
				'--original_colors',
				'--device', '/gpu:0'],
				capture_output=True, cwd=LIB_PATH)

		toc = time.time()
		print(f'Elapsed time is {round((toc - tic)/60, 2)} minutes')