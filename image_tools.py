import numpy as np
import matplotlib.pyplot as plt


def outliers(image, k):

	mean = image[image != -1].mean()
	std = image[image != -1].std()
	max_ = mean + k * std
	min_ = mean - k * std
	less_mask1 = image < min_
	less_mask2 = image != -1
	less_mask = less_mask1 * less_mask2
	more_mask = image > max_
	return less_mask, more_mask


def ultimate_outliers(image, k_ult, N_min, max_iter=10, display=False):

	less_mask = np.zeros(image.shape[0]).astype(np.bool)
	more_mask = np.zeros(image.shape[0]).astype(np.bool)
	img = image.copy()
	for iter_ in xrange(max_iter):
		l, m = outliers(img, k_ult)

		if (l+m).sum() == (img != -1).sum(): # converged 
			break

		less_mask += l
		more_mask += m

		if display:
			print iter_, '\t less:', l.sum(), '\t more:', m.sum(), \
			'\t out: %.4f %%' % (100.0* (less_mask.sum() + more_mask.sum()) / img.shape[0])
			plt.figure(figsize=(7,1.5))
			plt.tick_params(
				axis='y',
				which='both',
				bottom='off',
				top='off',
				labelleft='off')
			plt.hist(img[~(less_mask + more_mask)], bins=30)
			plt.show()

		if (l+m).sum() <= N_min: # converged
			break

		img[l+m] = -1
	return less_mask, more_mask







