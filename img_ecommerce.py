import os
# import shutil
import time
import argparse
# import numpy as np
import subprocess
from PIL import Image, ImageOps


# Instantiate the argument parser object
ap = argparse.ArgumentParser()

# Add the arguments to the parser
ap.add_argument('-sbox', '--sandbox', action='store_true', help='Sandbox is for experiments')
ap.add_argument('-crop', '--crop_image', nargs=1, metavar=('IMAGE_PATH'),	help='')
ap.add_argument('-upsize', '--upsize_image', nargs=2, metavar=('STYLE', 'MOCKUP_NUMBER'),	help='')
ap.add_argument('-upsizeall4096', '--upsize_all_images_to_4096px', nargs=1, metavar=('STYLE'),	help='')
ap.add_argument('-getallar', '--get_all_aspect_ratios', nargs=1, metavar=('STYLE'),	help='')
ap.add_argument('-combinecollage', '--combine_collage_images', action='store_true', help='')
ap.add_argument('-makebannerad', '--make_banner_ad', nargs=3, metavar=('STYLE', 'MOCKUP_NUMBER', 'BANNER_POSITION'), help='')
args = vars(ap.parse_args())
print(f'----- Arguments -----\n{args}\n')

if args['sandbox']:
	print('------- Sandbox --------')
	pass



if args['upsize_image']:
	STYLE = args['upsize_image'][0]
	MOCKUP_NUMBER = args['upsize_image'][1]
	IMAGE_NAME = 'mockup-' + str(MOCKUP_NUMBER) + '.png'
	PRODUCTS_DIRECTORY = 'img/squarespace/website-assets/products/'
	for product_folder in os.listdir(PRODUCTS_DIRECTORY):
		if STYLE in product_folder:
			print(f'Upsizing --- {STYLE} --- {IMAGE_NAME} ')
			subprocess.run(['python', 'python2_image_enlarge.py',
				'--image_name', IMAGE_NAME,
				'--source_folder', os.path.join(PRODUCTS_DIRECTORY, product_folder),
				'--dest_folder', os.path.join(PRODUCTS_DIRECTORY, product_folder)],
				capture_output=True)



if args['get_all_aspect_ratios']:
	STYLE = args['get_all_aspect_ratios'][0]
	PRODUCTS_DIRECTORY = 'img/squarespace/website-assets/products/'
	for product_folder in os.listdir(PRODUCTS_DIRECTORY):
		if STYLE in product_folder:
			for x in range(0,8):
				IMAGE_NAME = STYLE + '-' + str(x) + '-4096.png'
				product_path = os.path.join(PRODUCTS_DIRECTORY, STYLE)
				im = Image.open(os.path.join(product_path, IMAGE_NAME), 'r')
				print(f'{x} - aspect ratio is {max(im.size)/min(im.size)}')


if args['upsize_all_images_to_4096px']:
	STYLE = args['upsize_all_images_to_4096px'][0]
	PRODUCTS_DIRECTORY = 'img/squarespace/website-assets/products/'
	for product_folder in os.listdir(PRODUCTS_DIRECTORY):
		if STYLE in product_folder:
			for x in range(0,10):
				IMAGE_NAME = STYLE + '-' + str(x) + '-4096.png'
				product_path = os.path.join(PRODUCTS_DIRECTORY, STYLE)
				if os.path.exists(os.path.join(product_path, IMAGE_NAME)):
					print(os.path.join(product_path, IMAGE_NAME))
					im = Image.open(os.path.join(product_path, IMAGE_NAME), 'r')
					while max(im.size) < 4096:
								print(f'{x} - Upsizing image {IMAGE_NAME}')
								terminal_output = subprocess.run(['python', 'python2_image_enlarge.py',
									'--image_name', IMAGE_NAME,
									'--source_folder', os.path.join(PRODUCTS_DIRECTORY, product_folder),
									'--dest_folder', os.path.join(PRODUCTS_DIRECTORY, product_folder)],
									capture_output=True)
								# print(terminal_output)
								im = Image.open(os.path.join(product_path, IMAGE_NAME), 'r')





if args['make_collage_banner']:
	STYLE = args['make_collage_banner'][0]






if args['combine_collage_images']:
	PRODUCTS_DIRECTORY = 'img/squarespace/website-assets/collage/1/'
	files = []
	for image in sorted(os.listdir(PRODUCTS_DIRECTORY)):
		if 'combined' in image:
			print(f'Removing {image}')
			os.remove(os.path.join(PRODUCTS_DIRECTORY, image))
		else:
			files.append(image)


	for index, image in enumerate(files):
		# if index >2:
		# 	break
		if (index % 2) == 0:
			continue
		else:
			original_image_path = os.path.join(PRODUCTS_DIRECTORY, image)
			canvas_image_path = os.path.join(PRODUCTS_DIRECTORY, files[index-1])

			im1 = Image.open(original_image_path, 'r')
			im1 = ImageOps.expand(im1, border=150, fill='#EEEEEE')
			im1 = ImageOps.expand(im1, border=50, fill='white')

			im2 = Image.open(canvas_image_path, 'r')
			top = 100
			left = 175
			right = im2.size[1] - 275
			bottom = im2.size[0] - 100
			im2 = im2.crop((left, top, right, bottom))

			im2 = im2.resize(im1.size)

			### combine original and mockup into a new image
			if im1.size[0] > im1.size[1]:  # landscape orientation
				continue
				# im_combined = Image.new('RGB', (im1.size[0],im1.size[1]*2))
				# im_combined.paste(im1, (0,0))
				# im_combined.paste(im2, (0, im1.size[1]))
				
			else:  # portrait orientation
				im_combined = Image.new('RGB', (im1.size[0]*2,im1.size[1]))
				im_combined.paste(im1, (0,0))
				im_combined.paste(im2, (im1.size[0], 0))
				
			# resize combined image			
			height = im_combined.size[0]
			width = im_combined.size[1]
			aspect_ratio = width/height if height>width else height/width

			new_width = 1200
			new_height = int(aspect_ratio*new_width)
			im_combined = im_combined.resize((new_width, new_height))


			im_combined = ImageOps.expand(im_combined, border=75, fill='white')
			FINAL_IMAGE_PATH = canvas_image_path[:-4] + '-combined' + canvas_image_path[-4:]
			print(f'Final Image ------ {FINAL_IMAGE_PATH}')

			im_combined.save(FINAL_IMAGE_PATH)



if args['make_banner_ad']:
	STYLE = args['make_banner_ad'][0]
	MOCKUP_NUMBER = args['make_banner_ad'][1]
	BANNER_POSITION = args['make_banner_ad'][2]
	ICONS_PATH = 'img/squarespace/website-assets/icons/'
	PRODUCTS_DIRECTORY = 'img/squarespace/website-assets/products/'

	for product_style in os.listdir(PRODUCTS_DIRECTORY):

		if STYLE in product_style:
			PRODUCT_PATH = os.path.join(PRODUCTS_DIRECTORY, STYLE)

			ORIGINAL_IMAGE_PATH = os.path.join(PRODUCT_PATH, STYLE + '-' + str(MOCKUP_NUMBER) + '-original.jpg')
			im1 = Image.open(ORIGINAL_IMAGE_PATH, 'r')
			im1 = ImageOps.expand(im1, border=50, fill='#EEEEEE')
			im1 = ImageOps.expand(im1, border=50, fill='white')

			MOCKUP_IMAGE_PATH = os.path.join(PRODUCT_PATH, STYLE + '-' + str(MOCKUP_NUMBER) + '-canvas.jpg')
			im2 = Image.open(MOCKUP_IMAGE_PATH, 'r')

			top = 100
			left = 175
			right = im2.size[1] - 275
			bottom = im2.size[0] - 100 
			im2 = im2.crop((left, top, right, bottom))

			im2 = im2.resize(im1.size)

			print(f'Product Folder --- {PRODUCT_PATH}')
			print(f'Original Image --- {ORIGINAL_IMAGE_PATH}')
			print(f'Mockup Image ----- {MOCKUP_IMAGE_PATH}')

			# combine original and mockup into a new image
			if im1.size[0] > im1.size[1]:  # landscape orientation
				im_combined = Image.new('RGBA', ((im1.size[0]),im1.size[1]*2), (0, 0, 0, 0))
				im_combined.paste(im1, (0,0))
				im_combined.paste(im2, (0, im1.size[1]))
				
			else:  # portrait orientation
				im_combined = Image.new('RGBA', ((im1.size[0]*2),im1.size[1]), (0, 0, 0, 0))
				im_combined.paste(im1, (0,0))
				im_combined.paste(im2, (im1.size[0], 0))
				

			# resize combined image			
			height = im_combined.size[0]
			width = im_combined.size[1]
			aspect_ratio = width/height if height>width else height/width

			new_width = 1200
			new_height = int(aspect_ratio*new_width)
			im_combined = im_combined.resize((new_width, new_height))

			


			if BANNER_POSITION == 'top':
				im_banner = Image.open(os.path.join(ICONS_PATH, 'how-it-works-1200-top.png'), 'r')
				im_final = Image.new('RGBA', ((im_combined.size[0]), im_banner.size[1] + im_combined.size[1]), (0, 0, 0, 0))
				im_final.paste(im_banner, (0,0))
				im_final.paste(im_combined, (0, im_banner.size[1]))
				

			if BANNER_POSITION == 'bottom':
				im_banner = Image.open(os.path.join(ICONS_PATH, 'how-it-works-1200-bottom.png'), 'r')
				im_final = Image.new('RGBA', ((im_combined.size[0]), im_banner.size[1] + im_combined.size[1]), (0, 0, 0, 0))
				im_final.paste(im_banner, (0,im_combined.size[1]))
				im_final.paste(im_combined, (0, 0))
				


			im_final = ImageOps.expand(im_final, border=50, fill='white')
			FINAL_IMAGE_PATH = MOCKUP_IMAGE_PATH[:-4] + '-combined-banner' + MOCKUP_IMAGE_PATH[-4:]
			print(f'Final Image ------ {FINAL_IMAGE_PATH}')

			im_final.save(FINAL_IMAGE_PATH, format="png")



if args['crop_image']:
	for new_aspect_ratio in [1.25, 1.333333333, 1.5]:  # 1.0, 1.25, 1.333333333, 1.4, 1.5, 2.0, 3.0
		IMAGE_PATH = args['crop_image'][0]
		im = Image.open(IMAGE_PATH)
		width, height = im.size
		larger_side = "width" if width > height else "height"
		smaller_side = "height" if width > height else "width"
		current_aspect_ratio = width/height if larger_side == "width"  else height/width

		# determine which side to crop
		if current_aspect_ratio > new_aspect_ratio:
			side_to_crop = "larger"
		elif current_aspect_ratio < new_aspect_ratio:
			side_to_crop = "smaller"
		else:
			side_to_crop = None

		# calculate crop parameters
		if side_to_crop == "larger" and larger_side == "width":
			target_width = new_aspect_ratio * height
			difference = (width - target_width)/2
			left = difference
			top = 0
			right = width - difference
			bottom = height

		elif side_to_crop == "larger" and larger_side == "height":
			target_height = new_aspect_ratio * width
			difference = (height - target_height)/2
			left = 0
			top = difference
			right = width
			bottom = height - difference

		elif side_to_crop == "smaller" and smaller_side == "width":
			target_width =  height / new_aspect_ratio
			difference = (width - target_width)/2
			left = difference
			top = 0
			right = width - difference
			bottom = height 

		elif side_to_crop == "smaller" and smaller_side == "height":
			target_height = width / new_aspect_ratio
			difference = (height - target_height)/2
			left = 0
			top = difference
			right = width
			bottom = height - difference

		else:  # stock pixel dimensions already match a canvas size do not crop
			left = 0
			top = 0
			right = width
			bottom = height

		# generate new image name
		cropped_image_path = IMAGE_PATH[:-4] + '-aspect-ratio-' + str(int(new_aspect_ratio * 100)) + IMAGE_PATH[-4:]
		print(f'--- Cropping --- {cropped_image_path}')
		# crop the image
		cropped_file_size = 0
		quality = 100
		cropped_image = im.crop((left, top, right, bottom))
		cropped_image.save(cropped_image_path, 'PNG', quality = quality)
