import os
import shutil
import time
import argparse
import numpy as np
import subprocess
import cv2
from PIL import Image


# Instantiate the argument parser object
ap = argparse.ArgumentParser()

# Add the arguments to the parser
ap.add_argument('-sbox', '--sandbox', action='store_true',
	help='Sandbox is for running prototype code and tests')

ap.add_argument('-upsize', '--upsize_images', nargs=3, metavar=('ITERATIONS', 'SOURCE_DIRECTORY', 'destination_folder'),
	help='Upsize images in the SOURCE_DIRECTORY doubling in size for each of the specified ITERATIONS and storing the results in the destination_folder')

ap.add_argument('-combine', '--combine_images', nargs=3, metavar=('BEFORE_DIRECTORY', 'AFTER_DIRECTORY', 'destination_folder'),
	help='Combine all images in the BEFORE_DIRECTORY with all similarly named images in the AFTER_DIRECTORY placing them side by side and storing the resulting image in the destination_folder')

ap.add_argument('-banner', '--add_banner_to_images', nargs=3, metavar=('BANNER_PATH', 'SOURCE_DIRECTORY', 'destination_folder'),
	help='Add banner specified by BANNER_PATH to all images in the SOURCE_DIRECTORY storing the results in the destination_folder')

ap.add_argument('-padding', '--pad_images', nargs=6, metavar=('TOP', 'BOTTOM', 'LEFT', 'RIGHT', 'SOURCE_DIRECTORY', 'destination_folder'),
	help='Add padding per TOP, BOTTOM, LEFT, RIGHT to all images in the SOURCE_DIRECTORY storing the results in the destination_folder')

ap.add_argument('-create', '--create_product_images', action='store_true',
	help='Upsize, create, combine, padding, banner on all images of a certain style and subject')

ap.add_argument('-organize', '--organize_images', action='store_true',
	help='Organize all new files into their respective style and subject folders')

ap.add_argument('-count', '--count_styled_images', action='store_true',
	help='Count number of styled images for each style and subject and display results to the terminal')

ap.add_argument('-move', '--move_from_lib_to_product_images', action='store_true',
	help='')

ap.add_argument('-compare', '--compare_folders', action='store_true',
	help='')


ap.add_argument('-back_delete_from_combined', '--back_delete_from_combined', nargs=2, metavar=('STYLE', 'SUBJECT'),
	help='')

ap.add_argument('-border', '--add_border', nargs=5, metavar=('FILE_PATH', 'BORDER_SIZE', 'BORDER_COLOR_RED', 'BORDER_COLOR_GREEN', 'BORDER_COLOR_BLUE'),
	help='border size of original image that is overlayed onto final product photo')





ap.add_argument('-downsize', '--downsize_original_image', nargs=1, metavar=('RESIZE_ORIGINAL'),
	help='pixel size of preview of original image that is overlayed onto final product photo')

ap.add_argument('-pp', '--place_preview', nargs=1, metavar=('PLACE_PREVIEW'),
	help='where the original image preview is to be overlayed on the final product photo (topleft, topmiddle, topright, bottomleft, bottommiddle, bottom right)')

ap.add_argument('-pw', '--place_watermark', nargs=1, metavar=('PLACE_WATERMARK'),
	help='where the watermark overlayed on the final product photo (topleft, topmiddle, topright, bottomleft, bottommiddle, bottom right)')

args = vars(ap.parse_args())
print(f'----- Arguments -----\n{args}\n')

ALL_STYLES = ['abstract', 'illustration', 'cubist', 'impressionist', 'postimpressionist', 'sketch', 'watercolor']
ALL_SUBJECTS = ['cats', 'couples', 'dogs', 'family', 'self-portraits', 'wedding']


if args['sandbox']:
	print('------- Sandbox --------')


if args['move_from_lib_to_product_images']:
	SOURCE_DIR = 'lib/neural-style-tf-master/image_output'
	DESTINATION_DIR = 'img/squarespace/product-images/to-do'

	print(f'source directory is {SOURCE_DIR} of type {type(SOURCE_DIR)}')
	for folder in os.listdir(SOURCE_DIR):
		files = os.listdir(os.path.join(SOURCE_DIR, folder))
		for file in files:
			# optional final condition to move file
			if 'all-famous-art' in file:
				print(f'\nMoving {file} \nFrom {SOURCE_DIR} \nTo {DESTINATION_DIR}\n')
				x = os.path.join(SOURCE_DIR, folder, file)
				y = os.path.join(DESTINATION_DIR, file)
				os.rename(x, y)



if args['add_border']:
	FILE_PATH = args['add_border'][0]
	BORDER_SIZE = int(args['add_border'][1])
	BORDER_COLOR_RED = int(args['add_border'][2])
	BORDER_COLOR_GREEN = int(args['add_border'][3])
	BORDER_COLOR_BLUE = int(args['add_border'][4])

	if not os.path.isfile(FILE_PATH):
		print(f'Error: File Not Found {FILE_PATH}')
	else:
		im = cv2.imread(FILE_PATH)
		top = bottom = left = right = BORDER_SIZE

		print(f'Adding {BORDER_SIZE}px Border to {FILE_PATH}')
		bordered_image = cv2.copyMakeBorder(im, top=top, bottom=bottom, left=left, right=right,
									borderType=cv2.BORDER_CONSTANT,
									value=[BORDER_COLOR_RED, BORDER_COLOR_GREEN, BORDER_COLOR_GREEN])

		BORDERED_FILE_PATH = FILE_PATH[:-4] + '-bordered-' + str(BORDER_SIZE) + '-' + str(BORDER_COLOR_RED) + '-' + str(BORDER_COLOR_GREEN) +  '-'  + str(BORDER_COLOR_BLUE) + FILE_PATH[-4:]
		cv2.imwrite(BORDERED_FILE_PATH, bordered_image)



if args['back_delete_from_combined']:
	STYLE = args['back_delete_from_combined'][0]
	SUBJECT = args['back_delete_from_combined'][1]
	COMBINED_FOLDER = 'img/squarespace/product-images/'+STYLE+'/'+SUBJECT+'/combined/'
	
	files_to_save = {}
	for filename in os.listdir(COMBINED_FOLDER):
		# print(f'Save: {filename}')
		files_to_save[filename] = True

	for folder in ['styled512','styled1024','padded','banner']:
		destination_folder = 'img/squarespace/product-images/'+STYLE+'/'+SUBJECT+'/'+folder+'/'
		print(f'destination folder is {destination_folder}')
		for filename in os.listdir(destination_folder):
			if filename not in files_to_save:
				print(f'removing {os.path.join(destination_folder, filename)}')
				os.remove(os.path.join(destination_folder, filename))


if args['place_watermark']:
	for filename in os.listdir(PRODUCT_IMAGE_FOLDER):
		watermark_image = Image.open(WATERMARK_IMAGE_PATH, 'r')
		styled_img = Image.open(os.path.join(PRODUCT_IMAGE_FOLDER, filename), 'r')
		placement = args['place_watermark'][0]

		if placement == 'topleft':
			x1 = y1 = 0

		elif placement == 'topright':
			x1 = styled_img.size[0] - watermark_image.size[0]
			y1 = 0

		elif placement == 'bottomleft':
			x1 = 0
			y1 = styled_img.size[1] - watermark_image.size[1]

		elif placement == 'bottomright':
			x1 = styled_img.size[0] - watermark_image.size[0]
			y1 = styled_img.size[1] - watermark_image.size[1]

		else:
			print('Error: Invalid Watermark Placement')
			continue

		# print(f'x1, y1 = {x1}, {y1}')
		text_img = Image.new('RGBA', (styled_img.size[0],styled_img.size[1]), (0, 0, 0, 0))
		text_img.paste(styled_img, (0,0))
		text_img.paste(watermark_image, (x1,y1), mask=watermark_image)
		text_img.save(PRODUCT_IMAGE_FOLDER+filename, format="png")


if args['compare_folders']:
	for style in ALL_STYLES:
			for subject in ALL_SUBJECTS:
					destination_folder = 'img/squarespace/product-images/'+style+'/'+subject+'/styled512/'
					style512_files = os.listdir(destination_folder)

					destination_folder = 'img/squarespace/product-images/'+style+'/'+subject+'/combined/'
					combined_files = os.listdir(destination_folder)

					print(f'{style} | {subject} | {set(style512_files) - set(combined_files)}\n')


if args['count_styled_images']:
	print('styled512 --- combined')
	for style in ALL_STYLES:
			for subject in ALL_SUBJECTS:
					styled512_folder_path = 'img/squarespace/product-images/'+style+'/'+subject+'/styled512/'
					combined_folder_path = 'img/squarespace/product-images/'+style+'/'+subject+'/combined/'
					print(f'{len(os.listdir(styled512_folder_path))}\t---\t{len(os.listdir(combined_folder_path))}\t{style} {subject}')		


if args['organize_images']:
	SOURCE_FOLDER = 'img/squarespace/product-images/to-do/'
	for filename in os.listdir(SOURCE_FOLDER):
		for style in ALL_STYLES:
			if style in filename:
				for subject in ALL_SUBJECTS:
					if subject in filename:
						destination_folder = 'img/squarespace/product-images/'+style+'/'+subject+'/styled512'
						print(f'Copying image {filename} to {style} | {subject}')
						shutil.copy(os.path.join(SOURCE_FOLDER, filename), os.path.join(destination_folder, filename))

	# organized files were copied, delete the originals
	for filename in os.listdir(SOURCE_FOLDER):
		os.remove(os.path.join(SOURCE_FOLDER, filename))


if args['create_product_images']:
		for style in ALL_STYLES:
				for subject in ALL_SUBJECTS:

					print(f'Upsizing --- {style} --- {subject}')
					styled512_folder = 'img/squarespace/product-images/'+style+'/'+subject+'/styled512/'
					styled1024_folder = 'img/squarespace/product-images/'+style+'/'+subject+'/styled1024/'
					log = subprocess.run(['python3', 'create_product_photo.py',
						'-upsize', '1', styled512_folder, styled1024_folder], capture_output=True)	
					# print(log)

					print(f'Combining --- {style} --- {subject}')
					stock_photos_folder = 'img/squarespace/stock-photos'
					combined_folder = 'img/squarespace/product-images/'+style+'/'+subject+'/combined/'
					log = subprocess.run(['python3', 'create_product_photo.py',
						'-combine', stock_photos_folder, styled1024_folder, combined_folder], capture_output=True)	
					# print(log)


					print(f'Padding --- {style} --- {subject}')
					padding_folder = 'img/squarespace/product-images/'+style+'/'+subject+'/thumbnail/'
					log = subprocess.run(['python3', 'create_product_photo.py',
						'-padding', '200', '200', '0', '0', combined_folder, padding_folder], capture_output=True)	
					# print(log)


					print(f'Adding Banner --- {style} --- {subject}')
					banner_path = 'img/squarespace/website-assets/how-it-works/how-it-works.png'
					banner_folder = 'img/squarespace/product-images/'+style+'/'+subject+'/banner/'
					log = subprocess.run(['python3', 'create_product_photo.py',
						'-banner', banner_path, combined_folder, banner_folder], capture_output=True)	
					# print(log)


if args['pad_images']:
	TOP = int(args['pad_images'][0])
	BOTTOM = int(args['pad_images'][1])
	LEFT = int(args['pad_images'][2])
	RIGHT = int(args['pad_images'][3])
	SOURCE_DIRECTORY = args['pad_images'][4]
	destination_folder = args['pad_images'][5]

	for image in os.listdir(SOURCE_DIRECTORY):
		if image in os.listdir(destination_folder):
			print(f'Error: Padded image already exists\n{image}\n')
			continue
		im = Image.open(os.path.join(SOURCE_DIRECTORY, image), 'r')

		if im.size[0] > im.size[1]:  # landscape orientation
			final_image = Image.new('RGBA', (LEFT + im.size[0] + RIGHT, TOP + im.size[1] + BOTTOM), (0, 0, 0, 0))
			final_image.paste(im, (0 + LEFT, 0 + TOP))
		else:  # portrait orientation
			final_image = Image.new('RGBA', (TOP + im.size[0] + BOTTOM, LEFT + im.size[1] + RIGHT), (0, 0, 0, 0))
			final_image.paste(im, (0 + TOP, 0 + LEFT))

		print(f'Saving Image with Padding to {os.path.join(destination_folder, image)}')
		final_image.save(os.path.join(destination_folder, image), format="png")


if args['add_banner_to_images']:
	BANNER_PATH = args['add_banner_to_images'][0]
	SOURCE_DIRECTORY = args['add_banner_to_images'][1]
	destination_folder = args['add_banner_to_images'][2]

	for image in os.listdir(SOURCE_DIRECTORY):
		if image in os.listdir(destination_folder):
			print(f'Error: Ad on bottom image already exists\n{image}\n')
			continue
		im = Image.open(os.path.join(SOURCE_DIRECTORY, image), 'r')
		banner = Image.open(BANNER_PATH, 'r')

		if im.size[0] > im.size[1]:  # landscape orientation
			
			aspect_ratio_of_banner = banner.size[0] / banner.size[1]
			new_banner_height = int(im.size[0] / aspect_ratio_of_banner)
			banner = banner.resize((im.size[0], new_banner_height))
			final_image = Image.new('RGBA', ((im.size[0]),im.size[1] + new_banner_height), (0, 0, 0, 0))
			final_image.paste(im, (0,0))
			final_image.paste(banner, (0, im.size[1]))

			print(f'Saving Image with Banner to {os.path.join(destination_folder, image)}')
			final_image.save(os.path.join(destination_folder, image), format="png")


if args['upsize_images']:
	ITERATIONS = int(args['upsize_images'][0])
	SOURCE_DIRECTORY = args['upsize_images'][1]
	destination_folder = args['upsize_images'][2]
		
	for image in os.listdir(SOURCE_DIRECTORY):
		if image in os.listdir(destination_folder):
			print(f'Error: upsized image already exists\n{image}\n')
			continue
		for iteration in range(0, ITERATIONS):
			print(f'Upsizing image {image} on iteration {iteration}')
			subprocess.run(['python', 'python2_image_enlarge.py',
				'--image_name', image,
				'--source_folder', SOURCE_DIRECTORY,
				'--dest_folder', destination_folder], capture_output=True)


if args['combine_images']:
	BEFORE_DIRECTORY = args['combine_images'][0]
	AFTER_DIRECTORY = args['combine_images'][1]
	destination_folder = args['combine_images'][2]

	before_images = os.listdir(BEFORE_DIRECTORY)
	after_images = os.listdir(AFTER_DIRECTORY)

	# print(f'Before Images --- {before_images}\n')
	# print(f'After Images --- {after_images}\n')

	for bfimg in before_images:
		for afimg in after_images:
			if afimg in os.listdir(destination_folder):
				print(f'Error: combined image already exists\n{afimg}\n')
				continue				
			if bfimg[:-4] in afimg:
				print(f'Before Image --- {bfimg}')
				before = Image.open(os.path.join(BEFORE_DIRECTORY, bfimg), 'r')
				
				print(f'After Image ---- {afimg}\n')
				after = Image.open(os.path.join(AFTER_DIRECTORY, afimg), 'r')
				
				before = before.resize(after.size)

				if before.size[0] > before.size[1]:  # landscape orientation
					final_image = Image.new('RGBA', ((before.size[0]),before.size[1]*2), (0, 0, 0, 0))
					final_image.paste(before, (0,0))
					final_image.paste(after, (0, before.size[1]))

				else:  # portrait orientation
					final_image = Image.new('RGBA', ((before.size[0]*2),before.size[1]), (0, 0, 0, 0))
					final_image.paste(before, (0,0))
					final_image.paste(after, (before.size[0], 0))


				print(f'Saving Combined Image to {os.path.join(destination_folder, afimg)}')
				final_image.save(os.path.join(destination_folder, afimg), format="png")


if args['downsize_original_image']:
	for filename in os.listdir(ORIGINAL_IMAGE_FOLDER):
			if 'preview' not in filename:
				# resize
				im = cv2.imread(os.path.join(ORIGINAL_IMAGE_FOLDER, filename))
				old_size = im.shape[:2] # old_size is in (height, width) format
				pixel_max = int(args['downsize_original_image'][0])
				ratio = float(pixel_max)/max(old_size)
				new_size = tuple([int(x*ratio) for x in old_size])
				
				print(f'\n{filename} to be resized with pixel maximum {pixel_max}')
				im_preview = cv2.resize(im, (new_size[1], new_size[0]))

				PREVIEW_FILENAME = filename[:-4] + '_preview' + filename[-4:]
				PREVIEW_IMAGE_PATH = os.path.join(ORIGINAL_IMAGE_FOLDER, PREVIEW_FILENAME)
				cv2.imwrite(PREVIEW_IMAGE_PATH, im_preview)


if args['place_preview']:

	PREVIEW_IMAGE_PATH = ''
	for filename in os.listdir(ORIGINAL_IMAGE_FOLDER):
		for part_of_filename in filename.split():
			if 'preview_bordered.' in part_of_filename:
				PREVIEW_IMAGE_PATH = os.path.join(ORIGINAL_IMAGE_FOLDER, filename) # get preview image

	for filename in os.listdir(STYLED2X_IMAGE_FOLDER):
		preview_image = cv2.imread(PREVIEW_IMAGE_PATH)
		styled_img = cv2.imread(os.path.join(STYLED2X_IMAGE_FOLDER, filename))

		# print(f'\nstyled image shape is {styled_img.shape}')
		# print(f'preview image shape is {preview_image.shape}\n')

		placement = args['place_preview'][0]

		if placement == 'topleft':
			y1 = x1 = 0
			y2 = preview_image.shape[0]
			x2 = preview_image.shape[1]

		elif placement == 'topright':
			y1 = 0
			x1 = styled_img.shape[1] - preview_image.shape[1]
			y2 = preview_image.shape[0]
			x2 = styled_img.shape[1]

		elif placement == 'topmiddle':
			y1 = 0
			x1 = int(styled_img.shape[1]/1.83) - (preview_image.shape[1]//2)
			y2 = preview_image.shape[0]
			x2 = x1 + preview_image.shape[1]

		elif placement == 'bottomleft':
			y1 = styled_img.shape[0] - preview_image.shape[0]
			x1 = 0
			y2 = styled_img.shape[0]
			x2 = preview_image.shape[1]

		elif placement == 'bottomright':
			y1 = styled_img.shape[0] - preview_image.shape[0]
			x1 = styled_img.shape[1] - preview_image.shape[1]
			y2 = styled_img.shape[0]
			x2 = styled_img.shape[1]

		else:
			print('Error: Invalid Preview Placement')
			continue

		# print(f'y1, y2 = {y1}, {y2}')
		# print(f'x1, x2 = {x1}, {x2}')
		styled_img[y1:y2, x1:x2 ] = preview_image
		PRODUCT_IMAGE_PATH = os.path.join(PRODUCT_IMAGE_FOLDER, filename)
		cv2.imwrite(PRODUCT_IMAGE_PATH, styled_img)