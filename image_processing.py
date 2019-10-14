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
		orig = Image.open(file_path).convert('RGBA')

		# Paste original image onto white background
		image = Image.new("RGB", orig.size, "#ffffff")
		image.paste(orig, None, orig)

		# Initialize width and height
		width = image.size[0]
		height = image.size[1]

		# Derive new width and height based on ratio 
		if type(ratio) is tuple:
			if ratio[0] == 0:
				new_height = ratio[1]
				new_width = round(new_height * width / height)
			else:
				new_width = ratio[0]
				new_height = round(new_width * height / width)
		else:
			new_width = round(width * ratio)
			new_height = round(height * ratio)

		# Resize image
		image = image.resize((new_width, new_height), Image.ANTIALIAS)

		# Save image
		if overwrite:
			# Overwrite file with same file name
			image.save(file_path)
		else:
			# Append ratio (ie. x0.25) to new file name
			if type(ratio) is tuple:
				image.save(re.sub(r'\.(?!.*\.)', '_' + str(new_width) + "x" + str(new_height) + '.', file_path), optimize=True, quality=95)
			else:
				image.save(re.sub(r'\.(?!.*\.)', '_x' + str(ratio) + '.', file_path), optimize=True, quality=95)


# resize_image(path='test/', ext='png', ratio=(128, 0))

resize_image(path='../99dropstep/assets/images/thumbs/', ext='png', ratio=(128, 0), overwrite=True)