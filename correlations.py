import numpy
import scipy

def normalize(ratings):
	meanr = numpy.mean(ratings)
	sd = numpy.std(ratings,ddof=1)
	norm_ratings = (ratings - meanr)/sd
	return norm_ratings

def pearson_similarity(list1, list2):
    out_len = min(len(list1), len(list2))
    avg1 = float(sum(list1))/out_len
    avg2 = float(sum(list2))/out_len
    
    return (avg1 + avg2)/2
