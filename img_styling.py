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

ap.add_argument('-move', '--move_from_lib_to_styled_images', action='store_true',
	help='')

args = vars(ap.parse_args())
print(f'----- Arguments -----\n{args}\n')


ALL_STYLES = ['abstract', 'cubist', 'impressionist', 'sketch', 'watercolor']
ALL_SUBJECTS = ['cats', 'couples', 'dogs', 'family', 'portraits', 'wedding']

if args['sandbox']:
	print('------- Sandbox --------')
	for style in ALL_STYLES:
		sp_path = 'img/squarespace/product-images/'+style+'/self-portraits/'
		new_path = 'img/squarespace/product-images/'+style+'/portraits/'
		if(os.path.isdir(sp_path)):
			os.rename(sp_path, new_path)


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