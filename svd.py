import numpy
import scipy
from recsys.algorithm.factorize import SVD
svd = SVD()
svd.load_data(filename='m-medium/ratings.dat',
	    sep='::',
	    format={'col':0, 'row':1, 'value':2, 'ids': int})
k = 100
svd.compute(k=k,
	    min_values=10,
	    pre_normalize=None,
	    mean_center=True,
	    post_normalize=True,
	    savefile='/tmp/movielens')
sims=[]
for i in range(0,89000):
	for j in range(i+1,90000):
		try:
			l=[[i,j],[svd.similarity(i,j),1]]
			print(l)
		except:
			pass
