import os
from sys import getsizeof
from PIL import Image

# disable decompression bomb DOS attack protection for giga-pixel images
import PIL.Image
PIL.Image.MAX_IMAGE_PIXELS = None


# get image filenames and sort them alphabetically
origin_path = "img/tocrop/"
destination_path = "img/cropped/"
files = os.listdir(origin_path)
files.sort()

# iterate through all images
for src in files:
	im = Image.open(origin_path+src)
	width, height = im.size
	larger_side = "width" if width > height else "height"
	smaller_side = "height" if width > height else "width"
	current_aspect_ratio = width/height if larger_side == "width"  else height/width
	valid_aspect_ratios = [1.0, 1.25, 1.333333333, 1.4, 1.5, 2.0, 3.0]
	closest_aspect_ratio = min(valid_aspect_ratios, key=lambda x:abs(x-current_aspect_ratio))

	# determine which side to crop
	if current_aspect_ratio > closest_aspect_ratio:
		side_to_crop = "larger"
	elif current_aspect_ratio < closest_aspect_ratio:
		side_to_crop = "smaller"
	else:
		side_to_crop = None

	# calculate crop parameters
	if side_to_crop == "larger" and larger_side == "width":
		target_width = closest_aspect_ratio * height
		difference = (width - target_width)/2
		left = difference
		top = 0
		right = width - difference
		bottom = height

	elif side_to_crop == "larger" and larger_side == "height":
		target_height = closest_aspect_ratio * width
		difference = (height - target_height)/2
		left = 0
		top = difference
		right = width
		bottom = height - difference

	elif side_to_crop == "smaller" and smaller_side == "width":
		target_width =  height / closest_aspect_ratio
		difference = (width - target_width)/2
		left = difference
		top = 0
		right = width - difference
		bottom = height 

	elif side_to_crop == "smaller" and smaller_side == "height":
		target_height = width / closest_aspect_ratio
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
	segments = src.split('-')
	segments[-1] = "_aspect_ratio_" + str(int(closest_aspect_ratio * 100)) + ".png"
	src = "-".join(segments)

	# crop the image
	cropped_file_size = 0
	quality = 100
	while cropped_file_size == 0 or cropped_file_size > 50000000:  # ensure final image is less than 50MB
		cropped_image = im.crop((left, top, right, bottom))
		cropped_image.save(destination_path+src, 'PNG', quality = quality)
		cropped_file_size = os.path.getsize(destination_path+src)
		quality -= 1

	# debug
	print(src)
	print("width: {}".format(width))
	print("height: {}".format(height))
	print("current aspect ratio: {}".format(current_aspect_ratio))
	print("closest aspect ratio: {}".format(closest_aspect_ratio))
	print("image quality: {}".format(quality+1))
	print("cropped file size: {}".format(cropped_file_size))
	print("\n")