from PIL import Image
import os
import re

def fetch_files(path, ext):
	all_files = os.listdir(path)
	regex = re.compile('.*\.' + ext + '$')
	files = list(filter(regex.match, all_files))
	return(files)


def resize_image(path, ext, ratio, overwrite=False):

	files = fetch_files(path, ext)

	for file in files:
		file_path = path + file
		image = Image.open(file_path)

		new_width = round(image.size[0] * ratio)
		new_height = round(image.size[1] * ratio)

		image.thumbnail((new_width, new_height), Image.ANTIALIAS)

		if overwrite:
			image.save(file_path)
		else:
			image.save(re.sub(r'\.(?!.*\.)', r'_2.', file_path))


resize_image(path='test/', ext='png', ratio=0.25, overwrite=False)