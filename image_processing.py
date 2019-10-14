from PIL import Image
import os
import re

def fetch_files(path, ext):

	# Search through all files within folder 
	all_files = os.listdir(path)
	regex = re.compile('.*\.' + ext + '$')
	files = list(filter(regex.match, all_files))
	return(files)


def resize_image(path, ext, ratio, overwrite=False):

	# Fetch all file names with extension ext
	files = fetch_files(path, ext)

	# Iterate through each file
	for f in files:

		# Access image
		file_path = path + f
		image = Image.open(file_path)

		# Derive new width and height based on ratio 
		new_width = round(image.size[0] * ratio)
		new_height = round(image.size[1] * ratio)

		# Resize image
		image.thumbnail((new_width, new_height), Image.ANTIALIAS)

		# Save image
		if overwrite:
			# Overwrite file with same file name
			image.save(file_path)
		else:
			# Append ratio (ie. x0.25) to new file name
			image.save(re.sub(r'\.(?!.*\.)', '_x' + str(ratio) + '.', file_path))


resize_image(path='test/', ext='png', ratio=1.25, overwrite=False)