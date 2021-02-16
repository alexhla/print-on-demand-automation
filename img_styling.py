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

ap.add_argument('-count', '--count_styled_images', action='store_true',
	help='Count number of styled images for each style and subject and display results to the terminal')

ap.add_argument('-move', '--move_from_lib_to_styled_images', action='store_true',
	help='Move images from styling libarary output to styled images storage')

ap.add_argument('-organize', '--organize_styled_images_into_folders', action='store_true',
	help='Organize all newly styled images into their respective style and subject folders')



args = vars(ap.parse_args())
print(f'----- Arguments -----\n{args}\n')


ALL_STYLES = ['abstract', 'cubist', 'impressionist', 'watercolor']
ALL_SUBJECTS = ['buildings', 'cats', 'couples', 'dogs', 'family', 'portraits', 'wedding']

if args['sandbox']:
	print('------- Sandbox --------')
	pass



'''

Count

'''
if args['count_styled_images']:
	print('styled512       combined')
	for style in ALL_STYLES:
		print('')
		for subject in ALL_SUBJECTS:
			styled512_folder_path = 'img/squarespace/styled-images/'+style+'/'+subject+'/styled512/'
			combined_folder_path = 'img/squarespace/styled-images/'+style+'/'+subject+'/combined/'
			print(f'{len(os.listdir(styled512_folder_path))}\t---\t{len(os.listdir(combined_folder_path))}\t{style} {subject}')		




'''

Move

'''
if args['move_from_lib_to_styled_images']:
	SOURCE_DIR = 'lib/neural-style-tf-master/image_output'
	DESTINATION_DIR = 'img/squarespace/styled-images/to-do'
	print(f'source directory is {SOURCE_DIR} of type {type(SOURCE_DIR)}')
	for folder in os.listdir(SOURCE_DIR):
		files = os.listdir(os.path.join(SOURCE_DIR, folder))
		for file in files:
			if 'all-famous-art' in file:
				print(f'\nMoving {file} \nFrom {SOURCE_DIR} \nTo {DESTINATION_DIR}\n')
				x = os.path.join(SOURCE_DIR, folder, file)
				y = os.path.join(DESTINATION_DIR, file)
				os.rename(x, y)

	# remove image holders folders
	for folder in os.listdir(SOURCE_DIR):
		shutil.rmtree(os.path.join(SOURCE_DIR, folder))






'''

Organize

'''
if args['organize_styled_images_into_folders']:
	SOURCE_FOLDER = 'img/squarespace/styled-images/to-do/'
	count = {}

	# ensure all files fall into a category
	for filename in os.listdir(SOURCE_FOLDER):
		count[filename] = 0
		for style in ALL_STYLES:		
			if style in filename:
				for subject in ALL_SUBJECTS:
					if subject in filename:
						count[filename] += 1

	if not any(v == 0 for k,v in count.items()):
		print('Organizing Files...')
		for filename in os.listdir(SOURCE_FOLDER):
			for style in ALL_STYLES:	
				if style in filename:
					for subject in ALL_SUBJECTS:
						if subject in filename:
							destination_folder = 'img/squarespace/styled-images/'+style+'/'+subject+'/styled512'
							shutil.copy(os.path.join(SOURCE_FOLDER, filename), os.path.join(destination_folder, filename))

		# delete original files
		for filename in os.listdir(SOURCE_FOLDER):
			os.remove(os.path.join(SOURCE_FOLDER, filename))
	else:
		print('Error: Organzing the Following Files')
		for k,v in count.items():
			if v == 0:
				print(k)
