import numpy as np
from image_tools import outliers, ultimate_outliers
from astropy.io import fits


class Filter:

	def __init__(self, path):
		self.k_outliers = 3.0 # k for final selection
		self.k_ultimate = 10.0 # k for preprocessing
		self.n_min = 10 # minimal number of outliers
		self.less_mask = None
		self.more_mask = None
		image = np.array(fits.getdata(path)).astype(np.int)
		self.shape = image.shape
		self.image = image.ravel()
		
	def process(self, display=False):
		less, more = ultimate_outliers(self.image, self.k_ultimate, self.n_min, display=display)
		image = self.image.copy()
		image[less+more] = -1
		self.less_mask, self.more_mask = outliers(image, self.k_outliers)