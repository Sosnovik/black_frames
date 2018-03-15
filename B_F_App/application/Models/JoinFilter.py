import numpy as np
from multiprocessing.dummy import Pool
from Filter import Filter


class JoinFilter:

	def __init__(self, paths, success=None, failure=None):
		if isinstance(paths, str):
			paths = [paths]
		pool = Pool()
		self.filters = pool.map(lambda x: Filter(x), paths)
		self.shape = self.filters[0].shape
		for f in self.filters:
			if f.shape != self.shape:
				print "The shapes of images are not the same"
				if failure:
					failure()
				return
		if success:
			success()

	def process(self, completion=None):
		pool = Pool()
		pool.map(lambda x: x.process(), self.filters)
		if completion:
			completion()

	def mark(self, completion=None):
		indices = self.all_indices(d=2)
		pool = Pool()
		pool.map(lambda x: x.mark(indices), self.filters)
		if completion:
			completion()

	def less_mask(self):
		less = np.array([f.less_mask for f in self.filters])
		return less.prod(0)

	def more_mask(self):
		more = np.array([f.more_mask for f in self.filters])
		return more.prod(0)

	def less_indices(self, d=1):
		indices = np.where(self.less_mask() == 1)[0]
		if d == 1:
			return indices
		indices = np.where(self.less_mask().reshape(self.shape) == 1)
		indices = [(indices[0][k], indices[1][k]) for k in xrange(indices[0].shape[0])]
		return np.array(indices).astype(np.int)

	def more_indices(self, d=1):
		indices = np.where(self.more_mask() == 1)[0]
		if d == 1:
			return indices
		indices = np.where(self.more_mask().reshape(self.shape) == 1)
		indices = [(indices[0][k], indices[1][k]) for k in xrange(indices[0].shape[0])]
		return np.array(indices).astype(np.int)

	def all_indices(self, d=1):
		less = np.array(self.less_indices(d=d))
		more = np.array(self.more_indices(d=d))
		if less.size == 0:
			return more
		if more.size == 0:
			return less
		return np.concatenate((less, more))

	def set_k_ult(self, k_ult):
		for filter_ in self.filters:
			filter_.k_ultimate = k_ult

	def set_k_out(self, k_out):
		for filter_ in self.filters:
			filter_.k_outliers = k_out
