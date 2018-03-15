from __future__ import print_function
import numpy as np
from image_tools import outliers, ultimate_outliers, highlight
import pyfits
from PIL import Image

FACTOR = 7

class Filter:

	def __init__(self, path):
		self.k_outliers = 3.0  # k for final selection
		self.k_ultimate = 10.0  # k for preprocessing
		self.n_min = 10  # minimal number of outliers
		self.less_mask = None
		self.more_mask = None
		image = np.array(pyfits.getdata(path)).astype(np.int)
		self.shape = image.shape
		self.image = image.ravel()
		self.pil_image = self.get_pil_image().convert('RGB')
		self.pil_out = None

	def get_pil_image(self):
		img = self.image.reshape(self.shape).copy()
		img -= img.min()
		img = (255.0 * img / img.max()).astype(np.uint8)
		image = Image.fromarray(img[::FACTOR, ::FACTOR])

		return image

	def process(self):
		less, more = ultimate_outliers(self.image, self.k_ultimate, self.n_min)
		image = self.image.copy()
		image[less + more] = -1
		self.less_mask, self.more_mask = outliers(image, self.k_outliers)

	def mark(self, indices):
		img = self.pil_image.copy()
		for ind in indices:
			img = highlight(img, ind[1] / FACTOR, ind[0] / FACTOR, 3, (160, 120, 30))
		self.pil_out = img
