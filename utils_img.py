# Install Dependencies (Linux):
# $ pip3 install argparse numpy matplotlib opencv-python opencv-contrib-python

import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
import cv2

# Instantiate the argument parser object
ap = argparse.ArgumentParser()

# Add the arguments to the parser
ap.add_argument('-d', '--directory', nargs=1, metavar=('DIRECTORY'), help='path to directory of images')
ap.add_argument('-di', '--directory_info', action='store_true', help='get info on images in directory')

ap.add_argument('-m', '--move_files', nargs=2, metavar=('SOURCE_DIR', 'DESTINATION_DIR'),
	help='move files from all subdirectories in SOURCE_DIR to DESTINATION_DIR')

ap.add_argument('-fd', '--find_duplicates', action='store_true', help='find duplicate images in directory')
ap.add_argument('-i', '--image_info', nargs=1, metavar=('INDEX'), help='get info on image at given index')
ap.add_argument('-b', '--add_border', nargs=3, metavar=('FILENAME', 'BORDER_SIZE', 'BORDER_COLOR'),
	help='add border to image at the given INDEX with the specified BORDER_SIZE and BORDER_COLOR')

ap.add_argument('-r', '--resize_image', nargs=2, metavar=('INDEX', 'MAX'),
	help='resize image at the given INDEX to the specified pixel MAX; maintaining aspect ratio')

ap.add_argument('-rall', '--resize_all_images_in_directory', nargs=1, metavar=('MAX'),
	help='resize all images in the given directory to the specified pixel MAX; maintaining aspect ratios')

ap.add_argument('-stretch', '--stretch_image', nargs=3, metavar=('INDEX','HEIGHT','WIDTH'),
	help='stretch image at the given index to the specified dimensions; disregarding aspect ratio')

ap.add_argument('-pad', '--pad_image', nargs=4, metavar=('INDEX','FILL','HEIGHT','WIDTH'),
	help='pad image at INDEX with FILL (white | black | reflect) to meet the specified WIDTH and HEIGHT pixel dimensions; maintaining aspect ratio')

ap.add_argument('-padall', '--pad_all_images_in_directory', nargs=3, metavar=('FILL','HEIGHT','WIDTH'),
	help='pad all images in the given directory with FILL (white | black | reflect) to meet the specified WIDTH and HEIGHT pixel dimensions; maintaining aspect ratio')

ap.add_argument('-s', '--show_image', nargs=1, metavar=('INDEX'), help='show the image at INDEX`')
ap.add_argument('-sbgr', '--show_bgr', nargs=1, metavar=('INDEX'), help='show bgr channels of the image at INDEX')
ap.add_argument('-scym', '--show_cym', nargs=1, metavar=('INDEX'), help='show cyan (bg), yellow (gr), magenta (rb) channels of the image at INDEX')

ap.add_argument('-add', '--add_images', nargs=2, metavar=('INDEX1','INDEX2'),
	help='add the images at INDEX1 and INDEX2; equalizing pixel dimensions by cropping the larger image')

# parse user arguments
args = vars(ap.parse_args())
print(f'argparse arguments: {args}')


if args['directory']:
	folder_path = args['directory'][0]
	files = os.listdir(folder_path)
	print(f'argparse arguments: {args}')
	print(f'\n{len(files)} images found in {folder_path}')
	print(f'files are {files}')


if args['move_files']:
	SOURCE_DIR = args['move_files'][0]
	DESTINATION_DIR = args['move_files'][1]

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
	SOURCE_FILENAME = args['add_border'][0]
	BORDER_SIZE = int(args['add_border'][1])
	BORDER_COLOR = args['add_border'][2]

	NEW_FILENAME = SOURCE_FILENAME[:-4] + '-bordered.jpg'
	im = cv2.imread(os.path.join(folder_path, SOURCE_FILENAME))

	top = bottom = left = right = BORDER_SIZE
	border = cv2.copyMakeBorder(im, top=top, bottom=bottom, left=left, right=right,
								borderType=cv2.BORDER_CONSTANT,
								value=[255,255,255])
	
	cv2.imwrite(os.path.join(folder_path, NEW_FILENAME), border)


if args['find_duplicates']:
	hashDict = {}
	hashSize = 8
	for index, filename in enumerate(files):

		im = cv2.imread(os.path.join(folder_path, filename))  # read file
		gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)  # convert to gray
		resized = cv2.resize(im, (hashSize + 1, hashSize))  # resize to 9x8 pixels
		diff = resized[:, 1:] > resized[:, :-1]
		im_hash =  sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])
		print(im_hash)

		if im_hash in hashDict:
			hashDict[im_hash] += 1
		else:
			hashDict[im_hash] = 1

	hashDict_sorted = dict(sorted(hashDict.items()))
	print(f'\nImage Count by Hash Sorted: {hashDict_sorted}')


if args['pad_all_images_in_directory']:
	fill_type = args['pad_all_images_in_directory'][0]
	desired_height = int(args['pad_all_images_in_directory'][1])
	desired_width = int(args['pad_all_images_in_directory'][2])

	for index, filename in enumerate(os.listdir(folder_path)):
		print(f'\nPadding image at index {index} with fill type ({fill_type}) to pixel dimensions ({desired_width}, {desired_height})')

		im = cv2.imread(os.path.join(folder_path, filename))
		height = im.shape[0]
		width = im.shape[1]
		print(f'\nShape of image is {im.shape}')

		# calculate pixel paddings for each side of the image
		top = bottom = left = right = 0
		if height <= desired_height:
			top = bottom = (desired_height - height) // 2
		if width <= desired_width:
			left = right = (desired_width - width) // 2

		# add pixels lost during integer division with odd numbers
		if desired_height != top + height + bottom:
			top += (desired_height - (top + height + bottom))
		if desired_width != left + width + right:
			left += (desired_width - (left + width + right))

		print(f'\nPadding pixel widths are as follows top:{top}, bottom:{bottom}, left:{left}, right:{right}')
		im_padded = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_REFLECT, 0)

		print(f'\nShape of padded image is {im_padded.shape}')
		print(f'\nSaving {filename} to current directory')

		folder_name = str(desired_height) + 'x' + str(desired_width)

		if not os.path.isdir(folder_name):
			os.mkdir(folder_name)

		cv2.imwrite(os.path.join(folder_name, filename), im_padded)


if args['pad_image']:
	index = args['pad_image'][0]
	fill_type = args['pad_image'][1]
	desired_height = int(args['pad_image'][2])
	desired_width = int(args['pad_image'][3])
	filename = files[int(index)]
	new_filename = 'padded_' + str(desired_height) + 'x' + str(desired_width)  + '_' +  filename
	print(f'\nPadding image at index {index} with fill type ({fill_type}) to pixel dimensions ({desired_width}, {desired_height})')

	im = cv2.imread(os.path.join(folder_path, filename))
	height = im.shape[0]
	width = im.shape[1]
	print(f'\nShape of image is {im.shape}')

	# calculate pixel paddings for each side of the image
	top = bottom = left = right = 0
	if height <= desired_height:
		top = bottom = (desired_height - height) // 2
	if width <= desired_width:
		left = right = (desired_width - width) // 2

	# add pixels lost during integer division with odd numbers
	if desired_height != top + height + bottom:
		top += (desired_height - (top + height + bottom))
	if desired_width != left + width + right:
		left += (desired_width - (left + width + right))

	print(f'\nPadding pixel widths are as follows top:{top}, bottom:{bottom}, left:{left}, right:{right}')
	im_padded = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_REFLECT, 0)

	print(f'\nShape of padded image is {im_padded.shape}')
	print(f'\nSaving {new_filename} to current directory')
	cv2.imwrite(new_filename, im_padded)


if args['resize_image']:
	index = args['resize_image'][0]
	pixel_max = args['resize_image'][1]
	filename = files[int(index)]
	new_filename = 'resize_' + str(pixel_max) + '_' +filename
	
	print(f'\nImage {filename} at index {index} to be resized with pixel maximum {pixel_max}')
	im = cv2.imread(os.path.join(folder_path, filename))
	old_size = im.shape[:2] # old_size is in (height, width) format
	ratio = float(pixel_max)/max(old_size)
	new_size = tuple([int(x*ratio) for x in old_size])
	
	print(f'\nResizing to new pixel dimensions: {new_size}')
	im = cv2.resize(im, (new_size[1], new_size[0]))
	print(f'\nSaving {new_filename} to current directory')
	cv2.imwrite(new_filename, im)


if args['resize_all_images_in_directory']:
	pixel_max = args['resize_all_images_in_directory'][0]
	for index, filename in enumerate(files):
		print(f'Index {index} points to {filename}')
		im = cv2.imread(os.path.join(folder_path, filename))
		old_size = im.shape[:2] # old_size is in (height, width) format
		ratio = float(pixel_max)/max(old_size)
		new_size = tuple([int(x*ratio) for x in old_size])
		
		print(f'\nResizing to new pixel dimensions: {new_size}')
		im = cv2.resize(im, (new_size[1], new_size[0]))
		print(f'\nSaving image to {pixel_max}/{filename}')

		if not os.path.isdir(pixel_max):
			os.mkdir(pixel_max)

		cv2.imwrite(os.path.join(pixel_max, filename), im)

if args['image_info']:
	index = args['image_info'][0]
	filename = files[int(index)]
	im = cv2.imread(os.path.join(folder_path, filename))
	print(f'\nFile: {filename} {type(im)}')
	print(f'Image dtype: {im.dtype}')
	print(f'Image size (pixels): {im.size}')	
	print(f'Image Shape: {im.shape}')
	print(f'Image Height: {im.shape[0]}')
	print(f'Image Width: {im.shape[1]}')
	print(f'Number of Channels: {im.shape[2]}')
	cv2.imshow('', im)
	cv2.waitKey(5000)
	cv2.destroyAllWindows()


if args['add_images']:
	index1 = int(args['add_images'][0])
	index2 = int(args['add_images'][1])
	im1 = cv2.imread(os.path.join(folder_path, files[index1]))
	im2 = cv2.imread(os.path.join(folder_path, files[index2]))
	h = min(im1.shape[0], im2.shape[0])
	w =  min(im1.shape[1], im2.shape[1])
	im1_cropped = im1[0:h, 0:w]  # crop to match image dimensions, preserving aspect ratio but losing content
	im2_cropped = im2[0:h, 0:w]
	im_sum = cv2.add(im1_cropped, im2_cropped)
	cv2.imshow('', im_sum)
	cv2.waitKey(10000)
	cv2.destroyAllWindows()


if args['show_image']:
	index = int(args['show_image'][0])
	im = cv2.imread(os.path.join(folder_path, files[index]))
	cv2.imshow('', im)
	cv2.waitKey(5000)
	cv2.destroyAllWindows()


if args['show_bgr']:
	index = int(args['show_bgr'][0])
	im = cv2.imread(os.path.join(folder_path, files[index]))
	b,g,r = cv2.split(im)
	z = np.zeros(b.shape, dtype=np.uint8)
	b = cv2.merge((b, g, z))
	g = cv2.merge((z, g, z))
	r = cv2.merge((z, z, r))
	cv2.imshow("im-b", b)
	cv2.imshow("im-g", g)
	cv2.imshow("im-r", r)
	cv2.waitKey(10000)  
	cv2.destroyAllWindows()  


if args['show_cym']:
	index = int(args['show_cym'][0])
	im = cv2.imread(os.path.join(folder_path, files[index]))
	b,g,r = cv2.split(im)
	z = np.zeros(b.shape, dtype=np.uint8)
	bg = cv2.merge((b, g, z))
	gr = cv2.merge((z, g, r))
	rb = cv2.merge((b, z, r))
	cv2.imshow("im-bg (cyan)", bg)
	cv2.imshow("im-gr (yellow)", gr)
	cv2.imshow("im-rb (magenta)", rb)
	cv2.waitKey(10000)  
	cv2.destroyAllWindows()  


if args['directory_info']:
	image_count_by_shape = {}
	image_count_by_height = {}
	image_count_by_width = {}
	image_count_by_channels = {}

	for index, filename in enumerate(files):

		# if index > 10:  # batch size for testing
		# 	cv2.imshow("im",im)
		# 	cv2.waitKey(5000)  
		# 	cv2.destroyAllWindows()  
		# 	break

		im = cv2.imread(os.path.join(folder_path, files[index]))

		height = im.shape[0]
		width = im.shape[1]
		channels = im.shape[2]

		print(f'\nFile: {filename} {type(im)}')
		print(f'Image dtype: {im.dtype}')
		print(f'Image size (pixels): {im.size}')	
		print(f'Image Shape: {im.shape}')
		print(f'Image Height: {im.shape[0]}')
		print(f'Image Width: {im.shape[1]}')
		print(f'Number of Channels: {im.shape[2]}')

		# tally images by im.shape
		if im.shape in image_count_by_shape:
			image_count_by_shape[im.shape] += 1
		else:
			image_count_by_shape[im.shape] = 1

		# tally images by width
		if width in image_count_by_width:
			image_count_by_width[width] += 1
		else:
			image_count_by_width[width] = 1

		# tally images by height
		if height in image_count_by_height:
			image_count_by_height[height] += 1
		else:
			image_count_by_height[height] = 1

		# tally images by channels
		if channels in image_count_by_channels:
			image_count_by_channels[channels] += 1
		else:
			image_count_by_channels[channels] = 1

	print(f'\nImage Count by Pixel Dimensions: {image_count_by_shape}')
	print(f'\nImage Count by Pixel Width: {image_count_by_width}')
	print(f'\nImage Count by Pixel Height: {image_count_by_height}')
	print(f'\nImage Count by Pixel Channels: {image_count_by_channels}')

	image_count_by_sorted_width = dict(sorted(image_count_by_width.items()))
	image_count_by_sorted_height = dict(sorted(image_count_by_height.items()))

	# print(f'\nImage Count by Pixel Height Sorted: {image_count_by_sorted_width}')
	# print(f'\nImage Count by Pixel Width Sorted: {image_count_by_sorted_height}')

	width_keys = [str(key) for key in image_count_by_sorted_width.keys()]
	height_keys = [str(key) for key in image_count_by_sorted_height.keys()]

	width_values = image_count_by_sorted_width.values()
	height_values = image_count_by_sorted_height.values()

	fig = plt.figure(figsize = (12.8, 7.2))
	fig.suptitle(f'Image Distribution by Resolution'
				+f'\nDirectory: {args["directory"][0]}'
				+f'\nNumber of Images: {len(files)}')
	
	ax1 = fig.add_subplot(211)
	ax1.set_ylabel('Files per Pixel Width')
	ax1.set_xticks(np.linspace(0, len(width_keys)-1, 10))
	ax1.bar(width_keys, width_values, color = 'seagreen')
	
	ax2 = fig.add_subplot(212)	
	ax2.set_ylabel('Files per Pixel Height')
	ax2.set_xticks(np.linspace(0, len(height_keys)-1, 10))
	ax2.bar(height_keys, height_values, color = 'steelblue')
	
	plt.savefig('plots/image_distribution_by_resolution_'+ f'{args["directory"][0].replace("/","_")[:-1]}' + '.png')
	plt.show()