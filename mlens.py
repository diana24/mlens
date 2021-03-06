#!/usr/bin/python

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "."))

from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol
from mrjob.step import MRStep
from operator import itemgetter
from itertools import combinations
from correlations import *

class MRMlens(MRJob):

	# JOB 1
	# ----------------------------------------
	# Mapper: (user_id) ((movie_id),(rating))
	def mapper_arrange(self, _, line):
		try:
			line=line.strip()
			parts = line.split("::")
			user_id = parts[0]
			movie_id = parts[1]
			rating = parts[2]
			yield int(user_id), (int(movie_id), float(rating))
		except:
			pass

	# Reducer: (user_id) ((movie_id, rating), (movie_id, rating)...)
	def reducer_arrange(self, user_id, movie_rating_pairs):
		user_ratings = []
		movie_ids = []
		movie_ratings = []
		for movie_id, rating in movie_rating_pairs:
			movie_ids.append(movie_id)
			movie_ratings.append(rating)
		#movie_ratings = normalize(movie_ratings)
		for i in range(0,len(movie_ratings)-1):
			user_ratings.append([movie_ids[i], movie_ratings[i]])
		yield user_id, user_ratings

	# JOB 2
	# ----------------------------------------
	# Mapper: (movie_id, movie_id) (rating, rating)
	def mapper_groupmv(self, user_id, movie_rating_pairs):
		# Generate pairs (movie_id, movie_id) (rating, rating)
		# from all combinations of ((movie_id, rating), (movie_id, rating)...)
		for pair1, pair2 in combinations(movie_rating_pairs, 2):
		    yield (pair1[0], pair2[0]), (pair1[1], pair2[1])

	# Reducer: (movie_id, movie_id) (similarity)
	def reducer_groupmv(self, movies_pair, ratings_pair):
		cnt = 0
		avg = 0
		movie1, movie2 = movies_pair # movies_pair is a generator
		movie1_ratings = []
		movie2_ratings = []
		for rating1, rating2 in ratings_pair:
			movie1_ratings.append(rating1)
			movie2_ratings.append(rating2)
			cnt += 1
		s = pearson_similarity_normalized(movie1_ratings, movie2_ratings)
		yield (movie1, movie2), (s, cnt)

	# JOB 3
	# ----------------------------------------
	# Mapper: (movie_id1, similarity) (movie_id2, count)
	def mapper_similarity(self, movies_pair, similarity_and_count):
	    similarity, cnt = similarity_and_count
	    movie1, movie2 = movies_pair
	    yield (movie1, similarity), (movie2, cnt)

	# Reducer: (movie_id1, movie_id2, similarity, cnt)
	def reducer_similarity(self, movie_similarity_pair, similar_movie_count_pair):
		movie1, similarity = movie_similarity_pair
		for movie2, cnt in similar_movie_count_pair:
			yield (movie1, movie2), (similarity, cnt)

	def steps(self):
		return [
			MRStep(mapper=self.mapper_arrange, reducer = self.reducer_arrange),
			MRStep(mapper=self.mapper_groupmv, reducer = self.reducer_groupmv),
			MRStep(mapper=self.mapper_similarity, reducer = self.reducer_similarity)
		]

if __name__ == '__main__':
	MRMlens.run()	
