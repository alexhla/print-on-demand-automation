import os
import time
import argparse
import numpy as np
from PIL import Image
from ISR.models import RDN

# Instantiate the argument parser object
ap = argparse.ArgumentParser()

# Add the arguments to the parser
ap.add_argument('-i', '--image_name', nargs=1, metavar=('IMAGE_NAME'), required=True, help='image name (required)')
ap.add_argument('-s', '--source_folder', nargs=1, metavar=('SOURCE_FOLDER'), required=True, help='path to the folder containing image (required)')
ap.add_argument('-d', '--dest_folder', nargs=1, metavar=('DEST_FOLDER'), required=True, help='path to the folder where the enlarged image will be saved (required)')

args = vars(ap.parse_args())
IMAGE_NAME = args['image_name'][0]
SOURCE_FOLDER = args['source_folder'][0]
DEST_FOLDER = args['dest_folder'][0]

print('argparse arguments: %s\n' % args)
print('Image --- %s' % IMAGE_NAME)
print('Image Folder --- %s' % SOURCE_FOLDER)
print('Enlarged Image Folder --- %s' % DEST_FOLDER)

img_path = os.path.join(SOURCE_FOLDER, IMAGE_NAME)
img = Image.open(os.path.join(SOURCE_FOLDER, IMAGE_NAME))
lr_img = np.array(img)
rdn = RDN(weights='psnr-small')
sr_img = rdn.predict(lr_img, by_patch_of_size=50)
img_doubled = Image.fromarray(sr_img)

img_name = IMAGE_NAME[:-4] + '_' +str(max(img_doubled.size)) + IMAGE_NAME[-4:]
img_path = os.path.join(DEST_FOLDER, img_name)
img_doubled.save(img_path)