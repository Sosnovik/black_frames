import numpy as np
from PIL import ImageDraw


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


def ultimate_outliers(image, k_ult, n_min, max_iter=10):
	less_mask = np.zeros(image.shape[0]).astype(np.bool)
	more_mask = np.zeros(image.shape[0]).astype(np.bool)
	img = image.copy()
	for iter_ in xrange(max_iter):
		l, m = outliers(img, k_ult)

		if (l + m).sum() == (img != -1).sum():  # converged
			break

		less_mask += l
		more_mask += m

		if (l + m).sum() <= n_min:  # converged
			break

		img[l + m] = -1
	return less_mask, more_mask


def highlight(img, x, y, r, color):
	img = img.copy()
	draw = ImageDraw.Draw(img)
	draw.ellipse((x - r, y - r, x + r, y + r), fill=color)
	return img
