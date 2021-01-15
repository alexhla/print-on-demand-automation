import os
import time
import argparse
import numpy as np
import subprocess
import cv2
from PIL import Image

# Instantiate the argument parser object
ap = argparse.ArgumentParser()

# Add the arguments to the parser
ap.add_argument('-upsize', '--upsize_styled_images', action='store_true',
	help='resize all styled images to 2x their current pixel width and height')

ap.add_argument('-downsize', '--downsize_original_image', nargs=1, metavar=('RESIZE_ORIGINAL'),
	help='pixel size of preview of original image that is overlayed onto final product photo')

ap.add_argument('-border', '--add_border', nargs=1, metavar=('ADD_BORDER'),
	help='border size of original image that is overlayed onto final product photo')

ap.add_argument('-pp', '--place_preview', nargs=1, metavar=('PLACE_PREVIEW'),
	help='where the original image preview is to be overlayed on the final product photo (topleft, topmiddle, topright, bottomleft, bottommiddle, bottom right)')

ap.add_argument('-pw', '--place_watermark', nargs=1, metavar=('PLACE_WATERMARK'),
	help='where the watermark overlayed on the final product photo (topleft, topmiddle, topright, bottomleft, bottommiddle, bottom right)')

args = vars(ap.parse_args())
print(f'----- Arguments -----\n{args}\n')


# paths
ORIGINAL_IMAGE_FOLDER = 'img/inprogress/original/'
PRODUCT_IMAGE_FOLDER = 'img/inprogress/product/'
WATERMARK_IMAGE_PATH = 'img/inprogress/watermark/watermark.png'
STYLED_IMAGE_FOLDER = 'img/inprogress/styled/'
STYLED2X_IMAGE_FOLDER = 'img/inprogress/styled2x/'

if args['upsize_styled_images']:
	for filename in os.listdir(STYLED2X_IMAGE_FOLDER):
		os.remove(os.path.join(STYLED2X_IMAGE_FOLDER, filename))
		
	for filename in os.listdir(STYLED_IMAGE_FOLDER):
		print(f'resizing styled file {filename}')
		subprocess.run(['python', 'python2_image_enlarge.py',
			'--image_name', filename,
			'--source_folder', STYLED_IMAGE_FOLDER,
			'--dest_folder', STYLED2X_IMAGE_FOLDER], capture_output=True)


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


if args['add_border']:
	for filename in os.listdir(ORIGINAL_IMAGE_FOLDER):
		if 'bordered' not in filename:
			if 'preview' in filename:
				im = cv2.imread(os.path.join(ORIGINAL_IMAGE_FOLDER, filename))

				BORDER_SIZE = int(args['add_border'][0])
				top = bottom = left = right = BORDER_SIZE

				print(f'Adding {BORDER_SIZE}px Border to {filename}')
				bordered_image = cv2.copyMakeBorder(im, top=top, bottom=bottom, left=left, right=right,
											borderType=cv2.BORDER_CONSTANT,
											value=[255,255,255])

				BORDERED_FILENAME = filename[:-4] + '_bordered' + filename[-4:]
				BORDERED_IMAGE_PATH = os.path.join(ORIGINAL_IMAGE_FOLDER, BORDERED_FILENAME)
				cv2.imwrite(BORDERED_IMAGE_PATH, bordered_image)


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