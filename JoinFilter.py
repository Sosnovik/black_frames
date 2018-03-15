import numpy as np
from multiprocessing.dummy import Pool
from Filter import Filter


class JoinFilter:

	def __init__(self, paths, completion=None):
		if isinstance(paths, str):
			paths = [paths]
		pool = Pool()
		self.filters = pool.map(lambda x: Filter(x), paths)
		self.shape = self.filters[0].shape
		for f in self.filters:
			if f.shape != self.shape:
				print "The shapes of images are not the same"
		if completion:
			completion()

	def process(self, completion=None):
		pool = Pool()
		pool.map(lambda x: x.process(), self.filters)
		if completion:
			completion()

	def less_mask(self):
		less = np.array([f.less_mask for f in self.filters])
		return less.prod(0)

	def more_mask(self):
		more = np.array([f.more_mask for f in self.filters])
		return more.prod(0)

	def less_indices(self, d=1):
		indices = np.where(self.less_mask()==1)[0]
		if d==1: 
			return indices
		m , n = self.shape
		ind = []
		for index in indices:
			x = index / m
			y = index % m
			ind.append((x,y))    
		return np.array(ind).reshape((-1,2))
 
	def more_indices(self, d=1):
		indices = np.where(self.more_mask()==1)[0]
		if d==1: 
			return indices
		m , n = self.shape
		ind = []
		for index in indices:
			x = index / m
			y = index % m
			ind.append((x,y))    
		return np.array(ind).reshape((-1,2))

	def all_indices(self, d=1):
		less = np.array(self.less_indices(d=d))
		more = np.array(self.more_indices(d=d))
		return np.concatenate((less, more))