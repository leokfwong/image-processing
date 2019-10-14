from PIL import Image
import os
import re

def fetch_files(path, ext):
	"""
	This function fetches all file names that matches extension type.

	Parameters
    ----------
    path : str
		The folder directory path name (ie. "/user/images/animals/cats/")
	ext : str
		The extension type of interest (ie. ".png", ".jpg")

    Returns
    -------
    files : list
        A list of strings representing the names of the images inside folder.
	"""

	# Search through all files within folder 
	all_files = os.listdir(path)
	regex = re.compile('.*\.' + ext + '$')
	files = list(filter(regex.match, all_files))
	return(files)


def resize_image(path, ext, ratio, overwrite=False):
	"""
	This function resizes images based on a ratio or dimensions.

	Parameters
    ----------
    path : str
		The folder directory path name (ie. "/user/images/animals/cats/")
	ext : str
		The extension type of interest (ie. ".png", ".jpg")
	ratio : float or tuple
		The percentage of increase or decrease in image size. 
		(ie. 0.5 = 50% original dimensions; 2 = 200% original dimensions)
		OR
		The new dimension to increase/decrease to. The non-zero element in the
		tuple represent the dimension of reference. If both elements are non-zero,
		the width is the reference by default. The aspect ratio is preserved.
		(ie. (0, 128) = new height is 128px, new width ajusted accordingly)
	overwrite : boolean
		False by default. When True, the output(s) will overwrite the original
		file(s) inside the folder.

    Returns
    -------
    None.
	"""

	# Fetch all file names with extension ext
	files = fetch_files(path, ext)

	# Iterate through each file
	for f in files:

		# Access image
		file_path = path + f
		orig = Image.open(file_path).convert('RGBA')

		# The reason we need to copy image onto white background
		# is to avoid bad quality output. However, if we work with
		# transparent images, then we might want to modify this code.

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
			# Append dimensions to new file name
			if type(ratio) is tuple:
				file_name = re.sub(r'\.(?!.*\.)', '_' + str(new_width) + "x" + str(new_height) + '.', file_path)
			else:
				file_name = re.sub(r'\.(?!.*\.)', '_x' + str(ratio) + '.', file_path)

			# Save new image file
			image.save(file_name, optimize=True, quality=95)


# resize_image(path='test/', ext='png', ratio=(128, 0))