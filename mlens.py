#!/usr/bin/python

from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol
from mrjob.step import MRStep
from operator import itemgetter
import sys

def avg_sim(rating_pairs):
	return 1

class MRMlens(MRJob):

	def mapper_arrange(self,_,line):
		line=line.strip()
		parts = line.split("::")
		user_id = parts[0]
		movie_id = parts[1]
		rating = parts[2]
		yield user_id, movie_id+','+rating
	def reducer_arrange(self,user_id,pairs):
		res = ""
		for pair in pairs:
			res = res+pair+' '
		yield user_id, res
	def mapper_groupmv(self,user_id,line):
		mvr_pairs = line.split(" ")
		for i in range(0,len(mvr_pairs)-2):
			for j in range(i+1,len(mvr_pairs)-1):
				movie_id1 = mvr_pairs[i].split(",")[0]
				movie_id2 = mvr_pairs[j].split(",")[0]
				rating1 = mvr_pairs[i].split(",")[1]
				rating2 = mvr_pairs[j].split(",")[1]
				if(movie_id1 < movie_id2):
					yield movie_id1+','+movie_id2, rating1+','+rating2
				else:
					yield movie_id2+','+movie_id1, rating2+','+rating1
	def reducer_groupmv(self,mvpair,rating_pairs):
		sim = avg_sim(rating_pairs)
		yield mvpair, sim
	def steps(self):
		return [
			MRStep(mapper=self.mapper_arrange,reducer = self.reducer_arrange),
			MRStep(mapper=self.mapper_groupmv,reducer = self.reducer_groupmv)
		]	
if __name__ == '__main__':
	MRMlens.run()	
