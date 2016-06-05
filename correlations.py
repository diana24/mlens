import numpy
import scipy
from math import sqrt

def normalize(ratings):
	meanr = numpy.mean(ratings)
	sd = numpy.std(ratings,ddof=1)
	norm_ratings = (ratings - meanr)/sd
	return norm_ratings

def pearson_similarity(data1, data2):
    return numpy.corrcoef(data1, data2)[0, 1]


def pearson_similarity_normalized(data1, data2):
    M = min(len(data1), len(data2))
    
    p = 0.0
    s1 = 0.0
    s2 = 0.0
    sq1 = 0.0
    sq2 = 0.0
    
    for i in range(M):
	p += data1[i] * data2[i]
	s1 += data1[i]
	s2 += data2[i]
	sq1 += data1[i] * data1[i]
	sq2 += data2[i] * data2[i]

    norm1 = sqrt(M * sq1 - s1 * s1)
    norm2 = sqrt(M * sq2 - s2 * s2)

    t = M * p - s1 * s2
    b = norm1 * norm2

    s = ( t / float(b)) if b else 0.0
    
    return (s + 1.0) / 2.0


def pearson_similarity_custom(data1, data2):
    M = min(len(data1), len(data2))

    sum1 = 0.0
    sum2 = 0.0

    for i in range(M):
	sum1 += data1[i]
	sum2 += data2[i]

    mean1 = sum1 / M
    mean2 = sum2 / M
    var_sum1 = 0.0
    var_sum2 = 0.0
    cross_sum = 0.0

    for i in range(M):
	var_sum1 += (data1[i] - mean1) ** 2
	var_sum2 += (data2[i] - mean2) ** 2
	cross_sum += (data1[i] * data2[i])

    std1 = (var_sum1 / M) ** 0.5
    std2 = (var_sum2 / M) ** 0.5
    cross_mean = cross_sum / M

    b = float(std1 * std2)
    return ((cross_mean - mean1 * mean2) / b) if b else 0.0


if __name__ == "__main__":
    data1 = [3.0, 4.0, 5.0]
    data2 = [5.0, 4.0, 5.0]
    print pearson_similarity_normalized(data1, data2)