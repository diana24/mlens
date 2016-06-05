import numpy
import scipy

def normalize(ratings=[]):
	meanr = numpy.mean(ratings)
	sd = numpy.std(ratings,ddof=1)
	norm_ratings = (ratings - meanr)/sd
	return norm_ratings
